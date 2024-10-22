import { Screen } from ".";

export default {
  title: "Components/Screen",
  component: Screen,
  argTypes: {
    dark: {
      options: ["submitted", "false", "file-chosen"],
      control: { type: "select" },
    },
  },
};

export const Default = {
  args: {
    dark: "submitted",
  },
};
