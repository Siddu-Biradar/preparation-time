/**
 * JS Notes — Inline Notes Injector
 * Automatically adds a notes editor below each <h2 id="..."> section in any JS phase file.
 * Include this script at the bottom of any phase HTML to get per-section notes.
 *
 * Persistence: localStorage + optional server (port 5502)
 */
(function() {
  'use strict';

  const NOTES_PREFIX = 'js-notes-';
  const NOTES_API = 'http://localhost:5502/api/notes';
  let serverAvailable = false;
  let fileNotes = {};
  const dirtyEditors = new Set();
  const autoSaveTimers = {};

  // Derive phase number from filename
  const pagePath = location.pathname;
  const phaseMatch = pagePath.match(/phase(\d+)/);
  const phaseNum = phaseMatch ? phaseMatch[1] : '0';

  // ===== INJECT CSS =====
  const style = document.createElement('style');
  style.textContent = `
    .jn-toggle-btn {
      display: inline-flex; align-items: center; gap: 4px;
      border: 1px solid #b3d4e8; background: #d6eaf8; color: #1a5276;
      padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;
      font-family: "Avenir Next", "Helvetica Neue", Helvetica, Arial, sans-serif;
      cursor: pointer; margin-left: 12px; transition: all 0.15s;
      vertical-align: middle;
    }
    .jn-toggle-btn:hover { background: #aed6f1; transform: scale(1.03); }
    .jn-toggle-btn.active { background: #1a5276; color: #fff; border-color: #1a5276; }
    .jn-toggle-btn.has-notes { background: #d4edda; color: #1b7340; border-color: #b7e4c7; }
    .jn-toggle-btn.has-notes.active { background: #1b7340; color: #fff; border-color: #1b7340; }

    .jn-notes-panel {
      display: none; margin: 12px 0 18px; padding: 14px 16px;
      background: #fefdfb; border: 1px solid #d8d0c3; border-radius: 10px;
      box-shadow: 0 2px 6px rgba(26,37,48,0.05);
    }
    .jn-notes-panel.open { display: block; animation: jnSlide 0.15s ease-out; }
    @keyframes jnSlide { from { opacity:0; transform: translateY(-6px); } to { opacity:1; transform: translateY(0); } }

    .jn-toolbar {
      display: flex; align-items: center; flex-wrap: wrap; gap: 4px;
      padding: 5px 8px; background: #f3efe7; border: 1px solid #d8d0c3;
      border-radius: 6px; margin-bottom: 8px;
    }
    .jn-toolbar button {
      border: none; background: transparent; cursor: pointer;
      padding: 3px 7px; border-radius: 4px; font-size: 12px; color: #1d1d1b;
      transition: background 0.1s;
    }
    .jn-toolbar button:hover { background: #e8e2d6; }
    .jn-toolbar .jn-sep { width: 1px; height: 16px; background: #d8d0c3; margin: 0 3px; }
    .jn-toolbar label { font-size: 10px; color: #5c584f; font-weight: 700; margin-right: 2px; }
    .jn-toolbar .jn-color-btn {
      width: 16px; height: 16px; border-radius: 50%; border: 2px solid #fff;
      box-shadow: 0 0 0 1px #d8d0c3; padding: 0; cursor: pointer;
    }

    .jn-editor {
      min-height: 80px; max-height: 350px; overflow-y: auto;
      padding: 10px 12px; border: 1px solid #d8d0c3; border-radius: 6px;
      background: #fff; font-size: 13px; line-height: 1.55;
      font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
      outline: none; transition: border-color 0.15s;
    }
    .jn-editor:focus { border-color: #1a5276; }
    .jn-editor:empty::before {
      content: attr(data-placeholder); color: #b8b0a0; font-style: italic;
    }

    .jn-footer {
      display: flex; align-items: center; gap: 6px; margin-top: 6px;
    }
    .jn-footer .jn-status { font-size: 11px; flex: 1; }
    .jn-footer button {
      border: none; padding: 4px 10px; border-radius: 5px;
      font-size: 11px; font-weight: 700; cursor: pointer; transition: background 0.15s;
    }
    .jn-footer .jn-save { background: #d4edda; color: #1b7340; }
    .jn-footer .jn-save:hover { background: #b7e4c7; }
    .jn-footer .jn-clear { background: #f8d7da; color: #721c24; }
    .jn-footer .jn-clear:hover { background: #f5c6cb; }

    /* Server indicator */
    .jn-server-badge {
      position: fixed; bottom: 12px; right: 12px; z-index: 999;
      font-size: 11px; padding: 4px 10px; border-radius: 999px;
      font-weight: 700; font-family: "Avenir Next", sans-serif;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .jn-server-badge.connected { background: #d4edda; color: #1b7340; }
    .jn-server-badge.disconnected { background: #f8d7da; color: #721c24; }
  `;
  document.head.appendChild(style);

  // ===== SERVER =====
  async function checkServer() {
    try {
      const res = await fetch(NOTES_API, { method: 'GET', signal: AbortSignal.timeout(1000) });
      if (res.ok) { serverAvailable = true; fileNotes = await res.json(); return; }
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
    } catch(e) {}
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
  function getSlug(sectionId) { return `phase${phaseNum}-${sectionId}`; }
  function getNoteContent(noteSlug) { return fileNotes[noteSlug] || localStorage.getItem(NOTES_PREFIX + noteSlug) || ''; }

  function saveNotes(noteSlug) {
    const editor = document.getElementById('jn-editor-' + noteSlug);
    const statusEl = document.getElementById('jn-status-' + noteSlug);
    if (!editor) return;
    const content = editor.innerHTML;
    if (content && content.trim() && content !== '<br>') {
      localStorage.setItem(NOTES_PREFIX + noteSlug, content);
      saveToServer(noteSlug, content);
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
    const editor = document.getElementById('jn-editor-' + noteSlug);
    if (!editor) return;
    const content = editor.innerHTML;
    if (content && content.trim() && content !== '<br>') {
      localStorage.setItem(NOTES_PREFIX + noteSlug, content);
      if (dirtyEditors.has(noteSlug)) saveToServer(noteSlug, content);
    }
    dirtyEditors.delete(noteSlug);
  }

  function clearNotes(noteSlug) {
    if (!confirm('Clear notes for this section?')) return;
    const editor = document.getElementById('jn-editor-' + noteSlug);
    editor.innerHTML = '';
    localStorage.removeItem(NOTES_PREFIX + noteSlug);
    delete fileNotes[noteSlug];
    deleteFromServer(noteSlug);
    dirtyEditors.delete(noteSlug);
    const statusEl = document.getElementById('jn-status-' + noteSlug);
    statusEl.textContent = '🗑️ Cleared';
    statusEl.style.color = '#721c24';
    setTimeout(() => { statusEl.textContent = ''; }, 2000);
    updateBtnState(noteSlug);
  }

  function autoSaveNotes(noteSlug) {
    dirtyEditors.add(noteSlug);
    clearTimeout(autoSaveTimers[noteSlug]);
    const statusEl = document.getElementById('jn-status-' + noteSlug);
    if (statusEl) { statusEl.textContent = 'typing...'; statusEl.style.color = '#5c584f'; }
    autoSaveTimers[noteSlug] = setTimeout(() => saveNotes(noteSlug), 800);
  }

  function toggleNotes(noteSlug) {
    const panel = document.getElementById('jn-panel-' + noteSlug);
    const btn = document.getElementById('jn-btn-' + noteSlug);
    const editor = document.getElementById('jn-editor-' + noteSlug);
    if (panel.classList.contains('open')) {
      if (dirtyEditors.has(noteSlug)) saveNotesQuiet(noteSlug);
      panel.classList.remove('open');
      btn.classList.remove('active');
    } else {
      panel.classList.add('open');
      btn.classList.add('active');
      const saved = getNoteContent(noteSlug);
      if (saved && !editor.innerHTML.trim()) editor.innerHTML = saved;
      editor.focus();
    }
  }

  function updateBtnState(noteSlug) {
    const btn = document.getElementById('jn-btn-' + noteSlug);
    if (!btn) return;
    const content = getNoteContent(noteSlug);
    if (content && content.trim() && content !== '<br>') {
      btn.classList.add('has-notes');
    } else {
      btn.classList.remove('has-notes');
    }
  }

  // Rich text
  function fmtBold() { document.execCommand('bold', false, null); }
  function fmtItalic() { document.execCommand('italic', false, null); }
  function fmtUnderline() { document.execCommand('underline', false, null); }
  function fmtColor(noteSlug, color) {
    const ed = document.getElementById('jn-editor-' + noteSlug);
    ed.focus(); document.execCommand('foreColor', false, color);
    dirtyEditors.add(noteSlug); setTimeout(() => saveNotesQuiet(noteSlug), 100);
  }
  function fmtHighlight(noteSlug, color) {
    const ed = document.getElementById('jn-editor-' + noteSlug);
    ed.focus(); document.execCommand('hiliteColor', false, color);
    dirtyEditors.add(noteSlug); setTimeout(() => saveNotesQuiet(noteSlug), 100);
  }
  function fmtRemove(noteSlug) {
    const ed = document.getElementById('jn-editor-' + noteSlug);
    ed.focus(); document.execCommand('removeFormat', false, null);
    dirtyEditors.add(noteSlug); setTimeout(() => saveNotesQuiet(noteSlug), 100);
  }

  // ===== INJECT PANELS =====
  function injectNotesPanels() {
    const h2s = document.querySelectorAll('h2[id]');
    h2s.forEach(h2 => {
      const sectionId = h2.id;
      const noteSlug = getSlug(sectionId);

      // Add toggle button to h2
      const btn = document.createElement('button');
      btn.className = 'jn-toggle-btn';
      btn.id = 'jn-btn-' + noteSlug;
      btn.textContent = '📝 Notes';
      btn.onclick = () => toggleNotes(noteSlug);
      h2.appendChild(btn);

      // Create panel
      const panel = document.createElement('div');
      panel.className = 'jn-notes-panel';
      panel.id = 'jn-panel-' + noteSlug;
      panel.innerHTML = `
        <div class="jn-toolbar">
          <button onclick="window._jn.fmtBold()" title="Bold"><b>B</b></button>
          <button onclick="window._jn.fmtItalic()" title="Italic"><i>I</i></button>
          <button onclick="window._jn.fmtUnderline()" title="Underline"><u>U</u></button>
          <span class="jn-sep"></span>
          <label>Text:</label>
          <button class="jn-color-btn" style="background:#e74c3c" onclick="window._jn.fmtColor('${noteSlug}','#e74c3c')" title="Red"></button>
          <button class="jn-color-btn" style="background:#27ae60" onclick="window._jn.fmtColor('${noteSlug}','#27ae60')" title="Green"></button>
          <button class="jn-color-btn" style="background:#2980b9" onclick="window._jn.fmtColor('${noteSlug}','#2980b9')" title="Blue"></button>
          <button class="jn-color-btn" style="background:#8e44ad" onclick="window._jn.fmtColor('${noteSlug}','#8e44ad')" title="Purple"></button>
          <span class="jn-sep"></span>
          <label>Highlight:</label>
          <button class="jn-color-btn" style="background:#fff176" onclick="window._jn.fmtHighlight('${noteSlug}','#fff176')" title="Yellow"></button>
          <button class="jn-color-btn" style="background:#aed581" onclick="window._jn.fmtHighlight('${noteSlug}','#aed581')" title="Green"></button>
          <button class="jn-color-btn" style="background:#81d4fa" onclick="window._jn.fmtHighlight('${noteSlug}','#81d4fa')" title="Blue"></button>
          <span class="jn-sep"></span>
          <button onclick="window._jn.fmtRemove('${noteSlug}')" title="Remove formatting">✖</button>
        </div>
        <div class="jn-editor" id="jn-editor-${noteSlug}" contenteditable="true"
             data-placeholder="Add your notes for this section..."
             oninput="window._jn.autoSaveNotes('${noteSlug}')"></div>
        <div class="jn-footer">
          <span class="jn-status" id="jn-status-${noteSlug}"></span>
          <button class="jn-save" onclick="window._jn.saveNotes('${noteSlug}')">💾 Save</button>
          <button class="jn-clear" onclick="window._jn.clearNotes('${noteSlug}')">🗑️ Clear</button>
        </div>
      `;
      // Insert panel after h2
      h2.parentNode.insertBefore(panel, h2.nextSibling);
    });
  }

  // ===== SAVE ALL ON CLOSE =====
  function saveAllDirty() {
    if (dirtyEditors.size === 0) return;
    const bulk = {};
    dirtyEditors.forEach(noteSlug => {
      const editor = document.getElementById('jn-editor-' + noteSlug);
      if (editor) {
        const content = editor.innerHTML;
        if (content && content.trim() && content !== '<br>') {
          localStorage.setItem(NOTES_PREFIX + noteSlug, content);
          bulk[noteSlug] = content;
        }
      }
    });
    if (serverAvailable && Object.keys(bulk).length > 0) {
      const blob = new Blob([JSON.stringify(bulk)], { type: 'application/json' });
      navigator.sendBeacon(NOTES_API + '/bulk', blob);
    }
    dirtyEditors.clear();
  }

  // ===== SERVER BADGE =====
  function showServerBadge() {
    const badge = document.createElement('div');
    badge.className = 'jn-server-badge ' + (serverAvailable ? 'connected' : 'disconnected');
    badge.textContent = serverAvailable ? '● Notes: Server' : '● Notes: Local';
    document.body.appendChild(badge);
    // Auto-hide after 3s
    setTimeout(() => { badge.style.opacity = '0.4'; }, 3000);
  }

  // ===== INIT =====
  async function init() {
    await checkServer();
    injectNotesPanels();

    // Load existing notes
    document.querySelectorAll('h2[id]').forEach(h2 => {
      const noteSlug = getSlug(h2.id);
      const content = getNoteContent(noteSlug);
      if (content) {
        const editor = document.getElementById('jn-editor-' + noteSlug);
        if (editor) editor.innerHTML = content;
        updateBtnState(noteSlug);
      }
    });

    showServerBadge();
  }

  // Expose functions for inline onclick handlers
  window._jn = {
    fmtBold, fmtItalic, fmtUnderline, fmtColor, fmtHighlight, fmtRemove,
    saveNotes, clearNotes, autoSaveNotes, toggleNotes
  };

  // Events
  window.addEventListener('beforeunload', saveAllDirty);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') saveAllDirty(); });
  window.addEventListener('pagehide', saveAllDirty);

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
