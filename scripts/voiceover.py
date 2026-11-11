"""Step 2: the voice-over script, for the user to review and then record or generate with their own tool.
Nothing is generated here except text: no audio, no API.

python <skill>/scripts/voiceover.py <slug>
Reads  src/episodes/<slug>/episode.json (script, lang, length)
Writes out/<slug>/voiceover.md   the review sheet: beats, timing estimate, checks
       out/<slug>/voiceover.txt  the clean narration only (one paragraph), to paste into a text-to-speech tool or read aloud

For Arabic (lang "ar") the script must be Modern Standard Arabic (Fusha) with full tashkeel; this checks that the
diacritics are really there and flags colloquial words it can recognise.
"""
import re

from wi import load_episode, out_dir

import sys

slug = sys.argv[1]
ep = load_episode(slug)
lang = ep.get('lang', 'en')
arabic = lang == 'ar'
beats = [(b.get('beat', ''), b['text'].strip()) for b in ep['script']]

TASHKEEL = re.compile('[ً-ْٰ]')   # fathatan .. sukun, dagger alif
LETTER = re.compile('[ء-ي]')
# common colloquial markers (Levantine/Egyptian/Gulf) that do not belong in Fusha narration
COLLOQUIAL = ['شو', 'ليش', 'إيش', 'ايش', 'دلوقتي', 'هلأ', 'هلا', 'كتير', 'مش ', 'بدّي', 'بدي', 'عشان', 'زي ', 'اللي', 'ده', 'دي ', 'يلا', 'وين', 'شلون', 'ازاي', 'إزاي']


def words(t):
    return [w for w in re.split(r'\s+', t) if w]


def strip_marks(t):
    return TASHKEEL.sub('', t)


total_words = sum(len(words(t)) for _, t in beats)
wps = 2.2 if arabic else 2.7          # a clear, unhurried read
secs = total_words / wps
target = ep.get('length')

rows, notes = [], []
for k, (name, text) in enumerate(beats, 1):
    n = len(words(text))
    row = f'### {k}. {name}\n\n{text}\n\n*{n} words, about {n / wps:.1f} s*\n'
    if arabic:
        letters = len(LETTER.findall(text))
        marks = len(TASHKEEL.findall(text))
        cover = marks / letters if letters else 1
        row += f'\n*tashkeel: {marks} marks on {letters} letters ({cover:.0%})*\n'
        if letters and cover < 0.6:
            notes.append(f'Beat {k} has too few diacritics ({cover:.0%}). Add full tashkeel: a mark on every letter, shadda, tanween, and a sukun where a letter is silent.')
        bare = strip_marks(text)
        for c in COLLOQUIAL:
            if c in bare:
                notes.append(f'Beat {k} may contain a colloquial word ("{c.strip()}"). Use the Fusha form.')
                break
        if not re.search(r'[ء-ي]', text):
            notes.append(f'Beat {k} has no Arabic letters but the episode is lang "ar".')
    rows.append(row)

if target:
    diff = secs - float(target)
    if abs(diff) > max(2.5, 0.12 * float(target)):
        notes.append(f'Estimated {secs:.0f} s against the {target} s target: {"cut" if diff > 0 else "add"} about {abs(diff) * wps:.0f} words.')

full = ' '.join(t for _, t in beats)
od = out_dir(slug)

head = f'# {" ".join(ep["title"]) if isinstance(ep.get("title"), list) else ep.get("title", slug)}: voice-over script\n\n'
head += f'Language: {"Modern Standard Arabic (Fusha), fully vowelled" if arabic else lang}. {total_words} words, about {secs:.0f} s at a clear, unhurried read'
head += f' (target {target} s).\n\n' if target else '.\n\n'
head += 'Review this, tell me what to change, then record it yourself or paste `voiceover.txt` into a text-to-speech tool of your choice and give me the file. I do not generate audio.\n\n'
if arabic:
    head += ('**Reading notes:** read it exactly as vowelled, at a steady pace; stop on the last letter of each sentence '
             '(waqf: no final vowel); pause a beat at every full stop and between beats; do not add words.\n\n')
body = '\n'.join(rows)
tail = ''
if notes:
    tail = '\n## Check before you record\n\n' + '\n'.join(f'- {n}' for n in notes) + '\n'
else:
    tail = '\n## Checks\n\nAll passed' + (': every beat is fully vowelled and in Fusha.' if arabic else '.') + '\n'
(od / 'voiceover.md').write_text(head + body + tail, encoding='utf-8')
(od / 'voiceover.txt').write_text(full + '\n', encoding='utf-8')

print(f'{total_words} words, about {secs:.0f} s' + (f' (target {target} s)' if target else ''))
for n in notes:
    print('  ! ' + n)
print(f'Wrote {od / "voiceover.md"} (review) and {od / "voiceover.txt"} (clean text)')
