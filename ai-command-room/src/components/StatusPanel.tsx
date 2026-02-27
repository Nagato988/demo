import { useState } from 'react'
import { useStore } from '../store/useStore'
import type { ClaudeStatus, CodexStatus, BossStatus, UsageInfo } from '../types'

const CLAUDE_COLOR: Record<ClaudeStatus, string> = {
  IDLE:      '#484f58',
  PLANNING:  '#7ee787',
  REVIEWING: '#4dd0e1',
  ESCALATED: '#f85149',
}

const CODEX_COLOR: Record<CodexStatus, string> = {
  WAITING: '#484f58',
  WORKING: '#ffb74d',
  BLOCKED: '#f85149',
}

const BOSS_COLOR: Record<BossStatus, string> = {
  IDLE:     '#484f58',
  DECIDING: '#58a6ff',
}

function Dot({ color }: { color: string }) {
  const active = color !== '#484f58'
  return (
    <span style={{
      display: 'inline-block',
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: color,
      boxShadow: active ? `0 0 7px ${color}` : 'none',
      flexShrink: 0,
    }} />
  )
}

function StatusRow({
  emoji, name, statusLabel, color,
}: { emoji: string; name: string; statusLabel: string; color: string }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
        <span style={{ fontSize: 16 }}>{emoji}</span>
        <span style={{ color: '#c9d1d9', fontSize: 13, fontWeight: 600 }}>{name}</span>
      </div>
      <div style={{ paddingLeft: 23, display: 'flex', alignItems: 'center', gap: 6 }}>
        <Dot color={color} />
        <span style={{ color, fontSize: 11, fontWeight: 700, letterSpacing: '0.06em' }}>
          {statusLabel}
        </span>
      </div>
    </div>
  )
}

function UsageStat({ label, value, field }: {
  label: string
  value: string
  field: keyof UsageInfo
}) {
  const setUsage = useStore(s => s.setUsage)
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(value)

  const commit = () => {
    setUsage({ [field]: draft } as Partial<UsageInfo>)
    setEditing(false)
  }

  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ fontSize: 11, color: '#484f58', marginBottom: 3 }}>{label}</div>
      {editing ? (
        <input
          value={draft}
          onChange={e => setDraft(e.target.value)}
          onBlur={commit}
          onKeyDown={e => { if (e.key === 'Enter') commit() }}
          autoFocus
          style={{
            background: '#0d1117',
            border: '1px solid #58a6ff',
            borderRadius: 4,
            color: '#c9d1d9',
            fontSize: 12,
            padding: '2px 7px',
            width: '100%',
            outline: 'none',
            fontFamily: 'inherit',
          }}
        />
      ) : (
        <div
          onClick={() => { setDraft(value); setEditing(true) }}
          title="Click to edit"
          style={{
            color: '#8b949e',
            fontSize: 12,
            cursor: 'text',
            padding: '1px 0',
          }}
        >
          {value}
        </div>
      )}
    </div>
  )
}

export function StatusPanel() {
  const { claudeStatus, codexStatus, bossStatus, usage } = useStore()

  return (
    <div style={{
      width: 220,
      background: '#161b22',
      borderLeft: '1px solid #21262d',
      padding: '16px 14px',
      display: 'flex',
      flexDirection: 'column',
      gap: 18,
      overflowY: 'auto',
      flexShrink: 0,
    }}>
      <div style={{
        fontSize: 10,
        fontWeight: 700,
        color: '#484f58',
        letterSpacing: '0.12em',
        textTransform: 'uppercase',
      }}>
        Agent Status
      </div>

      <StatusRow emoji="🧑‍💼" name="Boss"   statusLabel={bossStatus}   color={BOSS_COLOR[bossStatus]} />
      <StatusRow emoji="🧠"   name="Claude" statusLabel={claudeStatus} color={CLAUDE_COLOR[claudeStatus]} />
      <StatusRow emoji="⚙️"   name="Codex"  statusLabel={codexStatus}  color={CODEX_COLOR[codexStatus]} />

      <div style={{ borderTop: '1px solid #21262d', paddingTop: 14 }}>
        <div style={{
          fontSize: 10,
          fontWeight: 700,
          color: '#484f58',
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          marginBottom: 12,
        }}>
          Usage / Context
        </div>
        <UsageStat label="Claude tokens"   value={usage.claudeTokens}    field="claudeTokens" />
        <UsageStat label="Codex ctx left"  value={usage.codexContextLeft} field="codexContextLeft" />
        <div style={{ fontSize: 10, color: '#30363d', marginTop: 4 }}>
          Click values to edit
        </div>
      </div>

      <div style={{ borderTop: '1px solid #21262d', paddingTop: 14 }}>
        <div style={{ fontSize: 10, fontWeight: 700, color: '#484f58', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 10 }}>
          Hierarchy
        </div>
        {[
          { emoji: '🧑‍💼', label: 'Boss — final authority' },
          { emoji: '🧠', label: 'Claude — manager' },
          { emoji: '⚙️', label: 'Codex — executor' },
        ].map(({ emoji, label }) => (
          <div key={label} style={{ display: 'flex', gap: 7, marginBottom: 6, fontSize: 11, color: '#484f58' }}>
            <span>{emoji}</span>
            <span>{label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
