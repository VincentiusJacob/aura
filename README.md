# Project Aura | AI-Powered Unified Command Center

Aura is a high-end, minimalist productivity application designed to be your "Second Brain." It integrates tasks, notes, and calendar management with a context-aware AI partner powered by Gemini 2.5 Flash.

## Tech Stack
- **Frontend**: React (Vite), Tailwind v4, Framer Motion, Lucide.
- **Backend**: Python 3.12, Flask, Firebase Admin SDK.
- **AI**: Google Gemini 2.5 Flash via Google AI Studio.
- **Infrastructure**: Firebase Auth & Firestore.

## Local Setup

### 1. Backend Setup
1. Navigate to `/backend`.
2. Create a virtual environment: `python -m venv venv`.
3. Activate it: `source venv/bin/activate` (Mac/Linux).
4. Install dependencies: `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` and fill in your:
   - `GEMINI_API_KEY` (Get at [aistudio.google.com](https://aistudio.google.com/))
   - `FIREBASE_SERVICE_ACCOUNT_JSON` (Generate in Firebase Console -> Project Settings -> Service Accounts).
6. Run: `python app.py`.

### 2. Frontend Setup
1. Navigate to `/frontend`.
2. Install dependencies: `npm install`.
3. Copy `.env.example` to `.env.local` and fill in your Firebase Client config.
4. Run: `npm run dev`.

## Deployment

### Frontend (Firebase Hosting)
1. Install Firebase CLI: `npm install -g firebase-tools`.
2. Login: `firebase login`.
3. Initialize (if needed): `firebase init hosting`.
4. Deploy: `npm run build && firebase deploy --only hosting`.

### Backend (Render)
1. Push this repository to GitHub.
2. Connect your GitHub account to [Render](https://render.com).
3. Render will automatically detect `render.yaml` and prompt you to create the service.
4. Add your Environment Variables (`GEMINI_API_KEY`, etc.) in the Render dashboard.

## Design Philosophy: Minimalist Luxury
Aura follows a "Calm Tech" aesthetic:
- **Typography**: Fraunces (Serif) for character, Instrument Sans for clarity.
- **Interaction**: Keyboard-first via the Command Rail (`Cmd + K`).
- **Atmosphere**: Glassmorphic UI with soft ivory tones and gold accents.
