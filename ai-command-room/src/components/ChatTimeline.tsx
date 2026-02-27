import { useEffect, useRef } from 'react'
import { useStore } from '../store/useStore'
import { MessageCard } from './MessageCard'

export function ChatTimeline() {
  const messages = useStore(s => s.messages)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages.length])

  return (
    <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
      {messages.length === 0 && (
        <div style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 12,
          color: '#484f58',
        }}>
          <div style={{ fontSize: 32 }}>⚡</div>
          <div style={{ fontSize: 14 }}>AI Command Room is ready.</div>
          <div style={{ fontSize: 12 }}>Send a command below to begin the demo scenario.</div>
        </div>
      )}
      {messages.map(msg => (
        <MessageCard key={msg.id} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  )
}
