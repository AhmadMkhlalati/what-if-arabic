import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Hero, basePose, Pose, LOOKS, CastName, KitDefs, SetDefs, Study, TitleCard, FONT, hasArabic } from './engine';

// Two single-image compositions:
//   Portrait     one character, big, over the blurred study; pick them with --props.
//     npx remotion still src/index.ts Portrait out/noor.png --props='{"character":"noor","expr":"happy"}'
//   ArabicTitle  an Arabic title card (RTL, joined letters) with a character, the proof that Arabic renders.
//     npx remotion still src/index.ts ArabicTitle out/title-ar.png --frame=60

export type PortraitProps = { character: CastName; expr: Pose['expr']; yaw: number; caption: string };
export const portraitDefaults: PortraitProps = { character: 'noor', expr: 'happy', yaw: 0.25, caption: '' };

const Backdrop: React.FC = () => (
  <>
    <KitDefs />
    <SetDefs />
    <g filter="url(#blur10)">
      <Study t={0} id="portrait" />
    </g>
    <rect width={1920} height={1080} fill="#0B0816" opacity={0.4} />
  </>
);

export const Portrait: React.FC<PortraitProps> = ({ character, expr, yaw, caption }) => (
  <AbsoluteFill style={{ backgroundColor: '#14101C' }}>
    <svg width={1920} height={1080} viewBox="0 0 1920 1080">
      <Backdrop />
      <Hero look={LOOKS[character]} pose={{ ...basePose, x: 960, y: 590, scale: 1.75, yaw, expr, look: yaw * 1.5 }} shadow={0.7} />
      {caption ? (
        <text x={960} y={1010} textAnchor="middle" direction={hasArabic(caption) ? 'rtl' : 'ltr'} fontFamily={FONT.title} fontWeight={700} fontSize={64} fill="#F6EFE3">
          {caption}
        </text>
      ) : null}
    </svg>
  </AbsoluteFill>
);

export const ArabicTitle: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: '#14101C' }}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080">
        <Backdrop />
        <TitleCard t={f} lines={['ماذا لو استطعت', 'إعادة الزمن ١٠ ثوانٍ؟']} accent="إعادة" accentT={34} y={200} size={120} />
        <Hero look={LOOKS.noor} pose={{ ...basePose, x: 960, y: 740, scale: 1.15, yaw: 0.2, expr: 'happy' }} shadow={0.7} />
      </svg>
    </AbsoluteFill>
  );
};
