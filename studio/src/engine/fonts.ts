import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';
import { loadFont as loadBricolage } from '@remotion/google-fonts/BricolageGrotesque';
import { loadFont as loadMono } from '@remotion/google-fonts/FragmentMono';
import { loadFont as loadHand } from '@remotion/google-fonts/Kalam';
import { loadFont as loadCairo } from '@remotion/google-fonts/Cairo';
import { STUDIO } from '../studio.config';

// Three faces: a heavy display face for the title card, a mono for on-screen readouts (timers, labels, chips),
// and a handwriting face for chalk and notes. The Google faces load at render time (they need a connection);
// a local title face from studio.config.ts loads from public/ and works offline.

loadBricolage('normal', { weights: ['600', '700', '800'], subsets: ['latin'] });
loadMono('normal', { weights: ['400'], subsets: ['latin'] });
loadHand('normal', { weights: ['400', '700'], subsets: ['latin'] });
// Cairo covers Arabic (and Latin): it sits at the end of every font stack, so Arabic text falls through to it
// automatically while Latin text keeps its own face. Set `lang: "ar"` in episode.json (see references/arabic.md).
loadCairo('normal', { weights: ['400', '600', '700', '800'], subsets: ['arabic', 'latin'] });
if (STUDIO.titleFont) loadFont({ family: STUDIO.titleFont.family, url: staticFile(STUDIO.titleFont.file), weight: STUDIO.titleFont.weight });

export const FONT = {
  title: `${STUDIO.titleFont ? STUDIO.titleFont.family : 'Bricolage Grotesque'}, Cairo`,
  ui: 'Fragment Mono, Cairo',
  hand: 'Kalam, Cairo',
  ar: 'Cairo',
};

/** True when the text contains Arabic script. */
export const hasArabic = (s: string) => /[\u0600-\u06FF\u0750-\u077F]/.test(s);
/** Letter-spacing that is safe for the script: Arabic letters join, so any spacing would break the words apart. */
export const tracking = (s: string, n: number) => (hasArabic(s) ? 0 : n);
