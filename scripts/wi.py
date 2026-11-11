"""Shared helpers for the What If animation scripts: paths, episode files, cues.

Every script runs from the studio folder (the copy of studio/ where you ran npm install) and takes the episode slug:
    python <skill>/scripts/plan.py copy-paste
Episode files:  src/episodes/<slug>/episode.json (you write it), timeline.json (plan.py writes it)
Renders/review: out/<slug>/
Video only. Audio is never generated; the one optional audio is the user's own recording, public/<slug>/voice.*
"""
import json, pathlib, re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
STUDIO = pathlib.Path.cwd()
if not (STUDIO / 'src' / 'episodes').exists():
    raise SystemExit('Run this from the studio folder (the one with src/episodes and package.json).')


# ---------------------------------------------------------------- paths
def ep_dir(slug):
    return STUDIO / 'src' / 'episodes' / slug


def out_dir(slug):
    d = STUDIO / 'out' / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_episode(slug):
    p = ep_dir(slug) / 'episode.json'
    if not p.exists():
        raise SystemExit(f'No episode.json at {p}')
    return json.loads(p.read_text(encoding='utf-8'))


def load_json(p, default=None):
    p = pathlib.Path(p)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default


def save_json(p, data):
    pathlib.Path(p).write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')


def user_voice(slug):
    """The user's own voice recording, public/<slug>/voice.(wav|mp3|m4a|aac|ogg), or None."""
    for ext in ('wav', 'mp3', 'm4a', 'aac', 'ogg'):
        q = STUDIO / 'public' / slug / f'voice.{ext}'
        if q.exists():
            return q
    return None


def duration(path):
    """Length of a media file in seconds, via ffprobe."""
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------------------------------------------------------- cues
# Cues are frames or seconds, or shots: with no voice there are no word timings.
CUE = re.compile(r'^(?P<base>[^+\-#]+?)(?:#(?P<nth>\d+))?(?P<off>[+-]\d+)?$')


def resolve(cue, fps, segments=None, shot_ids=()):
    """A cue to a global frame. Forms:
    f:123      an absolute frame          s:4.2     seconds
    S3+2       2 frames after the start of shot S3's first segment (S3#2+2: its second segment; S3-4 before it)
    """
    cue = str(cue).strip()
    if cue.startswith('f:'):
        return int(round(float(cue[2:])))
    if cue.startswith('s:'):
        return int(round(float(cue[2:]) * fps))
    m = CUE.match(cue)
    if not m:
        raise SystemExit(f'Bad cue "{cue}"')
    base, nth, off = m['base'], int(m['nth'] or 1), int(m['off'] or 0)
    if segments is not None and base in shot_ids:
        segs = [s for s in segments if s['shot'] == base]
        if len(segs) < nth:
            raise SystemExit(f'Cue "{cue}": shot {base} has only {len(segs)} segment(s)')
        return segs[nth - 1]['a'] + off
    raise SystemExit(f'Cue "{cue}" is not a frame (f:123), seconds (s:4.2) or a shot (S3+2).')
