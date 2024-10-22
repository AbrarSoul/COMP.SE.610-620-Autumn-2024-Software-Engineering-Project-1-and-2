import { fn } from "@storybook/test";
import React from "react";

/** @type { import('@storybook/react').Preview } */
const preview = {
  parameters: {
    actions: {
      onClick: fn(),
    },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export const decorators = [
  (Story, context) => <Story key={JSON.stringify(context.args)} />,
];

export default preview;
