import { useState, useEffect } from 'react'
import { CheckSquare, Calendar, FileText, LayoutGrid } from 'lucide-react'
import { api } from '../lib/api'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog'
import { Input } from './ui/input'

interface DashboardProps {
  activeContext: string
  setActiveContext: (context: string) => void
}

export function Dashboard({ activeContext, setActiveContext }: DashboardProps) {
  const [tasks, setTasks] = useState<any[]>([])
  const [notes, setNotes] = useState<any[]>([])
  const [events, setEvents] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)

  // Dialog states
  const [isTaskOpen, setIsTaskOpen] = useState(false)
  const [isNoteOpen, setIsNoteOpen] = useState(false)
  const [isEventOpen, setIsEventOpen] = useState(false)
  const [inputValue, setInputValue] = useState('')

  const navItems = [
    { id: 'Overview', icon: <LayoutGrid className="w-5 h-5" /> },
    { id: 'Tasks', icon: <CheckSquare className="w-5 h-5" /> },
    { id: 'Calendar', icon: <Calendar className="w-5 h-5" /> },
    { id: 'Notes', icon: <FileText className="w-5 h-5" /> },
  ]

  const fetchData = async () => {
    setIsLoading(true)
    try {
      const [t, n, e] = await Promise.all([
        api.getTasks().catch(() => []),
        api.getNotes().catch(() => []),
        api.getEvents().catch(() => [])
      ])
      setTasks(t.length ? t : [])
      setNotes(n.length ? n : [])
      setEvents(e.length ? e : [])
    } catch (error) {
      console.error("Failed to fetch data", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return
    await api.createTask({ title: inputValue, description: "New task added" })
    setInputValue('')
    setIsTaskOpen(false)
    fetchData()
  }

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return
    await api.createNote({ title: inputValue, excerpt: "Started writing..." })
    setInputValue('')
    setIsNoteOpen(false)
    fetchData()
  }

  const handleAddEvent = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return
    await api.createEvent({ title: inputValue, date: new Date().toISOString().split('T')[0] })
    setInputValue('')
    setIsEventOpen(false)
    fetchData()
  }

  const handleDelete = async (collection: 'tasks'|'notes'|'events', id: string) => {
    await api.deleteItem(collection, id)
    fetchData()
  }

  return (
    <div className="space-y-12">
      {/* Header & Nav */}
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-4xl font-serif mb-2">Aura</h2>
          <p className="text-aura-slate/50 font-medium">Good afternoon, Vincentius.</p>
        </div>
        <nav className="flex gap-2 p-1.5 bg-aura-accent/30 rounded-full border border-aura-accent/20">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveContext(item.id)}
              className={`flex items-center gap-2 px-6 py-2.5 rounded-full transition-all duration-300 font-medium ${
                activeContext === item.id 
                  ? 'bg-white shadow-sm text-aura-slate border border-aura-accent/30' 
                  : 'text-aura-slate/40 hover:text-aura-slate'
              }`}
            >
              {item.icon}
              {item.id}
            </button>
          ))}
        </nav>
      </header>

      {/* Main Content Area */}
      <section className="animate-aura-in">
        {activeContext === 'Overview' && (
          <div className="grid grid-cols-2 gap-8">
            <div className="glass-card p-8 min-h-[400px]">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-2xl">Priority Tasks</h3>
                <button onClick={() => setActiveContext('Tasks')} className="text-aura-gold font-bold text-xs uppercase tracking-widest">View All</button>
              </div>
              <div className="space-y-4">
                {isLoading ? <p className="text-aura-slate/50 text-sm">Loading...</p> : 
                  tasks.slice(0,3).map(task => (
                    <TaskItem key={task.id} title={task.title} description={task.description} onDelete={() => handleDelete('tasks', task.id)} />
                  ))
                }
                {!isLoading && tasks.length === 0 && <p className="text-aura-slate/50 text-sm">No tasks yet.</p>}
              </div>
            </div>
            <div className="glass-card p-8 min-h-[400px]">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-2xl">Recent Notes</h3>
                <button onClick={() => setActiveContext('Notes')} className="text-aura-gold font-bold text-xs uppercase tracking-widest">New Note</button>
              </div>
              <div className="space-y-6">
                {isLoading ? <p className="text-aura-slate/50 text-sm">Loading...</p> : 
                  notes.slice(0,3).map(note => (
                    <NotePreview key={note.id} title={note.title} excerpt={note.excerpt} onDelete={() => handleDelete('notes', note.id)} />
                  ))
                }
                {!isLoading && notes.length === 0 && <p className="text-aura-slate/50 text-sm">No notes yet.</p>}
              </div>
            </div>
          </div>
        )}

        {activeContext === 'Tasks' && (
          <div className="glass-card p-12 min-h-[600px]">
            <h3 className="text-4xl mb-8">My Tasks</h3>
            <div className="space-y-4 max-w-2xl mb-8">
              {isLoading ? <p className="text-aura-slate/50">Loading tasks...</p> : 
                tasks.map(task => (
                  <TaskItem key={task.id} title={task.title} description={task.description} onDelete={() => handleDelete('tasks', task.id)} />
                ))
              }
              {!isLoading && tasks.length === 0 && <p className="text-aura-slate/50">Your task list is empty.</p>}
            </div>
            <Dialog open={isTaskOpen} onOpenChange={setIsTaskOpen}>
              <DialogTrigger asChild>
                <button className="w-full max-w-2xl py-4 border-2 border-dashed border-aura-accent rounded-2xl text-aura-slate/30 font-bold hover:border-aura-gold hover:text-aura-gold transition-all">
                  + Add New Task
                </button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>New Task</DialogTitle>
                  <DialogDescription>What needs to be done?</DialogDescription>
                </DialogHeader>
                <form onSubmit={handleAddTask} className="space-y-4 pt-4">
                  <Input 
                    placeholder="E.g., Complete the project proposal" 
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    autoFocus
                  />
                  <DialogFooter>
                    <button type="submit" className="btn-primary w-full py-3">Add Task</button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        )}

        {activeContext === 'Notes' && (
          <div className="glass-card p-12 min-h-[600px]">
            <h3 className="text-4xl mb-8">Knowledge Base</h3>
            <div className="grid grid-cols-3 gap-6">
              {isLoading ? <p className="text-aura-slate/50 col-span-3">Loading notes...</p> : 
                notes.map(note => (
                  <div key={note.id} className="group p-6 bg-white/50 rounded-3xl border border-aura-accent relative">
                    <button onClick={() => handleDelete('notes', note.id)} className="absolute top-4 right-4 text-xs text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">Delete</button>
                    <h4 className="font-bold mb-2 pr-6">{note.title}</h4>
                    <p className="text-sm text-aura-slate/50">{note.excerpt}</p>
                  </div>
                ))
              }
              <Dialog open={isNoteOpen} onOpenChange={setIsNoteOpen}>
                <DialogTrigger asChild>
                  <button className="aspect-square flex flex-col items-center justify-center border-2 border-dashed border-aura-accent rounded-3xl text-aura-slate/30 hover:border-aura-gold hover:text-aura-gold transition-all">
                    <span className="text-2xl mb-2">+</span>
                    <span className="text-xs font-bold uppercase tracking-widest">New Entry</span>
                  </button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>New Note</DialogTitle>
                    <DialogDescription>Start a new entry in your knowledge base.</DialogDescription>
                  </DialogHeader>
                  <form onSubmit={handleAddNote} className="space-y-4 pt-4">
                    <Input 
                      placeholder="Note Title" 
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      autoFocus
                    />
                    <DialogFooter>
                      <button type="submit" className="btn-primary w-full py-3">Create Note</button>
                    </DialogFooter>
                  </form>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        )}

        {(activeContext === 'Calendar') && (
          <div className="glass-card p-12 min-h-[600px]">
             <h3 className="text-4xl mb-8">Calendar Events</h3>
             <div className="space-y-4 max-w-2xl mb-8">
              {isLoading ? <p className="text-aura-slate/50">Loading events...</p> : 
                events.map(event => (
                  <div key={event.id} className="group flex items-start gap-4 p-4 hover:bg-white/50 rounded-2xl transition-all border border-transparent hover:border-white/20">
                    <Calendar className="w-5 h-5 mt-1 text-aura-gold" />
                    <div className="flex-1">
                      <h4 className="font-bold mb-1 leading-tight">{event.title}</h4>
                      <p className="text-sm text-aura-slate/50">{event.date}</p>
                    </div>
                    <button onClick={() => handleDelete('events', event.id)} className="text-xs text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">Delete</button>
                  </div>
                ))
              }
              {!isLoading && events.length === 0 && <p className="text-aura-slate/50">No upcoming events.</p>}
            </div>
            <Dialog open={isEventOpen} onOpenChange={setIsEventOpen}>
              <DialogTrigger asChild>
                <button className="w-full max-w-2xl py-4 border-2 border-dashed border-aura-accent rounded-2xl text-aura-slate/30 font-bold hover:border-aura-gold hover:text-aura-gold transition-all">
                  + Add Event
                </button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>New Event</DialogTitle>
                  <DialogDescription>Add an event to your calendar.</DialogDescription>
                </DialogHeader>
                <form onSubmit={handleAddEvent} className="space-y-4 pt-4">
                  <Input 
                    placeholder="Event Name" 
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    autoFocus
                  />
                  <DialogFooter>
                    <button type="submit" className="btn-primary w-full py-3">Add Event</button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        )}
      </section>
    </div>
  )
}

function TaskItem({ title, description, onDelete }: { title: string, description: string, onDelete: () => void }) {
  return (
    <div className="group flex items-start gap-4 p-4 hover:bg-white/50 rounded-2xl transition-all border border-transparent hover:border-white/20">
      <div onClick={onDelete} className="w-6 h-6 rounded-full border-2 border-aura-accent mt-0.5 hover:bg-aura-gold hover:border-aura-gold cursor-pointer transition-colors" />
      <div>
        <h4 className="font-bold mb-1 leading-tight">{title}</h4>
        <p className="text-sm text-aura-slate/50">{description}</p>
      </div>
    </div>
  )
}

function NotePreview({ title, excerpt, onDelete }: { title: string, excerpt: string, onDelete: () => void }) {
  return (
    <div className="group cursor-pointer border-b border-aura-accent/50 pb-4 last:border-0 relative">
      <h4 className="font-bold text-lg mb-2 group-hover:text-aura-gold transition-colors pr-8">{title}</h4>
      <p className="text-aura-slate/60 line-clamp-2 text-sm leading-relaxed">{excerpt}</p>
      <button onClick={(e) => { e.stopPropagation(); onDelete(); }} className="absolute top-0 right-0 text-xs text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">Delete</button>
    </div>
  )
}
