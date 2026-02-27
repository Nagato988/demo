import { contextBridge } from 'electron'

// Minimal preload — renderer is pure React, no Node IPC needed for MVP.
// Add ipcRenderer bindings here when integrating real agent adapters.
contextBridge.exposeInMainWorld('versions', {
  node: () => process.versions.node,
  electron: () => process.versions.electron,
})
