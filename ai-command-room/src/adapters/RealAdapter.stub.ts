import type { AgentAdapter, AgentEvent } from './AgentAdapter'

/**
 * RealAdapter — stub for future real integration.
 *
 * Integration options (implement one per agent):
 *
 * Claude:
 *   A) CLI  — spawn child_process: execFile('claude', ['--message', msg], callback)
 *   B) API  — POST https://api.anthropic.com/v1/messages with ANTHROPIC_API_KEY from env/keychain
 *
 * Codex:
 *   A) tmux — reuse bridge.sh: execFile('./bridge.sh', [msg], callback)
 *   B) API  — POST OpenAI Codex API with OPENAI_API_KEY from env/keychain
 *
 * Steps:
 *   1. Implement sendToClaude / sendToCodex below
 *   2. Parse responses and call this.emit({ type: 'message', message: {...} })
 *   3. In store/useStore.ts, replace `new MockAdapter()` with `new RealAdapter()`
 */
export class RealAdapter implements AgentAdapter {
  private listeners: Set<(event: AgentEvent) => void> = new Set()

  sendToClaude(_message: string): void {
    // TODO: implement
    throw new Error('RealAdapter.sendToClaude not implemented')
  }

  sendToCodex(_message: string): void {
    // TODO: implement
    throw new Error('RealAdapter.sendToCodex not implemented')
  }

  onEvent(callback: (event: AgentEvent) => void): void {
    this.listeners.add(callback)
  }

  offEvent(callback: (event: AgentEvent) => void): void {
    this.listeners.delete(callback)
  }

  protected emit(event: AgentEvent): void {
    this.listeners.forEach(cb => cb(event))
  }
}
