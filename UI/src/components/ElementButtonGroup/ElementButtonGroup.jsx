/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { TextMedium } from "../TextMedium";
import "./style.css";

export const ElementButtonGroup = ({
  size,
  position,
  state,
  className,
  textMediumIconNoneClassName,
  textMediumDivClassName,
  textMediumText = "Label",
  onClick,
}) => {
  return (
    <div
      className={`element-button-group ${size} position-${position} state-${state} ${className}`}
      onClick={onClick}
    >
      {size === "small" && (
        <div className="text-small">
          <div className="div">Label</div>
        </div>
      )}

      {["large", "medium"].includes(size) && (
        <TextMedium
          className={textMediumIconNoneClassName}
          divClassName={textMediumDivClassName}
          icon="none"
          text={textMediumText}
        />
      )}
    </div>
  );
};

ElementButtonGroup.propTypes = {
  size: PropTypes.oneOf(["large", "medium", "small"]),
  position: PropTypes.oneOf(["right", "middle", "left"]),
  state: PropTypes.bool,
  textMediumText: PropTypes.string,
};
