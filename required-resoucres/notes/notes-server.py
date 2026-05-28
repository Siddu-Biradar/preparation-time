#!/usr/bin/env python3
"""
DSA Notes Persistence Server
Saves notes to dsa-notes-data.json so they survive browser cache clears & restarts.

Usage: python3 notes-server.py
Then open: http://localhost:5501/dsa-patterns-guide.html
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

PORT = 5501
# Store notes in home directory — outside Five Server's watch scope (prevents reload loops)
NOTES_DIR = os.path.join(os.path.expanduser('~'), '.dsa-notes')
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
        # CORS headers for local development
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
            # Return all saved notes
            notes = load_notes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(notes).encode('utf-8'))
        else:
            # Serve static files normally
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/notes':
            # Save notes
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
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
                self.wfile.write(b'{"status": "saved"}')
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid json"}')

        elif parsed.path == '/api/notes/bulk':
            # Bulk save all notes at once
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
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
                self.wfile.write(json.dumps({"status": "saved", "count": len(notes)}).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid json"}')

        elif parsed.path == '/api/notes/delete':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                incoming = json.loads(body.decode('utf-8'))
                slug = incoming.get('slug', '')
                notes = load_notes()
                notes.pop(slug, None)
                save_notes(notes)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "deleted"}')
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "invalid json"}')

    def log_message(self, format, *args):
        # Cleaner logging
        if '/api/' in str(args[0]):
            print(f"  [Notes API] {args[0]}")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('localhost', PORT), NotesHandler)
    print(f"""
╔══════════════════════════════════════════════════════╗
║   DSA Notes Server Running                          ║
║   Open: http://localhost:{PORT}/dsa-patterns-guide.html  ║
║   Notes saved to: dsa-notes-data.json               ║
║   Press Ctrl+C to stop                              ║
╚══════════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
