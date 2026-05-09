import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin
# In production, use GOOGLE_APPLICATION_CREDENTIALS env var or a service account JSON
try:
    if not firebase_admin._apps:
        # Check for service account path in env
        cred_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # Fallback for local development if creds are not provided yet
            firebase_admin.initialize_app()
    db = firestore.client()
except Exception as e:
    print(f"Firebase initialization warning: {e}")

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash') # Fallback to latest stable version

def verify_token():
    """Middleware-like function to verify Firebase ID Token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "aura-backend"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    user = verify_token()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    message = data.get('message')
    context = data.get('context', '') # UI context (e.g. current tasks)
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    try:
        # Construct a contextual prompt
        prompt = f"Context: {context}\nUser: {message}"
        response = model.generate_content(prompt)
        return jsonify({"response": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    user = verify_token()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    uid = user['uid']
    tasks_ref = db.collection('users').document(uid).collection('tasks')
    
    if request.method == 'GET':
        tasks = [doc.to_dict() | {"id": doc.id} for doc in tasks_ref.stream()]
        return jsonify(tasks), 200
    
    if request.method == 'POST':
        task_data = request.json
        # Basic validation
        if 'title' not in task_data:
            return jsonify({"error": "Title is required"}), 400
        
        # Add metadata
        task_data['uid'] = uid
        task_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        new_task_ref = tasks_ref.add(task_data)
        return jsonify({"id": new_task_ref[1].id, "status": "success"}), 201

@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    user = verify_token()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    uid = user['uid']
    notes_ref = db.collection('users').document(uid).collection('notes')
    
    if request.method == 'GET':
        notes = [doc.to_dict() | {"id": doc.id} for doc in notes_ref.stream()]
        return jsonify(notes), 200
    
    if request.method == 'POST':
        note_data = request.json
        if 'title' not in note_data:
            return jsonify({"error": "Title is required"}), 400
        
        note_data['uid'] = uid
        note_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        new_note_ref = notes_ref.add(note_data)
        return jsonify({"id": new_note_ref[1].id, "status": "success"}), 201

@app.route('/api/events', methods=['GET', 'POST'])
def handle_events():
    user = verify_token()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    uid = user['uid']
    events_ref = db.collection('users').document(uid).collection('events')
    
    if request.method == 'GET':
        events = [doc.to_dict() | {"id": doc.id} for doc in events_ref.stream()]
        return jsonify(events), 200
    
    if request.method == 'POST':
        event_data = request.json
        if 'title' not in event_data:
            return jsonify({"error": "Title is required"}), 400
        
        event_data['uid'] = uid
        event_data['created_at'] = firestore.SERVER_TIMESTAMP
        
        new_event_ref = events_ref.add(event_data)
        return jsonify({"id": new_event_ref[1].id, "status": "success"}), 201

@app.route('/api/<collection>/<doc_id>', methods=['DELETE'])
def delete_item(collection, doc_id):
    user = verify_token()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    allowed_collections = ['tasks', 'notes', 'events']
    if collection not in allowed_collections:
        return jsonify({"error": "Invalid collection"}), 400

    uid = user['uid']
    doc_ref = db.collection('users').document(uid).collection(collection).document(doc_id)
    doc_ref.delete()
    
    return jsonify({"status": "deleted"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
