/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const TextMedium = ({
  icon,
  className,
  divClassName,
  text = "Label",
}) => {
  return (
    <div className={`text-medium ${icon} ${className}`}>
      {icon === "none" && <div className={`label ${divClassName}`}>{text}</div>}

      {["left", "middle"].includes(icon) && (
        <>
          <div className="iconly-light-outline-wrapper">
            <div className="image-wrapper">
              <div className="image">
                <div className="overlap-group">
                  <img
                    className="fill"
                    alt="Fill"
                    src="https://c.animaapp.com/v9zriqdu/img/fill-4-2.svg"
                  />

                  <img
                    className="img"
                    alt="Fill"
                    src="https://c.animaapp.com/v9zriqdu/img/fill-6-2.svg"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="text">
            <div className="text-wrapper">{text}</div>
          </div>
        </>
      )}
    </div>
  );
};

TextMedium.propTypes = {
  icon: PropTypes.oneOf(["none", "middle", "left"]),
  text: PropTypes.string,
};
