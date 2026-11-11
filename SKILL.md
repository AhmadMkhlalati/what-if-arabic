---
name: what-if-arabic
description: Make a "What If" animated episode from one topic line ("What if you could rewind 10 seconds?"), in the dusk-lit stick-figure style of the What If channels that broke out on YouTube in October 2026. Writes the script on the seven-beat What If formula, lays out a shot list at the genre's pace, renders a storyboard of stills and self-checks it before animating, animates every frame in code (Remotion and SVG, with an original cast on one rig, rooms in perspective and light from lamps and windows), and renders a finished 15-25 s video, asking the user at each step (and for their own voice recording; no audio is generated). Use when someone asks for a What If episode, animation or cartoon, "make a what if video about X", a stick-figure explainer in this style, or to run the free What If skill.
---

# What If animation

One topic line in, a finished 15-25 second episode out. Every frame is SVG that Claude writes (rendered by
Remotion). No audio is generated: no AI voice, no sound effects, no music, no API keys. The only audio is a voice recording the user supplies. Two examples ship in `studio/src/episodes/`, both ready to
render: `rewind` ("What if you could rewind 10 seconds?", the proof clip: shots played backwards as the power) and
`copy-paste` ("What if you could copy and paste anything?", the skill's first full run: a new kitchen set, a
schematic for the science beat, a cliffhanger blackout). Read the one closest to your topic before you start.

| File | What's in it |
|---|---|
| `references/formula.md` | The seven-beat What If formula, the 15-25 s shape, script rules, choosing a topic |
| `references/look.md` | The measured look, pace, shot vocabulary, and the storyboard and motion checklists |
| `references/kit.md` | The building blocks: engine, cast, sets, room kit, light, UI, looks, and how to add each |
| `references/traps.md` | Everything that cost time on the two example episodes |
| `studio/` | The Remotion project: copy it once, then every episode lives in it |
| `scripts/` | plan, stills, board, motiongrid, master (Python 3.9+ and Node) |

## Rules

