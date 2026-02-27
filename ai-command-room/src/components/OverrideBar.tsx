import { useStore } from '../store/useStore'

interface Btn {
  label: string
  content: string
  color: string
}

const BUTTONS: Btn[] = [
  {
    label: '✅ Accept Anyway',
    content: '[Boss override] Accepting current output. Proceed to commit without further review.',
    color: '#3fb950',
  },
  {
    label: '🔄 Force Codex Retry',
    content: '[Boss override] Forcing Codex retry from scratch. Discard current output and re-run.',
    color: '#ffb74d',
  },
  {
    label: '🔍 Force Deep Analysis',
    content: '[Boss override] Escalating to Claude for deep analysis. Codex suspended until further notice.',
    color: '#58a6ff',
  },
  {
    label: '🛑 Stop Task',
    content: '[Boss override] Task stopped. All agents return to IDLE. No commit.',
    color: '#f85149',
  },
]

function OverrideButton({ label, content, color }: Btn) {
  const addMessage = useStore(s => s.addMessage)

  return (
    <button
      onClick={() => addMessage({ role: 'Boss', type: 'OVERRIDE', content })}
      style={{
        background: 'transparent',
        border: `1px solid ${color}`,
        borderRadius: 5,
        color,
        cursor: 'pointer',
        fontSize: 11,
        fontWeight: 700,
        padding: '5px 11px',
        letterSpacing: '0.02em',
        whiteSpace: 'nowrap',
        fontFamily: 'inherit',
        transition: 'background 0.12s',
      }}
      onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = color + '1a' }}
      onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = 'transparent' }}
    >
      {label}
    </button>
  )
}

export function OverrideBar() {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      padding: '8px 20px',
      borderTop: '1px solid #21262d',
      background: '#0d1117',
      overflowX: 'auto',
    }}>
      <span style={{
        fontSize: 10,
        color: '#484f58',
        fontWeight: 700,
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
        marginRight: 4,
        flexShrink: 0,
      }}>
        Boss Overrides:
      </span>
      {BUTTONS.map(btn => <OverrideButton key={btn.label} {...btn} />)}
    </div>
  )
}
