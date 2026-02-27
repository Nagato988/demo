export type Role = 'Boss' | 'Claude' | 'Codex' | 'System'

export type MessageType =
  | 'COMMAND'
  | 'PLAN'
  | 'ROUTING'
  | 'REVIEW'
  | 'DECISION'
  | 'QUALITY_GATE'
  | 'EXECUTION'
  | 'DIFF'
  | 'OUTPUT'
  | 'ERROR'
  | 'OVERRIDE'
  | 'SYSTEM'

export type ClaudeStatus = 'IDLE' | 'PLANNING' | 'REVIEWING' | 'ESCALATED'
export type CodexStatus = 'WORKING' | 'WAITING' | 'BLOCKED'
export type BossStatus = 'IDLE' | 'DECIDING'

export interface Attachment {
  type: 'diff' | 'log' | 'filelist'
  label: string
  content: string
}

export interface Message {
  id: string
  role: Role
  type: MessageType
  timestamp: string
  content: string
  attachments?: Attachment[]
}

export interface UsageInfo {
  claudeTokens: string
  codexContextLeft: string
}

// Scenario JSON types
export interface ScenarioStatusChange {
  claude?: ClaudeStatus
  codex?: CodexStatus
  boss?: BossStatus
}

export interface ScenarioEvent {
  delay: number
  status?: ScenarioStatusChange
  message?: {
    role: Role
    type: MessageType
    content: string
    attachments?: Attachment[]
  }
}
