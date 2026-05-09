import { useState, useEffect } from 'react'
import { CommandRail } from './components/CommandRail'
import { Dashboard } from './components/Dashboard'
import { AISidebar } from './components/AISidebar'
import { auth, googleProvider } from './lib/firebase'
import { onAuthStateChanged, signInWithPopup } from 'firebase/auth'

function App() {
  const [user, setUser] = useState<any>(null)
  const [isCommandOpen, setIsCommandOpen] = useState(false)
  const [activeContext, setActiveContext] = useState('Overview')

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
    })
    return () => unsubscribe()
  }, [])

  const handleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider)
    } catch (error) {
      console.error("Login failed:", error)
    }
  }

  // Keyboard shortcut for Command Rail
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsCommandOpen(prev => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  if (!user) {
    return (
      <div className="h-screen flex items-center justify-center bg-aura-ivory">
        <div className="text-center animate-aura-in">
          <h1 className="text-4xl mb-4 text-aura-slate">Aura</h1>
          <p className="text-aura-slate/60 mb-8 font-sans">Elevate your productivity.</p>
          <button 
            onClick={handleLogin}
            className="btn-primary"
          >
            Enter the Command Center
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-aura-ivory text-aura-slate font-sans selection:bg-aura-gold-muted selection:text-aura-slate">
      <div className="max-w-[1440px] mx-auto px-8 py-12 flex gap-8">
        {/* Main Dashboard Area */}
        <main className="flex-1 animate-aura-in">
          <Dashboard activeContext={activeContext} setActiveContext={setActiveContext} />
        </main>

        {/* AI Sidebar */}
        <aside className="w-80 animate-aura-in" style={{ animationDelay: '0.2s' }}>
          <AISidebar context={activeContext} />
        </aside>
      </div>

      {/* Floating Command Rail */}
      <CommandRail isOpen={isCommandOpen} onClose={() => setIsCommandOpen(false)} />
    </div>
  )
}

export default App
