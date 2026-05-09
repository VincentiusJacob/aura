import { motion, AnimatePresence } from 'framer-motion'
import { Search, Command, Zap, Clock, Calendar, CheckSquare } from 'lucide-react'

interface CommandRailProps {
  isOpen: boolean
  onClose: () => void
}

export function CommandRail({ isOpen, onClose }: CommandRailProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-aura-slate/20 backdrop-blur-sm z-40"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -20 }}
            transition={{ type: 'spring', damping: 20, stiffness: 300 }}
            className="fixed top-[20%] left-1/2 -translate-x-1/2 w-full max-w-2xl z-50 px-4"
          >
            <div className="bg-white border border-aura-accent shadow-2xl rounded-3xl overflow-hidden">
              <div className="flex items-center px-6 py-4 border-b border-aura-accent">
                <Search className="w-5 h-5 text-aura-slate/40 mr-4" />
                <input 
                  autoFocus
                  placeholder="What would you like to achieve?"
                  className="flex-1 bg-transparent border-none outline-none text-lg text-aura-slate placeholder:text-aura-slate/30"
                />
                <div className="flex items-center gap-1 px-2 py-1 bg-aura-ivory rounded border border-aura-accent text-[10px] font-bold text-aura-slate/40">
                  <Command className="w-3 h-3" /> K
                </div>
              </div>

              <div className="p-4 max-h-96 overflow-y-auto">
                <div className="mb-4">
                  <p className="px-3 text-[10px] font-bold uppercase tracking-widest text-aura-slate/40 mb-2">Suggestions</p>
                  <CommandItem icon={<Zap className="w-4 h-4" />} label="Quick Action: Draft Email" shortcut="D" />
                  <CommandItem icon={<CheckSquare className="w-4 h-4" />} label="Create New Task" shortcut="N" />
                  <CommandItem icon={<Calendar className="w-4 h-4" />} label="Schedule Meeting" shortcut="M" />
                </div>

                <div>
                  <p className="px-3 text-[10px] font-bold uppercase tracking-widest text-aura-slate/40 mb-2">Recent</p>
                  <CommandItem icon={<Clock className="w-4 h-4" />} label="Review Project Aura specs" />
                </div>
              </div>

              <div className="px-6 py-3 bg-aura-ivory border-t border-aura-accent flex justify-between items-center text-[11px] text-aura-slate/40">
                <span>Navigate with arrows, select with Enter</span>
                <span>ESC to close</span>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

function CommandItem({ icon, label, shortcut }: { icon: React.ReactNode, label: string, shortcut?: string }) {
  return (
    <div className="flex items-center justify-between px-3 py-3 hover:bg-aura-ivory rounded-xl cursor-pointer transition-colors group">
      <div className="flex items-center gap-4">
        <div className="p-2 bg-aura-ivory rounded-lg group-hover:bg-white border border-transparent group-hover:border-aura-accent transition-all">
          {icon}
        </div>
        <span className="font-medium">{label}</span>
      </div>
      {shortcut && (
        <span className="text-[10px] font-bold text-aura-slate/30 bg-white px-1.5 py-0.5 rounded border border-aura-accent">
          {shortcut}
        </span>
      )}
    </div>
  )
}
