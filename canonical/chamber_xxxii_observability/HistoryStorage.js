/**
 * Persistent storage for Type IV detector
 * Handles localStorage, indexedDB, or server backends
 */

export class HistoryStorage {
  constructor(backend = 'localStorage') {
    this.backend = backend;
    this.key = 'chamber_xxxii_run_history';
    
    if (backend === 'localStorage' && typeof localStorage === 'undefined') {
      console.warn('[HistoryStorage] localStorage unavailable, using memory');
      this.backend = 'memory';
      this.memoryStore = [];
    }
  }
  
  loadHistory() {
    try {
      if (this.backend === 'localStorage') {
        const stored = localStorage.getItem(this.key);
        return stored ? JSON.parse(stored) : [];
      } else if (this.backend === 'memory') {
        return this.memoryStore || [];
      }
    } catch (error) {
      console.error('[HistoryStorage] Load failed:', error);
      return [];
    }
  }
  
  saveHistory(history) {
    try {
      if (this.backend === 'localStorage') {
        localStorage.setItem(this.key, JSON.stringify(history));
      } else if (this.backend === 'memory') {
        this.memoryStore = history;
      }
    } catch (error) {
      console.error('[HistoryStorage] Save failed:', error);
    }
  }
}