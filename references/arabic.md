# Arabic support

What works out of the box:

- **Text on screen.** Cairo is loaded for Arabic and Latin and sits at the end of every font stack (`engine/fonts.ts`),
  so Arabic falls through to it with no change to the shots. `TitleCard` switches to right-to-left and drops
  letter-spacing for Arabic (spacing would break the joined letters). Use `tracking(text, n)` and `hasArabic(text)`
  for your own text.
- **Voice-over script.** No audio is generated. `scripts/voiceover.py <slug>` writes the narration for the user to
  review (`out/<slug>/voiceover.md`) and a clean copy (`voiceover.txt`) to record or paste into their own
  text-to-speech tool. Cuts are cued on frames (`f:` / `s:`).
- **Fusha with full tashkeel.** Write the narration in Modern Standard Arabic, fully vowelled:
  - a haraka on every letter (فَتْحَة، ضَمَّة، كَسْرَة), shadda (ـّ) on doubled letters, tanween (ـً ـٍ ـٌ) where the grammar needs it,
    sukun (ـْ) on silent letters, and the case endings (الإعراب) on the words inside the sentence;
  - the last word of a sentence is read with waqf (no final vowel), so write it with a sukun or no ending mark;
  - hamzat al-wasl and the lam shamsiyya are marked as they are read;
  - no colloquial words (شو، ليش، كتير، بدي، مش، عشان، دلوقتي...) and no dialect verb forms;
  - numbers as words, short sentences, one idea each; a full stop wherever the voice should rest.
  Example: `لَوْ أَمْكَنَكَ أَنْ تُعِيدَ عَشْرَ ثَوَانٍ إِلَى الْوَرَاءِ، فِي أَيِّ وَقْتٍ تَشَاءُ؟`
  `voiceover.py` flags beats under 60% diacritic coverage and common dialect words; it can't prove the grammar is
  right, so read it once more before the user records.
- **Characters.** `noor` wears a hijab (`extra: 'hijab'`). `bald` is also available.

Try it:

    cd studio && npm install
    npx remotion still src/index.ts ArabicTitle out/title-ar.png --frame=60
    npx remotion still src/index.ts Portrait out/noor.png --props='{"character":"noor","caption":"نور"}'

Not done yet: a full Arabic example episode.
