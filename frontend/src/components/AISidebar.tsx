import { useState } from 'react'
import { Sparkles, Send, User } from 'lucide-react'
import { api } from '../lib/api'

interface AISidebarProps {
  context: string
}

export function AISidebar({ context }: AISidebarProps) {
  const [messages, setMessages] = useState([
    { role: 'ai', text: `Welcome back. I see you're currently in the **${context}** view. How can I assist you today?` }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    
    const userMessage = { role: 'user', text: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    
    try {
      const response = await api.chat(input, context)
      setMessages(prev => [...prev, { role: 'ai', text: response.response }])
    } catch (error: any) {
      setMessages(prev => [...prev, { role: 'ai', text: `Error: ${error.message}. Make sure your Flask backend is running on port 5001.` }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] bg-white/30 backdrop-blur-sm border border-aura-accent rounded-[2rem] overflow-hidden">
      {/* Sidebar Header */}
      <div className="p-6 border-b border-aura-accent flex items-center gap-3">
        <div className="p-2 bg-aura-gold/10 rounded-xl text-aura-gold">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <h3 className="font-bold">Aura Partner</h3>
          <p className="text-[10px] uppercase tracking-widest text-aura-gold font-bold">Gemini 2.5 Flash</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              msg.role === 'ai' ? 'bg-aura-slate text-aura-ivory' : 'bg-aura-gold-muted text-aura-slate'
            }`}>
              {msg.role === 'ai' ? <Sparkles className="w-4 h-4" /> : <User className="w-4 h-4" />}
            </div>
            <div className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
              msg.role === 'ai' 
                ? 'bg-white border border-aura-accent text-aura-slate' 
                : 'bg-aura-slate text-white'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="p-6 border-t border-aura-accent">
        <div className="relative">
          <textarea 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask about your ${context.toLowerCase()}...`}
            className="w-full bg-white/80 border border-aura-accent rounded-2xl px-4 py-3 pr-12 text-sm outline-none focus:border-aura-gold transition-all resize-none min-h-[44px] max-h-32"
            rows={1}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSend()
              }
            }}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className={`absolute right-3 bottom-3 p-1.5 rounded-lg transition-all ${
              isLoading ? 'bg-aura-accent text-aura-slate/30' : 'bg-aura-slate text-aura-ivory hover:bg-aura-gold'
            }`}
          >
            {isLoading ? <div className="w-4 h-4 border-2 border-aura-slate/30 border-t-aura-slate rounded-full animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
        </div>
      </div>
    </div>
  )
}
