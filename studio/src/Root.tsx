import React from 'react';
import { Composition } from 'remotion';
import './engine/fonts';
import { STUDIO } from './studio.config';
import { EPISODES } from './episodes';
import { CastSheet } from './CastSheet';
import { Portrait, ArabicTitle, portraitDefaults } from './Portrait';

// Every episode gets two compositions: <Id> (the film) and <Id>Board (one frame per shot, at its key frame, for the
// storyboard). Cast renders the cast sheet.
//   npx remotion studio src/index.ts --port 3430

export const Root: React.FC = () => {
  const common = { width: STUDIO.width, height: STUDIO.height, fps: STUDIO.fps };
  const vertical = { ...common, width: 1080, height: 1920 }; // mobile episodes (episode.json "format": "vertical")
  return (
    <>
      {EPISODES.map((e) => (
        <React.Fragment key={e.id}>
          <Composition id={e.id} component={e.Main} durationInFrames={Math.max(1, e.total)} {...(e.format === 'vertical' ? vertical : common)} />
          <Composition id={`${e.id}Board`} component={e.Board} durationInFrames={Math.max(1, e.shotCount)} {...common} />
        </React.Fragment>
      ))}
      <Composition id="Portrait" component={Portrait} defaultProps={portraitDefaults} durationInFrames={1} {...common} />
      <Composition id="ArabicTitle" component={ArabicTitle} durationInFrames={90} {...common} />
      <Composition id="Cast" component={CastSheet} durationInFrames={1} {...common} />
    </>
  );
};
