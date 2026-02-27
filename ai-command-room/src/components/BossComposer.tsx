import { useState } from 'react'
import { useStore } from '../store/useStore'

export function BossComposer() {
  const [text, setText] = useState('')
  const sendCommand = useStore(s => s.sendCommand)

  const send = () => {
    const trimmed = text.trim()
    if (!trimmed) return
    sendCommand(trimmed)
    setText('')
  }

  return (
    <div style={{
      padding: '12px 20px',
      borderTop: '1px solid #21262d',
      background: '#161b22',
      display: 'flex',
      gap: 10,
      alignItems: 'flex-end',
    }}>
      <div style={{ fontSize: 20, paddingBottom: 10, flexShrink: 0 }}>🧑‍💼</div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            send()
          }
        }}
        placeholder="Send a command to Claude… (Enter to send, Shift+Enter for newline)"
        rows={2}
        style={{
          flex: 1,
          background: '#0d1117',
          border: '1px solid #30363d',
          borderRadius: 6,
          color: '#c9d1d9',
          fontSize: 13,
          padding: '9px 13px',
          resize: 'none',
          outline: 'none',
          fontFamily: 'inherit',
          lineHeight: 1.55,
          transition: 'border-color 0.15s',
        }}
        onFocus={e => { e.target.style.borderColor = '#388bfd' }}
        onBlur={e => { e.target.style.borderColor = '#30363d' }}
      />
      <button
        onClick={send}
        disabled={!text.trim()}
        style={{
          background: text.trim() ? '#238636' : '#21262d',
          border: '1px solid',
          borderColor: text.trim() ? '#2ea043' : '#30363d',
          borderRadius: 6,
          color: text.trim() ? '#ffffff' : '#484f58',
          cursor: text.trim() ? 'pointer' : 'not-allowed',
          fontSize: 13,
          fontWeight: 600,
          padding: '0 18px',
          height: 56,
          whiteSpace: 'nowrap',
          transition: 'all 0.15s',
          fontFamily: 'inherit',
        }}
      >
        Send ↵
      </button>
    </div>
  )
}
