# Arabic support

What works out of the box:

- **Text on screen.** Cairo is loaded for Arabic and Latin and sits at the end of every font stack (`engine/fonts.ts`),
  so Arabic falls through to it with no change to the shots. `TitleCard` switches to right-to-left and drops
  letter-spacing for Arabic (spacing would break the joined letters). Use `tracking(text, n)` and `hasArabic(text)`
  for your own text.
- **No voice.** Episodes are silent video; cuts are cued on frames (`f:` / `s:`).
- **Characters.** `noor` wears a hijab (`extra: 'hijab'`). `bald` is also available.

Try it:

    cd studio && npm install
    npx remotion still src/index.ts ArabicTitle out/title-ar.png --frame=60
    npx remotion still src/index.ts Portrait out/noor.png --props='{"character":"noor","caption":"نور"}'

Not done yet: a full Arabic example episode.