- **Original characters only.** Pip (the hero, look B) and Mo (his friend) are ours, and so are the sister, mum and
  the suit on the rig. Never a channel's own hero, and nothing that resembles a famous cartoon character: check every
  new look on the cast sheet (Mo's first hat was dropped for drifting toward one).
- **Original stories.** The formula is shared; the episode isn't anyone else's. Don't remake a channel's title.
- **Never claim the viral channels are made with Claude** or any other tool. Nobody has said how they're made.
- **Never generate audio.** No AI voice, sound effects, music or audio API. The only audio allowed is the user's own
  recording, which you ask them for (step 2) and drop in as `public/<slug>/voice.*`. Cuts are cued on frames
  (`f:` / `s:`); with a recording, listen to it or ask the user when each line lands, then set the frames.
- **Ask, step by step.** Run the pipeline as a conversation: one step at a time, in order. At the start of every
  step say which step it is, show what you made, ask the user your question(s) for that step, and **stop and wait for
  their answer** before starting the next. Never run ahead, never batch several steps, never assume an answer. If
  the user says "go ahead" or "you choose", you may do the remaining choices yourself but still show each result.
- **Storyboard before animation.** No video render until the stills pass the self-check (step 5) and, when the person
  is in the loop, they've seen the board.
- **Every fact is real.** A number in the script is worked out and sourced in the episode's `science` field first.

## Setup (once per machine)

Needs Node 18+, ffmpeg and ffprobe on the PATH, and Python 3.9+ with `Pillow`.

```bash
cp -r <skill>/studio ./what-if-studio && cd what-if-studio && npm install
```

Everything below runs from that studio folder; `<skill>` is this skill's folder. To work offline or in your own
brand face, put a display font in `public/fonts/` and set `titleFont` in `src/studio.config.ts` (the default title
face, Bricolage Grotesque, and the UI faces load from Google Fonts at render time). To update an existing studio to
a newer engine, copy `<skill>/studio/src/engine` over its `src/engine`.

## The pipeline

Open by telling the user the steps in one line (topic, script, voice, shot list, storyboard, check, animate, render)
and that you'll ask at each one. Then begin with step 1.

Work through the steps in order. Each ends on something you look at before the next.

### 1. Script

**Ask first:** "What's your topic line (what if ...)? Any power, tone or language (English/Arabic) you want?" Wait.
After writing the script, show it and ask: "Happy with this script, or what should change?" Wait for approval.

Read `references/formula.md`. Search YouTube for the premise first: if a What If channel already has that exact
episode, change the power or the rule. From the topic line, decide the power's word, its rule, three escalating
demos and the turn (one real fact with a number). Write `src/episodes/<slug>/episode.json` with `id` (PascalCase,
the composition name), `slug`, `topic`, `title` (two lines), `script` (one entry per beat) and `science` (each fact:
the claim, the working, the source). 45 to 65 words. Every line must be a picture; the script is the plan for the shots, nothing is spoken.

### 2. Your voice (optional, the user's own)

**Ask:** "Do you want a voice-over? I don't generate audio, so you'd record it yourself. Want me to give you the final
script text to read? Record it on your phone or computer and tell me the file path (wav, mp3 or m4a), or say skip for
a silent video." Wait. If they give a file, copy it to `public/<slug>/voice.<ext>` (create the folder), check its length
with ffprobe against the 15-25 s target, and tell them if it's far off (offer to trim the script or have them re-record).
Then ask roughly when each line starts (or listen to the length) so the cuts can be set; plan.py ends the episode at
the recording's length plus a short tail. If they skip, the video is silent.

### 3. Shot list

Design one shot per picture in the script (usually 9 to 14), varying the size and angle every cut (wide, insert,
medium, close-up, over the shoulder, high, low; see `references/look.md`). Add to `episode.json`:

- `shots`: `{ "id": "S1", "size": "medium", "set": "kitchen", "key": 14, "note": "what we see" }` (`key` is the
  frame of the shot's own clock the storyboard shows)
- `edit`: `{ "shot": "S1", "at": "f:44" }` per cut, cued on a frame (`f:44`), seconds (`s:1.5`) or `+18` frames after
  the previous cut (`reverse`, `from`, `to` and `look` for powers that bend a shot's clock)
- `end`: where the episode stops, `"f:560"` or `"s:18.5"`
- `fx`: one-frame flashes and shakes, `{ "at": "S3+2", "kind": "flash" }`

```bash
python <skill>/scripts/plan.py <slug>
```

It writes `timeline.json` and `out/<slug>/shotlist.md` and prints the pace. Aim for 27+ cuts a minute in the
opening and no static shot over about 3 s; fix what it flags before drawing anything.

### 4. Storyboard

**After the board is built, ask:** "Here's the storyboard. Which shots do you want changed?" Wait for notes before animating.

Read `references/kit.md` for the building blocks. Write `src/episodes/<slug>/shots.tsx`, one component per shot,
each a pure function of its clock `t` (copy the patterns in the two examples' `shots.tsx`), and `index.tsx` (the
episode and its power look), then add the episode to `src/episodes/index.ts`. At this step each shot only needs to
be right at its `key` frame. When a topic needs a place the library lacks, build it with the room kit and add it to
`src/engine/sets/` (and to the skill's copy) so the next episode has it, as the copy-paste run did with the kitchen
and the schematic. A new character or costume: add the look, then check it on the cast sheet
(`npx remotion still src/index.ts Cast out/cast.png`).

```bash
npx tsc --noEmit
node <skill>/scripts/stills.mjs <slug>
python <skill>/scripts/board.py <slug>
```

`out/<slug>/storyboard.jpg`: one captioned still per shot.

### 5. Self-check the stills

Look at the storyboard, then open every still in `out/<slug>/board/` at full size, and run the storyboard checklist
in `references/look.md` honestly, shot by shot. Write down what fails, fix it, re-render just those shots
(`stills.mjs <slug> S3 S7`), rebuild the sheet and look again. Repeat until it passes. Check `references/traps.md`
for the failure you're seeing before inventing a fix. If the person is in the loop, show them the board now and
take their notes before animating.

### 6. Animate

Bring each shot to life from its key pose: `poseAt` keys with anticipation, holds and overshoot, `faceAt` for
expressions, camera moves with `kf`, the power's look, the `fx`. Then render a draft and check the motion:

```bash
python <skill>/scripts/master.py <slug>
python <skill>/scripts/motiongrid.py <slug> S2 S5
node <skill>/scripts/stills.mjs <slug> --frames 120 240
```

Read the grids like a flipbook against the motion checklist in `references/look.md`; fix and re-render until it
reads.

### 7. Master and hand over

**Ask before the final render:** "Ready to render the final video?" After handing it over, ask if they want changes.

```bash
python <skill>/scripts/master.py <slug>
```

Renders the video (with the user's own voice if they supplied one, otherwise silent) and writes `out/<slug>/report.json` (length, pace). Watch the final file once through. Hand
over `out/<slug>/<slug>-final.mp4` and `out/<slug>/storyboard.jpg`, with the length and anything you'd still improve.

## Where an episode lives

| Path | What |
|---|---|
| `src/episodes/<slug>/episode.json` | Everything you write: script, science, shots, edit, fx |
| `src/episodes/<slug>/shots.tsx`, `index.tsx` | The drawing: one component per shot, the power's look |
| `src/episodes/<slug>/timeline.json` | Written by plan.py |
| `out/<slug>/` | board stills, storyboard.jpg, shotlist.md, motion grids, renders, report.json |


## Arabic episodes
If the user asks for an Arabic episode, set `"lang": "ar"` in episode.json, and write the on-screen text in Arabic.
Read references/arabic.md first. For one still image, use the `Portrait` or `ArabicTitle` compositions.
