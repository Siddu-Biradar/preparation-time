#!/usr/bin/env python3
"""
FSD Notes Persistence Server
Saves Frontend System Design notes to ~/.fsd-notes/data.json
so they survive browser cache clears & restarts.

Usage: python3 fsd-notes-server.py
Port: 5503 (avoids conflicts with DSA:5501, JS:5502)
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = 5503
NOTES_DIR = os.path.join(os.path.expanduser('~'), '.fsd-notes')
os.makedirs(NOTES_DIR, exist_ok=True)
NOTES_FILE = os.path.join(NOTES_DIR, 'data.json')


def load_notes():
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_notes(data):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class NotesHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/notes':
            notes = load_notes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        if parsed.path == '/api/notes':
            try:
                incoming = json.loads(body.decode('utf-8'))
                slug = incoming.get('slug', '')
                content = incoming.get('content', '')

                if not slug:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "slug required"}')
                    return

                notes = load_notes()
                if content and content.strip() and content.strip() != '<br>':
                    notes[slug] = content
                else:
                    notes.pop(slug, None)
                save_notes(notes)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid JSON"}')

        elif parsed.path == '/api/notes/bulk':
            try:
                incoming = json.loads(body.decode('utf-8'))
                notes = load_notes()
                for slug, content in incoming.items():
                    if content and content.strip() and content.strip() != '<br>':
                        notes[slug] = content
                    else:
                        notes.pop(slug, None)
                save_notes(notes)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid JSON"}')

        elif parsed.path == '/api/notes/delete':
            try:
                incoming = json.loads(body.decode('utf-8'))
                slug = incoming.get('slug', '')
                if slug:
                    notes = load_notes()
                    notes.pop(slug, None)
                    save_notes(notes)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid JSON"}')
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    print(f'🚀 FSD Notes Server running at http://localhost:{PORT}')
    print(f'   Notes saved to: {NOTES_FILE}')
    print(f'   Press Ctrl+C to stop')
    httpd = HTTPServer(('localhost', PORT), NotesHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n🛑 Server stopped.')
        httpd.server_close()
