# Arabic support

What works out of the box:

- **Text on screen.** Cairo is loaded for Arabic and Latin and sits at the end of every font stack (`engine/fonts.ts`),
  so Arabic falls through to it with no change to the shots. `TitleCard` switches to right-to-left and drops
  letter-spacing for Arabic (spacing would break the joined letters). Use `tracking(text, n)` and `hasArabic(text)`
  for your own text.
- **Voice.** Set `"lang": "ar"` in `episode.json`. `voice.py` then uses `eleven_multilingual_v2` (it speaks Arabic),
  keeps diacritics attached to their word, and the word timings drive the cuts as usual. The default voice is an
  English one: pick an Arabic-capable voice from your ElevenLabs library with `"voice": {"id": "<voice id>"}`.
- **Cues.** `edit` cues (`"at": "<word>"`) work with Arabic words; write the word without diacritics.
- **Characters.** `noor` wears a hijab (`extra: 'hijab'`). `bald` is also available.

Try it without any API key:

    cd studio && npm install
    npx remotion still src/index.ts ArabicTitle out/title-ar.png --frame=60
    npx remotion still src/index.ts Portrait out/noor.png --props='{"character":"noor","caption":"نور"}'

Not done yet (needs real testing with an Arabic voice): a full Arabic example episode, and checking the 15–25 s
length target against Arabic speaking pace. Voice timings for Arabic are untested here.
