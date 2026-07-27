/**
 * Inline Annotations — Figma-style text-level notes
 * Select any text → add a note/doubt right there.
 * Notes are persistent (localStorage), re-editable, color-supported.
 * 
 * Usage: Include this script at the bottom of any HTML page.
 */
(function() {
  'use strict';

  const STORAGE_KEY = 'inline-annotations-' + location.pathname;
  let annotations = loadAnnotations();
  let activePopup = null;
  let annotationIdCounter = annotations.length ? Math.max(...annotations.map(a => a.id)) + 1 : 1;

  // ===== STYLES =====
  const style = document.createElement('style');
  style.textContent = `
    /* Highlighted annotated text */
    .ia-highlight {
      background: rgba(255, 235, 59, 0.35);
      border-bottom: 2px solid #f39c12;
      cursor: pointer;
      position: relative;
      border-radius: 2px;
      transition: background 0.2s;
    }
    .ia-highlight:hover {
      background: rgba(255, 235, 59, 0.55);
    }
    .ia-highlight .ia-dot {
      display: inline-block;
      width: 8px; height: 8px;
      background: #e74c3c;
      border-radius: 50%;
      margin-left: 2px;
      vertical-align: super;
      font-size: 0;
      box-shadow: 0 0 0 2px rgba(231,76,60,0.3);
      animation: ia-pulse 2s infinite;
    }
    @keyframes ia-pulse {
      0%, 100% { box-shadow: 0 0 0 2px rgba(231,76,60,0.3); }
      50% { box-shadow: 0 0 0 5px rgba(231,76,60,0.1); }
    }

    /* Floating add-note button on text selection */
    .ia-add-btn {
      position: absolute;
      z-index: 10000;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff;
      border: none;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      font-family: "Avenir Next", "Helvetica Neue", sans-serif;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(102,126,234,0.4);
      transition: transform 0.15s, opacity 0.15s;
      opacity: 0;
      transform: translateY(4px);
      pointer-events: none;
    }
    .ia-add-btn.visible {
      opacity: 1;
      transform: translateY(0);
      pointer-events: all;
    }
    .ia-add-btn:hover {
      transform: translateY(-2px) scale(1.03);
      box-shadow: 0 6px 18px rgba(102,126,234,0.5);
    }

    /* Annotation popup/editor */
    .ia-popup {
      position: absolute;
      z-index: 10001;
      width: 340px;
      background: #fff;
      border: 1px solid #e0ddd6;
      border-radius: 12px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.15), 0 2px 8px rgba(0,0,0,0.08);
      font-family: "Avenir Next", "Helvetica Neue", sans-serif;
      animation: ia-popIn 0.2s ease-out;
      overflow: hidden;
    }
    @keyframes ia-popIn {
      from { opacity: 0; transform: translateY(-8px) scale(0.96); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .ia-popup-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
    }
    .ia-popup-header .ia-close-btn {
      background: rgba(255,255,255,0.2);
      border: none;
      color: #fff;
      width: 22px; height: 22px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.15s;
    }
    .ia-popup-header .ia-close-btn:hover { background: rgba(255,255,255,0.4); }

    .ia-popup-body {
      padding: 12px 14px;
    }
    .ia-popup-body .ia-context {
      font-size: 10px;
      color: #8b8178;
      padding: 6px 8px;
      background: #f9f7f3;
      border-radius: 6px;
      margin-bottom: 10px;
      border-left: 3px solid #667eea;
      max-height: 40px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .ia-color-row {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 10px;
    }
    .ia-color-row label {
      font-size: 10px;
      color: #5c584f;
      font-weight: 700;
    }
    .ia-color-dot {
      width: 18px; height: 18px;
      border-radius: 50%;
      border: 2px solid transparent;
      cursor: pointer;
      transition: transform 0.15s, border-color 0.15s;
    }
    .ia-color-dot:hover { transform: scale(1.2); }
    .ia-color-dot.selected { border-color: #1a2530; transform: scale(1.15); }

    .ia-textarea {
      width: 100%;
      min-height: 80px;
      max-height: 200px;
      border: 1px solid #e0ddd6;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 12px;
      font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
      line-height: 1.5;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
      color: #1d1d1b;
    }
    .ia-textarea:focus { border-color: #667eea; }

    .ia-popup-footer {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      background: #faf9f7;
      border-top: 1px solid #f0ece4;
    }
    .ia-popup-footer .ia-status {
      flex: 1;
      font-size: 10px;
      color: #8b8178;
    }
    .ia-popup-footer button {
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s, transform 0.1s;
    }
    .ia-popup-footer button:active { transform: scale(0.96); }
    .ia-btn-save { background: #d4edda; color: #1b7340; }
    .ia-btn-save:hover { background: #b7e4c7; }
    .ia-btn-delete { background: #f8d7da; color: #721c24; }
    .ia-btn-delete:hover { background: #f5c6cb; }

    /* Toggle panel for all annotations */
    .ia-panel-toggle {
      position: fixed;
      bottom: 16px;
      left: 16px;
      z-index: 9999;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff;
      border: none;
      width: 44px; height: 44px;
      border-radius: 50%;
      font-size: 18px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(102,126,234,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s;
    }
    .ia-panel-toggle:hover { transform: scale(1.1); }
    .ia-panel-toggle .ia-count {
      position: absolute;
      top: -4px; right: -4px;
      background: #e74c3c;
      color: #fff;
      font-size: 9px;
      font-weight: 800;
      width: 18px; height: 18px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* All annotations sidebar panel */
    .ia-sidebar {
      position: fixed;
      top: 0; left: 0;
      width: 360px;
      height: 100vh;
      background: #fff;
      z-index: 10002;
      box-shadow: 4px 0 20px rgba(0,0,0,0.15);
      transform: translateX(-100%);
      transition: transform 0.3s ease;
      display: flex;
      flex-direction: column;
      font-family: "Avenir Next", "Helvetica Neue", sans-serif;
    }
    .ia-sidebar.open { transform: translateX(0); }
    .ia-sidebar-header {
      padding: 16px 18px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .ia-sidebar-header h3 { margin: 0; font-size: 14px; }
    .ia-sidebar-header button {
      background: rgba(255,255,255,0.2);
      border: none;
      color: #fff;
      width: 28px; height: 28px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 16px;
    }
    .ia-sidebar-body {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
    }
    .ia-sidebar-item {
      padding: 12px;
      border: 1px solid #f0ece4;
      border-radius: 10px;
      margin-bottom: 10px;
      cursor: pointer;
      transition: background 0.15s, box-shadow 0.15s;
    }
    .ia-sidebar-item:hover {
      background: #f9f7f3;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .ia-sidebar-item .ia-si-context {
      font-size: 10px;
      color: #8b8178;
      padding: 4px 6px;
      background: #f4f1ea;
      border-radius: 4px;
      margin-bottom: 6px;
      border-left: 3px solid #667eea;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .ia-sidebar-item .ia-si-note {
      font-size: 12px;
      color: #1d1d1b;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .ia-sidebar-item .ia-si-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 6px;
      font-size: 9px;
      color: #b8b0a0;
    }
    .ia-sidebar-empty {
      text-align: center;
      padding: 40px 20px;
      color: #b8b0a0;
      font-size: 13px;
    }
    .ia-sidebar-empty span { font-size: 32px; display: block; margin-bottom: 10px; }

    /* Overlay when sidebar open */
    .ia-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.3);
      z-index: 10001;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s;
    }
    .ia-overlay.open { opacity: 1; pointer-events: all; }
  `;
  document.head.appendChild(style);

  // ===== PERSISTENCE =====
  function loadAnnotations() {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) { return []; }
  }

  function saveAnnotations() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(annotations));
    updateToggleBadge();
  }

  // ===== CREATE UI ELEMENTS =====
  // Floating "Add Note" button
  const addBtn = document.createElement('button');
  addBtn.className = 'ia-add-btn';
  addBtn.textContent = '📝 Add Note';
  document.body.appendChild(addBtn);

  // Sidebar toggle button
  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'ia-panel-toggle';
  toggleBtn.innerHTML = '📋<span class="ia-count">0</span>';
  toggleBtn.title = 'View all annotations';
  document.body.appendChild(toggleBtn);

  // Sidebar panel
  const sidebar = document.createElement('div');
  sidebar.className = 'ia-sidebar';
  sidebar.innerHTML = `
    <div class="ia-sidebar-header">
      <h3>📋 All Annotations</h3>
      <button class="ia-sidebar-close">✕</button>
    </div>
    <div class="ia-sidebar-body"></div>
  `;
  document.body.appendChild(sidebar);

  // Overlay
  const overlay = document.createElement('div');
  overlay.className = 'ia-overlay';
  document.body.appendChild(overlay);

  // ===== CORE FUNCTIONS =====
  const NOTE_COLORS = ['#1d1d1b', '#e74c3c', '#2980b9', '#27ae60', '#8e44ad', '#f39c12'];
  const HIGHLIGHT_COLORS = ['#fff176', '#aed581', '#81d4fa', '#f48fb1', '#ce93d8', '#ffab91'];

  function generateXPath(element) {
    if (element.id) return `//*[@id="${element.id}"]`;
    const parts = [];
    let current = element;
    while (current && current.nodeType === Node.ELEMENT_NODE) {
      let index = 1;
      let sibling = current.previousSibling;
      while (sibling) {
        if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === current.tagName) index++;
        sibling = sibling.previousSibling;
      }
      parts.unshift(`${current.tagName.toLowerCase()}[${index}]`);
      current = current.parentNode;
      if (current === document.body) break;
    }
    return '//' + parts.join('/');
  }

  function findTextInPage(searchText, xpath) {
    // Try to find the original text node by searching through the document
    const walker = document.createTreeWalker(
      document.querySelector('main') || document.body,
      NodeFilter.SHOW_TEXT,
      null
    );
    let node;
    while (node = walker.nextNode()) {
      if (node.textContent.includes(searchText)) {
        return node;
      }
    }
    return null;
  }

  function wrapTextWithHighlight(annotation) {
    const { selectedText, id } = annotation;
    const textNode = findTextInPage(selectedText);
    if (!textNode) return null;

    const text = textNode.textContent;
    const idx = text.indexOf(selectedText);
    if (idx === -1) return null;

    const range = document.createRange();
    range.setStart(textNode, idx);
    range.setEnd(textNode, idx + selectedText.length);

    const wrapper = document.createElement('span');
    wrapper.className = 'ia-highlight';
    wrapper.dataset.annotationId = id;
    wrapper.innerHTML = `<span class="ia-dot"></span>`;

    // Wrap without breaking existing structure
    try {
      range.surroundContents(wrapper);
      // Move the original text before the dot
      const originalText = document.createTextNode(selectedText);
      wrapper.insertBefore(originalText, wrapper.firstChild);
      // Remove the dot and re-add at end
      const dot = wrapper.querySelector('.ia-dot');
      wrapper.appendChild(dot);
    } catch(e) {
      // If surroundContents fails (crosses element boundaries), use alternative
      const fragment = range.extractContents();
      wrapper.insertBefore(fragment, wrapper.firstChild);
      range.insertNode(wrapper);
    }

    wrapper.addEventListener('click', (e) => {
      e.stopPropagation();
      showAnnotationPopup(annotation, wrapper);
    });

    return wrapper;
  }

  function showAnnotationPopup(annotation, anchorEl) {
    closeActivePopup();

    const rect = anchorEl.getBoundingClientRect();
    const popup = document.createElement('div');
    popup.className = 'ia-popup';
    popup.style.position = 'absolute';
    popup.style.top = (window.scrollY + rect.bottom + 8) + 'px';
    popup.style.left = Math.max(10, Math.min(rect.left, window.innerWidth - 360)) + 'px';

    const selectedColor = annotation.color || '#1d1d1b';
    const selectedHighlight = annotation.highlightColor || '#fff176';

    popup.innerHTML = `
      <div class="ia-popup-header">
        <span>📝 Annotation #${annotation.id}</span>
        <button class="ia-close-btn" title="Close">✕</button>
      </div>
      <div class="ia-popup-body">
        <div class="ia-context">"${escapeHtml(annotation.selectedText.substring(0, 80))}${annotation.selectedText.length > 80 ? '...' : ''}"</div>
        <div class="ia-color-row">
          <label>Text Color:</label>
          ${NOTE_COLORS.map(c => `<div class="ia-color-dot ${c === selectedColor ? 'selected' : ''}" data-type="text" data-color="${c}" style="background:${c};"></div>`).join('')}
        </div>
        <div class="ia-color-row">
          <label>Highlight:</label>
          ${HIGHLIGHT_COLORS.map(c => `<div class="ia-color-dot ${c === selectedHighlight ? 'selected' : ''}" data-type="highlight" data-color="${c}" style="background:${c};"></div>`).join('')}
        </div>
        <textarea class="ia-textarea" placeholder="Write your doubt / note here...">${escapeHtml(annotation.note || '')}</textarea>
      </div>
      <div class="ia-popup-footer">
        <span class="ia-status"></span>
        <button class="ia-btn-delete">🗑 Delete</button>
        <button class="ia-btn-save">💾 Save</button>
      </div>
    `;

    document.body.appendChild(popup);
    activePopup = popup;

    // Apply current color to textarea
    const textarea = popup.querySelector('.ia-textarea');
    textarea.style.color = selectedColor;

    // Color dot clicks
    popup.querySelectorAll('.ia-color-dot').forEach(dot => {
      dot.addEventListener('click', () => {
        const type = dot.dataset.type;
        const color = dot.dataset.color;
        // Deselect siblings
        dot.parentElement.querySelectorAll('.ia-color-dot').forEach(d => d.classList.remove('selected'));
        dot.classList.add('selected');

        if (type === 'text') {
          annotation.color = color;
          textarea.style.color = color;
        } else {
          annotation.highlightColor = color;
          anchorEl.style.background = color + '55';
          anchorEl.style.borderBottomColor = color;
        }
      });
    });

    // Save
    popup.querySelector('.ia-btn-save').addEventListener('click', () => {
      annotation.note = textarea.value;
      annotation.color = annotation.color || '#1d1d1b';
      annotation.highlightColor = annotation.highlightColor || '#fff176';
      annotation.updatedAt = new Date().toISOString();
      saveAnnotations();
      const status = popup.querySelector('.ia-status');
      status.textContent = '✓ Saved!';
      status.style.color = '#1b7340';
      setTimeout(() => closeActivePopup(), 800);
    });

    // Delete
    popup.querySelector('.ia-btn-delete').addEventListener('click', () => {
      if (!confirm('Delete this annotation?')) return;
      annotations = annotations.filter(a => a.id !== annotation.id);
      saveAnnotations();
      // Remove highlight from DOM
      if (anchorEl && anchorEl.parentNode) {
        const textContent = anchorEl.textContent.replace(/\s*$/, ''); // Remove dot's empty text
        const textNode = document.createTextNode(annotation.selectedText);
        anchorEl.parentNode.replaceChild(textNode, anchorEl);
      }
      closeActivePopup();
      renderSidebar();
    });

    // Close
    popup.querySelector('.ia-close-btn').addEventListener('click', closeActivePopup);

    // Focus textarea
    textarea.focus();
  }

  function showNewAnnotationPopup(selectedText, range) {
    closeActivePopup();

    const rect = range.getBoundingClientRect();
    const popup = document.createElement('div');
    popup.className = 'ia-popup';
    popup.style.position = 'absolute';
    popup.style.top = (window.scrollY + rect.bottom + 8) + 'px';
    popup.style.left = Math.max(10, Math.min(rect.left, window.innerWidth - 360)) + 'px';

    popup.innerHTML = `
      <div class="ia-popup-header">
        <span>📝 New Annotation</span>
        <button class="ia-close-btn" title="Close">✕</button>
      </div>
      <div class="ia-popup-body">
        <div class="ia-context">"${escapeHtml(selectedText.substring(0, 80))}${selectedText.length > 80 ? '...' : ''}"</div>
        <div class="ia-color-row">
          <label>Text Color:</label>
          ${NOTE_COLORS.map((c, i) => `<div class="ia-color-dot ${i === 0 ? 'selected' : ''}" data-type="text" data-color="${c}" style="background:${c};"></div>`).join('')}
        </div>
        <div class="ia-color-row">
          <label>Highlight:</label>
          ${HIGHLIGHT_COLORS.map((c, i) => `<div class="ia-color-dot ${i === 0 ? 'selected' : ''}" data-type="highlight" data-color="${c}" style="background:${c};"></div>`).join('')}
        </div>
        <textarea class="ia-textarea" placeholder="Write your doubt / note here..."></textarea>
      </div>
      <div class="ia-popup-footer">
        <span class="ia-status"></span>
        <button class="ia-btn-save">💾 Save</button>
      </div>
    `;

    document.body.appendChild(popup);
    activePopup = popup;

    const textarea = popup.querySelector('.ia-textarea');
    let chosenColor = '#1d1d1b';
    let chosenHighlight = '#fff176';

    // Color dot clicks
    popup.querySelectorAll('.ia-color-dot').forEach(dot => {
      dot.addEventListener('click', () => {
        const type = dot.dataset.type;
        const color = dot.dataset.color;
        dot.parentElement.querySelectorAll('.ia-color-dot').forEach(d => d.classList.remove('selected'));
        dot.classList.add('selected');
        if (type === 'text') {
          chosenColor = color;
          textarea.style.color = color;
        } else {
          chosenHighlight = color;
        }
      });
    });

    // Save
    popup.querySelector('.ia-btn-save').addEventListener('click', () => {
      const noteText = textarea.value.trim();
      if (!noteText) {
        textarea.style.borderColor = '#e74c3c';
        textarea.placeholder = 'Please write a note before saving...';
        return;
      }

      const annotation = {
        id: annotationIdCounter++,
        selectedText: selectedText,
        note: noteText,
        color: chosenColor,
        highlightColor: chosenHighlight,
        xpath: '', // We'll find it on reload
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      annotations.push(annotation);
      saveAnnotations();

      // Wrap the selected text with highlight
      wrapTextWithHighlight(annotation);

      const status = popup.querySelector('.ia-status');
      status.textContent = '✓ Saved!';
      status.style.color = '#1b7340';
      setTimeout(() => closeActivePopup(), 600);
      renderSidebar();
    });

    // Close
    popup.querySelector('.ia-close-btn').addEventListener('click', closeActivePopup);
    textarea.focus();
  }

  function closeActivePopup() {
    if (activePopup) {
      activePopup.remove();
      activePopup = null;
    }
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ===== TEXT SELECTION HANDLER =====
  let selectionTimeout;
  document.addEventListener('mouseup', (e) => {
    // Don't trigger on our own UI elements
    if (e.target.closest('.ia-popup') || e.target.closest('.ia-add-btn') || 
        e.target.closest('.ia-sidebar') || e.target.closest('.ia-panel-toggle') ||
        e.target.closest('.jn-notes-panel') || e.target.closest('.jn-toggle-btn')) return;

    clearTimeout(selectionTimeout);
    selectionTimeout = setTimeout(() => {
      const selection = window.getSelection();
      const selectedText = selection.toString().trim();

      if (selectedText.length > 2 && selectedText.length < 500) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        addBtn.style.top = (window.scrollY + rect.top - 36) + 'px';
        addBtn.style.left = (rect.left + rect.width / 2 - 50) + 'px';
        addBtn.classList.add('visible');

        // Store for later use
        addBtn._selectedText = selectedText;
        addBtn._range = range.cloneRange();
      } else {
        addBtn.classList.remove('visible');
      }
    }, 200);
  });

  // Hide add button on click elsewhere
  document.addEventListener('mousedown', (e) => {
    if (!e.target.closest('.ia-add-btn') && !e.target.closest('.ia-popup')) {
      addBtn.classList.remove('visible');
    }
    if (!e.target.closest('.ia-popup') && !e.target.closest('.ia-highlight') && !e.target.closest('.ia-add-btn')) {
      closeActivePopup();
    }
  });

  // Add button click
  addBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const selectedText = addBtn._selectedText;
    const range = addBtn._range;
    if (selectedText && range) {
      addBtn.classList.remove('visible');
      showNewAnnotationPopup(selectedText, range);
    }
  });

  // ===== SIDEBAR =====
  function renderSidebar() {
    const body = sidebar.querySelector('.ia-sidebar-body');
    if (annotations.length === 0) {
      body.innerHTML = `<div class="ia-sidebar-empty"><span>📝</span>No annotations yet.<br>Select any text to add a note!</div>`;
      return;
    }

    body.innerHTML = annotations.map(a => `
      <div class="ia-sidebar-item" data-id="${a.id}">
        <div class="ia-si-context">"${escapeHtml(a.selectedText.substring(0, 60))}${a.selectedText.length > 60 ? '...' : ''}"</div>
        <div class="ia-si-note" style="color:${a.color || '#1d1d1b'}">${escapeHtml(a.note)}</div>
        <div class="ia-si-meta">
          <span>${new Date(a.updatedAt || a.createdAt).toLocaleDateString()}</span>
          <span>#${a.id}</span>
        </div>
      </div>
    `).join('');

    // Click to scroll to annotation
    body.querySelectorAll('.ia-sidebar-item').forEach(item => {
      item.addEventListener('click', () => {
        const id = parseInt(item.dataset.id);
        const highlight = document.querySelector(`.ia-highlight[data-annotation-id="${id}"]`);
        if (highlight) {
          closeSidebar();
          highlight.scrollIntoView({ behavior: 'smooth', block: 'center' });
          highlight.style.outline = '3px solid #667eea';
          highlight.style.outlineOffset = '2px';
          setTimeout(() => {
            highlight.style.outline = '';
            highlight.style.outlineOffset = '';
          }, 2000);
        }
      });
    });
  }

  function openSidebar() {
    renderSidebar();
    sidebar.classList.add('open');
    overlay.classList.add('open');
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
  }

  toggleBtn.addEventListener('click', openSidebar);
  sidebar.querySelector('.ia-sidebar-close').addEventListener('click', closeSidebar);
  overlay.addEventListener('click', closeSidebar);

  function updateToggleBadge() {
    const count = toggleBtn.querySelector('.ia-count');
    count.textContent = annotations.length;
    count.style.display = annotations.length > 0 ? 'flex' : 'none';
  }

  // ===== RESTORE ANNOTATIONS ON LOAD =====
  function restoreAnnotations() {
    annotations.forEach(annotation => {
      const wrapper = wrapTextWithHighlight(annotation);
      if (wrapper && annotation.highlightColor) {
        wrapper.style.background = annotation.highlightColor + '55';
        wrapper.style.borderBottomColor = annotation.highlightColor;
      }
    });
    updateToggleBadge();
  }

  // ===== KEYBOARD SHORTCUT =====
  document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+N or Cmd+Shift+N to add note to selection
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'N') {
      e.preventDefault();
      const selection = window.getSelection();
      const selectedText = selection.toString().trim();
      if (selectedText.length > 2) {
        const range = selection.getRangeAt(0);
        showNewAnnotationPopup(selectedText, range);
      }
    }
    // Escape to close popup
    if (e.key === 'Escape') {
      closeActivePopup();
      closeSidebar();
    }
  });

  // ===== INIT =====
  function init() {
    // Wait for DOM to be fully parsed
    restoreAnnotations();
    renderSidebar();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
