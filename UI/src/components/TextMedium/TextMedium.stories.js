import { TextMedium } from ".";

export default {
  title: "Components/TextMedium",
  component: TextMedium,
  argTypes: {
    icon: {
      options: ["none", "middle", "left"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    icon: "none",
    className: {},
    divClassName: {},
    text: "Label",
  },
};
