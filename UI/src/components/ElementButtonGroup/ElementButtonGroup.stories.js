import { ElementButtonGroup } from ".";

export default {
  title: "Components/ElementButtonGroup",
  component: ElementButtonGroup,
  argTypes: {
    size: {
      options: ["large", "medium", "small"],
      control: { type: "select" },
    },
    position: {
      options: ["right", "middle", "left"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    size: "large",
    position: "right",
    state: true,
    className: {},
    textMediumIconNoneClassName: {},
    textMediumDivClassName: {},
    textMediumText: "Label",
  },
};
