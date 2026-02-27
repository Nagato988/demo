import type { Message, ScenarioStatusChange } from '../types'

export interface AgentEvent {
  type: 'message' | 'status'
  message?: Omit<Message, 'id' | 'timestamp'>
  status?: ScenarioStatusChange
}

/**
 * AgentAdapter — the only interface the UI depends on.
 * Swap implementations without touching any component.
 */
export interface AgentAdapter {
  sendToClaude(message: string): void
  sendToCodex(message: string): void
  onEvent(callback: (event: AgentEvent) => void): void
  offEvent(callback: (event: AgentEvent) => void): void
}
