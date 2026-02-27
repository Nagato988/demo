import type { AgentAdapter, AgentEvent } from './AgentAdapter'
import type { ScenarioEvent } from '../types'
import scenarioData from '../scenarios/demo.json'

const scenario = scenarioData as ScenarioEvent[]

export class MockAdapter implements AgentAdapter {
  private listeners: Set<(event: AgentEvent) => void> = new Set()
  private running = false

  /** Called when Boss sends a command. Triggers the scripted scenario. */
  sendToClaude(_message: string): void {
    if (this.running) return
    this.runScenario()
  }

  /** In mock mode Codex is driven by the scenario; this is a no-op. */
  sendToCodex(_message: string): void {}

  onEvent(callback: (event: AgentEvent) => void): void {
    this.listeners.add(callback)
  }

  offEvent(callback: (event: AgentEvent) => void): void {
    this.listeners.delete(callback)
  }

  private emit(event: AgentEvent): void {
    this.listeners.forEach(cb => cb(event))
  }

  private async runScenario(): Promise<void> {
    this.running = true
    for (const event of scenario) {
      await this.sleep(event.delay)
      if (event.status) {
        this.emit({ type: 'status', status: event.status })
      }
      if (event.message) {
        this.emit({ type: 'message', message: event.message })
      }
    }
    this.running = false
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}
