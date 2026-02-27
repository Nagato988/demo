import { useState } from 'react'
import type { Message } from '../types'

const ROLE_CONFIG: Record<string, { emoji: string; color: string }> = {
  Boss:   { emoji: '🧑‍💼', color: '#58a6ff' },
  Claude: { emoji: '🧠',   color: '#7ee787' },
  Codex:  { emoji: '⚙️',   color: '#ffb74d' },
  System: { emoji: '🔧',   color: '#8b949e' },
}

const TYPE_COLOR: Record<string, string> = {
  COMMAND:      '#58a6ff',
  PLAN:         '#7ee787',
  ROUTING:      '#ce93d8',
  REVIEW:       '#4dd0e1',
  DECISION:     '#fff176',
  QUALITY_GATE: '#ffca28',
  EXECUTION:    '#ffb74d',
  DIFF:         '#f78166',
  OUTPUT:       '#79c0ff',
  ERROR:        '#f85149',
  OVERRIDE:     '#ff4081',
  SYSTEM:       '#8b949e',
}

export function MessageCard({ message }: { message: Message }) {
  const [expanded, setExpanded] = useState<Record<number, boolean>>({})
  const cfg = ROLE_CONFIG[message.role] ?? ROLE_CONFIG.System
  const typeColor = TYPE_COLOR[message.type] ?? '#8b949e'

  return (
    <div style={{
      display: 'flex',
      gap: 12,
      padding: '14px 20px',
      borderBottom: '1px solid #21262d',
      background: message.type === 'OVERRIDE'
        ? 'rgba(255,64,129,0.06)'
        : message.type === 'QUALITY_GATE'
          ? 'rgba(255,202,40,0.04)'
          : 'transparent',
    }}>
      {/* Avatar */}
      <div style={{ fontSize: 20, flexShrink: 0, paddingTop: 2, lineHeight: 1 }}>
        {cfg.emoji}
      </div>

      {/* Content */}
      <div style={{ flex: 1, minWidth: 0 }}>
        {/* Header row */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
          <span style={{ color: cfg.color, fontWeight: 700, fontSize: 13 }}>
            {message.role}
          </span>
          <span style={{
            fontSize: 10,
            fontWeight: 700,
            padding: '1px 6px',
            borderRadius: 4,
            background: typeColor + '20',
            color: typeColor,
            border: `1px solid ${typeColor}40`,
            letterSpacing: '0.06em',
          }}>
            {message.type}
          </span>
          <span style={{ color: '#484f58', fontSize: 11, marginLeft: 'auto', flexShrink: 0 }}>
            {message.timestamp}
          </span>
        </div>

        {/* Body */}
        <div style={{
          color: '#c9d1d9',
          fontSize: 13,
          lineHeight: 1.65,
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}>
          {message.content}
        </div>

        {/* Attachments */}
        {message.attachments?.map((att, i) => (
          <div key={i} style={{ marginTop: 8 }}>
            <button
              onClick={() => setExpanded(e => ({ ...e, [i]: !e[i] }))}
              style={{
                background: '#161b22',
                border: '1px solid #30363d',
                borderRadius: 4,
                color: '#8b949e',
                fontSize: 11,
                padding: '3px 10px',
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 5,
                fontFamily: 'inherit',
              }}
            >
              <span style={{ fontSize: 9 }}>{expanded[i] ? '▼' : '▶'}</span>
              {att.type.toUpperCase()} · {att.label}
            </button>
            {expanded[i] && (
              <pre style={{
                margin: '6px 0 0',
                padding: 12,
                background: '#0d1117',
                border: '1px solid #30363d',
                borderRadius: 4,
                color: att.type === 'diff' ? '#7ee787' : '#c9d1d9',
                fontSize: 12,
                overflow: 'auto',
                maxHeight: 280,
                lineHeight: 1.5,
                fontFamily: '"Cascadia Code", "Fira Code", "Consolas", monospace',
              }}>
                {att.content}
              </pre>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
