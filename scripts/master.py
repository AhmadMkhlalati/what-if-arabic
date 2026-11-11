"""Step 8: the master. Renders the episode and writes the report. Silent unless the user supplied their own voice file; never generates audio.

python <skill>/scripts/master.py <slug> [--skip-render] [--concurrency 6]
Writes out/<slug>/<slug>-raw.mp4, out/<slug>/<slug>-final.mp4 and out/<slug>/report.json
"""
import json, subprocess, sys, time

from wi import STUDIO, ep_dir, load_episode, load_json, out_dir, save_json

slug = sys.argv[1]
args = sys.argv[2:]
conc = args[args.index('--concurrency') + 1] if '--concurrency' in args else None
ep = load_episode(slug)
od = out_dir(slug)
raw = od / f'{slug}-raw.mp4'
final = od / f'{slug}-final.mp4'
npx = 'npx.cmd' if sys.platform == 'win32' else 'npx'

if '--skip-render' not in args:
    t0 = time.time()
    cmd = [npx, 'remotion', 'render', 'src/index.ts', ep['id'], str(raw), '--log', 'error']
    if conc:
        cmd += ['--concurrency', conc]
    print(' '.join(cmd))
    subprocess.run(cmd, cwd=STUDIO, check=True)
    print(f'rendered in {time.time() - t0:.0f} s')

has_voice = bool((load_json(ep_dir(slug) / 'timeline.json') or {}).get('audio'))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-c:v', 'copy', *(['-c:a', 'aac', '-b:a', '192k'] if has_voice else ['-an']), '-movflags', '+faststart', str(final)], check=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(final)], capture_output=True, text=True).stdout.strip())
tl = load_json(ep_dir(slug) / 'timeline.json')
report = {
    'episode': ep['id'], 'file': str(final), 'seconds': round(dur, 2),
    'segments': len(tl['segments']), 'cuts_per_min': round((len(tl['segments']) - 1) / (tl['total'] / tl['fps']) * 60, 1),
}
save_json(od / 'report.json', report)
print(json.dumps(report, indent=1))
