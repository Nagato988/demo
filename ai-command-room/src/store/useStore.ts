import { create } from 'zustand'
import type { Message, ClaudeStatus, CodexStatus, BossStatus, UsageInfo } from '../types'
import { MockAdapter } from '../adapters/MockAdapter'
import type { AgentAdapter } from '../adapters/AgentAdapter'

// Swap MockAdapter for RealAdapter here when integrating real agents.
const adapter: AgentAdapter = new MockAdapter()

interface Store {
  messages: Message[]
  claudeStatus: ClaudeStatus
  codexStatus: CodexStatus
  bossStatus: BossStatus
  usage: UsageInfo

  addMessage: (msg: Omit<Message, 'id' | 'timestamp'>) => void
  setClaudeStatus: (s: ClaudeStatus) => void
  setCodexStatus: (s: CodexStatus) => void
  setBossStatus: (s: BossStatus) => void
  setUsage: (u: Partial<UsageInfo>) => void
  sendCommand: (text: string) => void
}

export const useStore = create<Store>((set, get) => {
  adapter.onEvent(event => {
    if (event.type === 'status' && event.status) {
      const s = event.status
      if (s.claude) get().setClaudeStatus(s.claude)
      if (s.codex) get().setCodexStatus(s.codex)
      if (s.boss) get().setBossStatus(s.boss)
    }
    if (event.type === 'message' && event.message) {
      get().addMessage(event.message)
    }
  })

  return {
    messages: [],
    claudeStatus: 'IDLE',
    codexStatus: 'WAITING',
    bossStatus: 'IDLE',
    usage: {
      claudeTokens: '~12k / 200k',
      codexContextLeft: '~85%',
    },

    addMessage: (msg) => {
      const message: Message = {
        ...msg,
        id: crypto.randomUUID(),
        timestamp: new Date().toLocaleTimeString(),
      }
      set(state => ({ messages: [...state.messages, message] }))
    },

    setClaudeStatus: (s) => set({ claudeStatus: s }),
    setCodexStatus: (s) => set({ codexStatus: s }),
    setBossStatus: (s) => set({ bossStatus: s }),
    setUsage: (u) => set(state => ({ usage: { ...state.usage, ...u } })),

    sendCommand: (text) => {
      get().addMessage({ role: 'Boss', type: 'COMMAND', content: text })
      get().setBossStatus('IDLE')
      adapter.sendToClaude(text)
    },
  }
})
