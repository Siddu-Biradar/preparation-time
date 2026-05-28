/**
 * FSD Notes — Inline Notes Injector for Frontend System Design
 * Automatically adds a notes editor below each <h2 id="..."> section in any phase file.
 * Include this script at the bottom of any phase HTML to get per-section notes.
 *
 * Persistence: localStorage (primary) + optional server (port 5503)
 * Data safety: Notes are ONLY written on explicit Save click or auto-save after 2s idle.
 *              Notes are NEVER erased unless user clicks Clear.
 *              On page load, notes load from server first (if available), then localStorage fallback.
 */
(function() {
  'use strict';

  const NOTES_PREFIX = 'fsd-notes-';
  const NOTES_API = 'http://localhost:5503/api/notes';
  let serverAvailable = false;
  let serverNotes = {};
  const dirtyEditors = new Set();
  const autoSaveTimers = {};

  // Derive phase from filename: phase1-fundamentals-architecture.html → "phase1"
  const pagePath = location.pathname;
  const phaseMatch = pagePath.match(/(phase\d+)/);
  const phaseKey = phaseMatch ? phaseMatch[1] : 'fsd';

  // ===== INJECT CSS =====
  const style = document.createElement('style');
  style.textContent = `
    .fsd-toggle-btn {
      display: inline-flex; align-items: center; gap: 4px;
      border: 1px solid #b3d4e8; background: #e8f4fd; color: #1a5276;
      padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;
      font-family: "Inter", "Segoe UI", sans-serif;
      cursor: pointer; margin-left: 12px; transition: all 0.15s;
      vertical-align: middle;
    }
    .fsd-toggle-btn:hover { background: #aed6f1; transform: scale(1.03); }
    .fsd-toggle-btn.active { background: #1a5276; color: #fff; border-color: #1a5276; }
    .fsd-toggle-btn.has-notes { background: #d4edda; color: #1b7340; border-color: #b7e4c7; }
    .fsd-toggle-btn.has-notes.active { background: #1b7340; color: #fff; border-color: #1b7340; }

    .fsd-notes-panel {
      display: none; margin: 12px 0 18px; padding: 14px 16px;
      background: #fefdfb; border: 1px solid #d8d0c3; border-radius: 10px;
      box-shadow: 0 2px 6px rgba(26,37,48,0.05);
    }
    .fsd-notes-panel.open { display: block; animation: fsdSlide 0.15s ease-out; }
    @keyframes fsdSlide { from { opacity:0; transform: translateY(-6px); } to { opacity:1; transform: translateY(0); } }

    .fsd-toolbar {
      display: flex; align-items: center; flex-wrap: wrap; gap: 4px;
      padding: 5px 8px; background: #f3efe7; border: 1px solid #d8d0c3;
      border-radius: 6px; margin-bottom: 8px;
    }
    .fsd-toolbar button {
      border: none; background: transparent; cursor: pointer;
      padding: 3px 7px; border-radius: 4px; font-size: 12px; color: #1d1d1b;
      transition: background 0.1s;
    }
    .fsd-toolbar button:hover { background: #e8e2d6; }
    .fsd-toolbar .fsd-sep { width: 1px; height: 16px; background: #d8d0c3; margin: 0 3px; }
    .fsd-toolbar label { font-size: 10px; color: #5c584f; font-weight: 700; margin-right: 2px; }
    .fsd-toolbar .fsd-color-btn {
      width: 16px; height: 16px; border-radius: 50%; border: 2px solid #fff;
      box-shadow: 0 0 0 1px #d8d0c3; padding: 0; cursor: pointer;
    }

    .fsd-editor {
      min-height: 80px; max-height: 400px; overflow-y: auto;
      padding: 10px 12px; border: 1px solid #d8d0c3; border-radius: 6px;
      background: #fff; font-size: 13px; line-height: 1.55;
      font-family: "JetBrains Mono", "SF Mono", Menlo, monospace;
      outline: none; transition: border-color 0.15s;
    }
    .fsd-editor:focus { border-color: #0f9d7a; }
    .fsd-editor:empty::before {
      content: attr(data-placeholder); color: #b8b0a0; font-style: italic;
    }

    .fsd-footer {
      display: flex; align-items: center; gap: 6px; margin-top: 6px;
    }
    .fsd-footer .fsd-status { font-size: 11px; flex: 1; }
    .fsd-footer button {
      border: none; padding: 4px 10px; border-radius: 5px;
      font-size: 11px; font-weight: 700; cursor: pointer; transition: background 0.15s;
    }
    .fsd-footer .fsd-save { background: #d4edda; color: #1b7340; }
    .fsd-footer .fsd-save:hover { background: #b7e4c7; }
    .fsd-footer .fsd-clear { background: #f8d7da; color: #721c24; }
    .fsd-footer .fsd-clear:hover { background: #f5c6cb; }

    /* Server indicator */
    .fsd-server-badge {
      position: fixed; bottom: 12px; right: 12px; z-index: 999;
      font-size: 11px; padding: 4px 10px; border-radius: 999px;
      font-weight: 700; font-family: "Inter", sans-serif;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .fsd-server-badge.connected { background: #d4edda; color: #1b7340; }
    .fsd-server-badge.disconnected { background: #fdf5e8; color: #b26b00; }
  `;
  document.head.appendChild(style);

  // ===== SERVER COMMUNICATION =====
  async function checkServer() {
    try {
      const res = await fetch(NOTES_API, { method: 'GET', signal: AbortSignal.timeout(1500) });
      if (res.ok) { serverAvailable = true; serverNotes = await res.json(); return; }
    } catch(e) {}
    serverAvailable = false;
  }

  async function saveToServer(noteSlug, content) {
    if (!serverAvailable) return;
    try {
      await fetch(NOTES_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug: noteSlug, content })
      });
    } catch(e) { /* fail silently, localStorage is primary */ }
  }

  async function deleteFromServer(noteSlug) {
    if (!serverAvailable) return;
    try {
      await fetch(NOTES_API + '/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug: noteSlug })
      });
    } catch(e) {}
  }

  // ===== NOTES LOGIC =====
  function getSlug(sectionId) { return `${phaseKey}-${sectionId}`; }

  function getNoteContent(noteSlug) {
    // Server data takes priority (it's the "source of truth" when available)
    if (serverNotes[noteSlug]) return serverNotes[noteSlug];
    return localStorage.getItem(NOTES_PREFIX + noteSlug) || '';
  }

  function saveNotes(noteSlug) {
    const editor = document.getElementById('fsd-editor-' + noteSlug);
    const statusEl = document.getElementById('fsd-status-' + noteSlug);
    if (!editor) return;
    const content = editor.innerHTML;
    if (content && content.trim() && content !== '<br>') {
      localStorage.setItem(NOTES_PREFIX + noteSlug, content);
      saveToServer(noteSlug, content);
      serverNotes[noteSlug] = content; // Update local cache
    }
    dirtyEditors.delete(noteSlug);
    if (statusEl) {
      statusEl.textContent = '✓ Saved!';
      statusEl.style.color = '#1b7340';
      setTimeout(() => { statusEl.textContent = ''; }, 2000);
    }
    updateBtnState(noteSlug);
  }

  function saveNotesQuiet(noteSlug) {
    const editor = document.getElementById('fsd-editor-' + noteSlug);
    if (!editor) return;
    const content = editor.innerHTML;
    if (content && content.trim() && content !== '<br>') {
      localStorage.setItem(NOTES_PREFIX + noteSlug, content);
      if (dirtyEditors.has(noteSlug)) saveToServer(noteSlug, content);
      serverNotes[noteSlug] = content;
    }
    dirtyEditors.delete(noteSlug);
  }

  function clearNotes(noteSlug) {
    if (!confirm('Clear notes for this section? This cannot be undone.')) return;
    const editor = document.getElementById('fsd-editor-' + noteSlug);
    editor.innerHTML = '';
    localStorage.removeItem(NOTES_PREFIX + noteSlug);
    delete serverNotes[noteSlug];
    deleteFromServer(noteSlug);
    dirtyEditors.delete(noteSlug);
    const statusEl = document.getElementById('fsd-status-' + noteSlug);
    statusEl.textContent = '🗑️ Cleared';
    statusEl.style.color = '#721c24';
    setTimeout(() => { statusEl.textContent = ''; }, 2000);
    updateBtnState(noteSlug);
  }

  function autoSaveNotes(noteSlug) {
    dirtyEditors.add(noteSlug);
    clearTimeout(autoSaveTimers[noteSlug]);
    const statusEl = document.getElementById('fsd-status-' + noteSlug);
    if (statusEl) { statusEl.textContent = 'typing...'; statusEl.style.color = '#5c584f'; }
    // Auto-save after 2 seconds of idle (generous to prevent accidental loss)
    autoSaveTimers[noteSlug] = setTimeout(() => saveNotes(noteSlug), 2000);
  }

  function toggleNotes(noteSlug) {
    const panel = document.getElementById('fsd-panel-' + noteSlug);
    const btn = document.getElementById('fsd-btn-' + noteSlug);
    const editor = document.getElementById('fsd-editor-' + noteSlug);
    if (panel.classList.contains('open')) {
      // Save any unsaved changes before closing
      if (dirtyEditors.has(noteSlug)) saveNotesQuiet(noteSlug);
      panel.classList.remove('open');
      btn.classList.remove('active');
    } else {
      panel.classList.add('open');
      btn.classList.add('active');
      // Load saved content into editor
      const saved = getNoteContent(noteSlug);
      if (saved && !editor.innerHTML.trim()) editor.innerHTML = saved;
      editor.focus();
    }
  }

  function updateBtnState(noteSlug) {
    const btn = document.getElementById('fsd-btn-' + noteSlug);
    if (!btn) return;
    const content = getNoteContent(noteSlug);
    if (content && content.trim() && content !== '<br>') {
      btn.classList.add('has-notes');
    } else {
      btn.classList.remove('has-notes');
    }
  }

  // ===== RICH TEXT FORMATTING =====
  function fmtBold() { document.execCommand('bold', false, null); }
  function fmtItalic() { document.execCommand('italic', false, null); }
  function fmtUnderline() { document.execCommand('underline', false, null); }
  function fmtCode() {
    const sel = window.getSelection();
    if (sel.rangeCount) {
      const range = sel.getRangeAt(0);
      const code = document.createElement('code');
      code.style.cssText = 'background:#f1f4fa;padding:1px 4px;border-radius:3px;font-size:12px;';
      range.surroundContents(code);
    }
  }
  function fmtColor(noteSlug, color) {
    const ed = document.getElementById('fsd-editor-' + noteSlug);
    ed.focus(); document.execCommand('foreColor', false, color);
    dirtyEditors.add(noteSlug); setTimeout(() => saveNotesQuiet(noteSlug), 100);
  }
  function fmtHighlight(noteSlug, color) {
    const ed = document.getElementById('fsd-editor-' + noteSlug);
    ed.focus(); document.execCommand('hiliteColor', false, color);
    dirtyEditors.add(noteSlug); setTimeout(() => saveNotesQuiet(noteSlug), 100);
  }
  function fmtRemove(noteSlug) {
    const ed = document.getElementById('fsd-editor-' + noteSlug);
    ed.focus(); document.execCommand('removeFormat', false, null);
    dirtyEditors.add(noteSlug); setTimeout(() => saveNotesQuiet(noteSlug), 100);
  }

  // ===== INJECT NOTES PANELS =====
  function injectNotesPanels() {
    const h2s = document.querySelectorAll('main h2[id]');
    h2s.forEach(h2 => {
      const sectionId = h2.id;
      const noteSlug = getSlug(sectionId);

      // Toggle button
      const btn = document.createElement('button');
      btn.className = 'fsd-toggle-btn';
      btn.id = 'fsd-btn-' + noteSlug;
      btn.textContent = '📝 Notes';
      btn.onclick = () => toggleNotes(noteSlug);
      h2.appendChild(btn);

      // Notes panel
      const panel = document.createElement('div');
      panel.className = 'fsd-notes-panel';
      panel.id = 'fsd-panel-' + noteSlug;
      panel.innerHTML = `
        <div class="fsd-toolbar">
          <button onclick="window._fsd.fmtBold()" title="Bold"><b>B</b></button>
          <button onclick="window._fsd.fmtItalic()" title="Italic"><i>I</i></button>
          <button onclick="window._fsd.fmtUnderline()" title="Underline"><u>U</u></button>
          <button onclick="window._fsd.fmtCode()" title="Inline Code">&lt;/&gt;</button>
          <span class="fsd-sep"></span>
          <label>Text:</label>
          <button class="fsd-color-btn" style="background:#e74c3c" onclick="window._fsd.fmtColor('${noteSlug}','#e74c3c')" title="Red"></button>
          <button class="fsd-color-btn" style="background:#27ae60" onclick="window._fsd.fmtColor('${noteSlug}','#27ae60')" title="Green"></button>
          <button class="fsd-color-btn" style="background:#2a5bd7" onclick="window._fsd.fmtColor('${noteSlug}','#2a5bd7')" title="Blue"></button>
          <button class="fsd-color-btn" style="background:#8e44ad" onclick="window._fsd.fmtColor('${noteSlug}','#8e44ad')" title="Purple"></button>
          <span class="fsd-sep"></span>
          <label>Highlight:</label>
          <button class="fsd-color-btn" style="background:#fff176" onclick="window._fsd.fmtHighlight('${noteSlug}','#fff176')" title="Yellow"></button>
          <button class="fsd-color-btn" style="background:#aed581" onclick="window._fsd.fmtHighlight('${noteSlug}','#aed581')" title="Green"></button>
          <button class="fsd-color-btn" style="background:#81d4fa" onclick="window._fsd.fmtHighlight('${noteSlug}','#81d4fa')" title="Blue"></button>
          <span class="fsd-sep"></span>
          <button onclick="window._fsd.fmtRemove('${noteSlug}')" title="Remove formatting">✖</button>
        </div>
        <div class="fsd-editor" id="fsd-editor-${noteSlug}" contenteditable="true"
             data-placeholder="Add your notes, key points, interview answers..."
             oninput="window._fsd.autoSaveNotes('${noteSlug}')"></div>
        <div class="fsd-footer">
          <span class="fsd-status" id="fsd-status-${noteSlug}"></span>
          <button class="fsd-save" onclick="window._fsd.saveNotes('${noteSlug}')">💾 Save</button>
          <button class="fsd-clear" onclick="window._fsd.clearNotes('${noteSlug}')">🗑️ Clear</button>
        </div>
      `;
      h2.parentNode.insertBefore(panel, h2.nextSibling);
    });
  }

  // ===== SAVE ALL ON PAGE CLOSE (data safety) =====
  function saveAllDirty() {
    if (dirtyEditors.size === 0) return;
    const bulk = {};
    dirtyEditors.forEach(noteSlug => {
      const editor = document.getElementById('fsd-editor-' + noteSlug);
      if (editor) {
        const content = editor.innerHTML;
        if (content && content.trim() && content !== '<br>') {
          localStorage.setItem(NOTES_PREFIX + noteSlug, content);
          bulk[noteSlug] = content;
        }
      }
    });
    // Use sendBeacon for reliable delivery on page close
    if (serverAvailable && Object.keys(bulk).length > 0) {
      const blob = new Blob([JSON.stringify(bulk)], { type: 'application/json' });
      navigator.sendBeacon(NOTES_API + '/bulk', blob);
    }
    dirtyEditors.clear();
  }

  // ===== SERVER BADGE =====
  function showServerBadge() {
    const badge = document.createElement('div');
    badge.className = 'fsd-server-badge ' + (serverAvailable ? 'connected' : 'disconnected');
    badge.textContent = serverAvailable ? '● Notes: Server + Local' : '● Notes: LocalStorage';
    badge.title = serverAvailable
      ? 'Notes saved to server (persistent) + localStorage (fast)'
      : 'Notes saved to localStorage only. Run fsd-notes-server.py for file persistence.';
    document.body.appendChild(badge);
    setTimeout(() => { badge.style.opacity = '0.4'; }, 4000);
  }

  // ===== INIT =====
  async function init() {
    await checkServer();
    injectNotesPanels();

    // Pre-load existing notes & mark buttons
    document.querySelectorAll('main h2[id]').forEach(h2 => {
      const noteSlug = getSlug(h2.id);
      const content = getNoteContent(noteSlug);
      if (content) {
        const editor = document.getElementById('fsd-editor-' + noteSlug);
        if (editor) editor.innerHTML = content;
        updateBtnState(noteSlug);
      }
    });

    showServerBadge();
  }

  // Expose for inline onclick handlers
  window._fsd = {
    fmtBold, fmtItalic, fmtUnderline, fmtCode,
    fmtColor, fmtHighlight, fmtRemove,
    saveNotes, clearNotes, autoSaveNotes, toggleNotes
  };

  // Data safety events — save dirty editors on:
  window.addEventListener('beforeunload', saveAllDirty);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveAllDirty(); });
  window.addEventListener('pagehide', saveAllDirty);

  // Run
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
