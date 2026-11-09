"""Checks the tools the studio needs and says what is missing, before anything fails halfway.

python scripts/preflight.py        (or: npm run preflight, from the studio folder)
Needs for stills/portraits: Node 18+. For full episodes: ffmpeg + ffprobe, Python 3.9+ with numpy and Pillow, and
ELEVENLABS_API_KEY (environment or a .env file). The key is only checked for being present, never printed.
"""
import importlib.util, os, shutil, subprocess, sys
from pathlib import Path

ok = True


def line(good, what, hint=''):
    global ok
    ok = ok and good
    print(('  OK   ' if good else '  MISS ') + what + ('' if good else '  ->  ' + hint))


node = shutil.which('node')
ver = subprocess.run([node, '-v'], capture_output=True, text=True).stdout.strip() if node else ''
line(bool(node) and int(ver.lstrip('v').split('.')[0]) >= 18, f'node {ver}', 'install Node 18 or newer')
line(bool(shutil.which('ffmpeg')) and bool(shutil.which('ffprobe')), 'ffmpeg + ffprobe', 'brew install ffmpeg')
line(sys.version_info >= (3, 9), f'python {sys.version.split()[0]}', 'use Python 3.9+')
for m in ('numpy', 'PIL'):
    line(importlib.util.find_spec(m) is not None, f'python module {m}', 'pip install numpy Pillow')
key = bool(os.environ.get('ELEVENLABS_API_KEY'))
for envf in (Path('.env'), Path('../.env')):
    if envf.exists() and 'ELEVENLABS_API_KEY=' in envf.read_text():
        key = True
line(key, 'ELEVENLABS_API_KEY (only for voiced episodes, not for stills)', 'set it in the environment or a .env file')
print('\nReady.' if ok else '\nSome items are missing (stills only need Node).')
