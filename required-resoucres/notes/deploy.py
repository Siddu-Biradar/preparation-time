#!/usr/bin/env python3
"""
Deploy DSA Notes to Netlify with embedded notes.
This injects your saved notes (from dsa-notes-data.json) into the HTML
so anyone who opens the shared URL can see your notes.

Usage: python3 deploy.py
"""

import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(SCRIPT_DIR, 'dsa-patterns-guide.html')
# Notes stored in home directory (outside Five Server watch scope)
NOTES_FILE = os.path.join(os.path.expanduser('~'), '.dsa-notes', 'data.json')


def load_notes():
    """Load saved notes from JSON file."""
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            notes = json.load(f)
            return notes if notes else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def inject_notes_into_html():
    """Inject notes data into the HTML embedded script tag."""
    notes = load_notes()

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the embedded notes JSON
    pattern = r'(<script id="embedded-notes-data" type="application/json">)(.*?)(</script>)'
    notes_json = json.dumps(notes, ensure_ascii=False)
    replacement = f'\\1{notes_json}\\3'
    new_html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

    if new_html == html and notes:
        print("⚠️  Could not find embedded-notes-data script tag in HTML!")
        sys.exit(1)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return len(notes)


def deploy_to_netlify():
    """Run netlify deploy."""
    print("🚀 Deploying to Netlify...")
    result = subprocess.run(
        ['netlify', 'deploy', '--prod', '--dir=.'],
        cwd=SCRIPT_DIR,
        capture_output=False
    )
    return result.returncode == 0


def restore_html():
    """Reset embedded notes to empty {} after deploy (keep local HTML clean)."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    pattern = r'(<script id="embedded-notes-data" type="application/json">)(.*?)(</script>)'
    new_html = re.sub(pattern, r'\1{}\3', html, count=1, flags=re.DOTALL)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)


if __name__ == '__main__':
    print("╔═══════════════════════════════════════════╗")
    print("║   DSA Notes — Deploy with Shared Notes   ║")
    print("╚═══════════════════════════════════════════╝")
    print()

    # Step 1: Inject notes
    count = inject_notes_into_html()
    print(f"✅ Injected {count} note(s) into HTML")

    # Step 2: Deploy
    success = deploy_to_netlify()

    # Step 3: Restore HTML (remove injected notes from local file)
    restore_html()
    print("✅ Local HTML restored (notes removed from embedded tag)")

    if success:
        print()
        print("════════════════════════════════════════════")
        print("✅ DEPLOYED! Share this link:")
        print("   https://dsa-patterns-guide-sid.netlify.app/dsa-patterns-guide.html")
        print("   Your friend will see all your saved notes!")
        print("════════════════════════════════════════════")
    else:
        print("❌ Deploy failed. Check netlify CLI output above.")
        sys.exit(1)
