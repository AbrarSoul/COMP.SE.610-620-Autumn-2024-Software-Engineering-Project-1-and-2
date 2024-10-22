/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React, { useReducer } from "react";
import { ElementButtonGroup } from "../ElementButtonGroup";
import { IconlyLightOutline } from "../IconlyLightOutline";
import "./style.css";

const initialState = { dark: "false" };

function reducer(state, action) {
  switch (action.type) {
    case "choose":
      return { ...state, dark: "file-chosen" };
    case "remove":
      return { ...state, dark: "false" };
    case "submit":
        return { ...state, dark: "submitted" };
    default:
      return state;
  }
}

export const Screen = ({ dark }) => {
  const [state, dispatch] = useReducer(reducer, { ...initialState, dark: dark || initialState.dark });

  return (
    <div className="screen">
      <div className={`file-upload ${state.dark}`}>
        {state.dark === "false" && (
          <>
            <IconlyLightOutline className="iconly-light-outline-upload" />
            <div className="text-wrapper-2">Drag your PDF here</div>
            <ElementButtonGroup
              className="choose-file-button"
              onClick={() => dispatch({ type: "choose" })}
              position="middle"
              size="medium"
              textMediumDivClassName="element-button-group-instance"
              textMediumIconNoneClassName="one-button-group"
              textMediumText="Choose file"
            />
          </>
        )}
        {state.dark === "file-chosen" && (
          <>
            <div className="file-upload-2">
              <div className="text-wrapper-3">file_name.pdf</div>
              <div className="div-wrapper">
                <div className="paper-wrapper">
                  <div className="paper">
                    <img className="fill-2" alt="Fill" src="https://c.animaapp.com/v9zriqdu/img/fill-4.svg" />
                    <img className="fill-3" alt="Fill" src="https://c.animaapp.com/v9zriqdu/img/fill-6.svg" />
                    <img className="fill-4" alt="Fill" src="https://c.animaapp.com/v9zriqdu/img/fill-8.svg" />
                  </div>
                </div>
              </div>
            </div>
            <div className="element-button-group-2">
              <ElementButtonGroup
                className="one-button-group-instance"
                onClick={() => dispatch({ type: "remove" })}
                position="left"
                size="medium"
                textMediumDivClassName="element-button-group-3"
                textMediumIconNoneClassName="instance-node"
                textMediumText="Remove"
              />
              <ElementButtonGroup
                className="element-button-group-4"
                onClick={() => dispatch({ type: "submit" })}
                position="right"
                size="medium"
                textMediumDivClassName="element-button-group-5"
                textMediumIconNoneClassName="instance-node"
                textMediumText="Submit"
              />
            </div>
          </>
        )}
        {state.dark === "submitted" && (
          <>
            <div className="text-wrapper-2">Submitted!</div>
          </>
        )}
      </div>
    </div>
  );
};

Screen.propTypes = {
  dark: PropTypes.oneOf(["submitted", "false", "file-chosen"]),
};

