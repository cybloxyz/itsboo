import React, { useState } from "react";
import "../../please.css";

const PixelImageButton = ({ imgSrc, width = 128, height = 64, onClick, style }) => {
  const [pressed, setPressed] = useState(false);

  const handleClick = () => {
    setPressed(true);
    if (onClick) onClick();
    setTimeout(() => setPressed(false), 100);
  };

  return (
    <button
      onClick={handleClick}
      style={{
        width,
        height,
        background: `url(${imgSrc}) repeat center/100% 100%`,
        border: "none",
        cursor: "cursorp",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        transform: pressed ? "scale(0.9)" : "scale(1)",
        transition: "transform 0.1s ease",
        imageRendering: "pixelated",
        ...style,
      }}
    />
  );
};

export default PixelImageButton;