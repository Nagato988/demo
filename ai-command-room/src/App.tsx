import { useStore } from './store/useStore'
import { ChatTimeline } from './components/ChatTimeline'
import { StatusPanel } from './components/StatusPanel'
import { BossComposer } from './components/BossComposer'
import { OverrideBar } from './components/OverrideBar'
import type { ClaudeStatus, CodexStatus, BossStatus } from './types'

const CLAUDE_COLOR: Record<ClaudeStatus, string> = {
  IDLE: '#484f58', PLANNING: '#7ee787', REVIEWING: '#4dd0e1', ESCALATED: '#f85149',
}
const CODEX_COLOR: Record<CodexStatus, string> = {
  WAITING: '#484f58', WORKING: '#ffb74d', BLOCKED: '#f85149',
}
const BOSS_COLOR: Record<BossStatus, string> = {
  IDLE: '#484f58', DECIDING: '#58a6ff',
}

function ParticipantBar() {
  const { claudeStatus, codexStatus, bossStatus } = useStore()

  const participants = [
    { emoji: '🧑‍💼', name: 'Boss',   color: BOSS_COLOR[bossStatus],   active: bossStatus !== 'IDLE' },
    { emoji: '🧠',   name: 'Claude', color: CLAUDE_COLOR[claudeStatus], active: claudeStatus !== 'IDLE' },
    { emoji: '⚙️',   name: 'Codex',  color: CODEX_COLOR[codexStatus],  active: codexStatus !== 'WAITING' },
  ]

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: 16,
      padding: '10px 20px',
      borderBottom: '1px solid #21262d',
      background: '#161b22',
      flexShrink: 0,
    }}>
      <span style={{ fontSize: 15, fontWeight: 800, color: '#c9d1d9', letterSpacing: '-0.02em' }}>
        ⚡ AI Command Room
      </span>
      <div style={{ flex: 1 }} />
      {participants.map(({ emoji, name, color, active }) => (
        <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12 }}>
          <span>{emoji}</span>
          <span style={{ color: '#8b949e' }}>{name}</span>
          <span style={{
            width: 7,
            height: 7,
            borderRadius: '50%',
            background: color,
            boxShadow: active ? `0 0 7px ${color}` : 'none',
            display: 'inline-block',
            transition: 'all 0.3s',
          }} />
        </div>
      ))}
    </div>
  )
}

export default function App() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      background: '#0d1117',
      color: '#c9d1d9',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      overflow: 'hidden',
    }}>
      <ParticipantBar />
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        {/* Main column */}
        <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
          <ChatTimeline />
          <OverrideBar />
          <BossComposer />
        </div>
        {/* Sidebar */}
        <StatusPanel />
      </div>
    </div>
  )
}
