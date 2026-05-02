"""
Watch mode: auto-rebuild HTML when any .py file changes.
Usage: python3 watch.py
"""
import time, subprocess, sys
from pathlib import Path

DIR = Path(__file__).parent
BUILD = DIR / "build_v2.py"
WATCHED = list(DIR.glob("*.py"))

def get_mtimes():
    return {f: f.stat().st_mtime for f in WATCHED if f.exists()}

prev = get_mtimes()
print(f"👀 Watching {len(prev)} files for changes... (Ctrl+C to stop)")

try:
    while True:
        time.sleep(1)
        curr = get_mtimes()
        changed = [f.name for f in curr if curr.get(f) != prev.get(f)]
        # Check for new files
        new_files = list(DIR.glob("*.py"))
        if len(new_files) != len(WATCHED):
            changed.append("(new/deleted files)")
            WATCHED.clear()
            WATCHED.extend(new_files)
        if changed:
            print(f"\n🔄 Changed: {', '.join(changed)}")
            result = subprocess.run([sys.executable, str(BUILD)],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print(f"❌ Build failed:\n{result.stderr.strip()}")
            prev = get_mtimes()
        else:
            prev = curr
except KeyboardInterrupt:
    print("\n👋 Watch stopped.")
