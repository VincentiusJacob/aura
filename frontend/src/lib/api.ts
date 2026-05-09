import { auth } from './firebase';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

async function getAuthToken() {
  const user = auth.currentUser;
  if (!user) return null;
  return await user.getIdToken();
}

export const api = {
  async request(endpoint: string, options: RequestInit = {}) {
    const token = await getAuthToken();
    
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'An unknown error occurred' }));
      throw new Error(error.error || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  // Chat with Gemini
  async chat(message: string, context: string) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, context }),
    });
  },

  // Task Management
  async getTasks() {
    return this.request('/tasks');
  },

  async createTask(task: { title: string; description?: string }) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  },

  // Notes Management
  async getNotes() {
    return this.request('/notes');
  },

  async createNote(note: { title: string; excerpt?: string; content?: string }) {
    return this.request('/notes', {
      method: 'POST',
      body: JSON.stringify(note),
    });
  },

  // Events Management
  async getEvents() {
    return this.request('/events');
  },

  async createEvent(event: { title: string; date?: string; time?: string }) {
    return this.request('/events', {
      method: 'POST',
      body: JSON.stringify(event),
    });
  },

  // Generic Delete
  async deleteItem(collection: 'tasks' | 'notes' | 'events', id: string) {
    return this.request(`/${collection}/${id}`, {
      method: 'DELETE',
    });
  }
};
