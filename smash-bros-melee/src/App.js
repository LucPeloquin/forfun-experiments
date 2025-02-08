import React from "react";

export default function App() {
  // Inline styles for the main title.
  // If you prefer, move these into a separate CSS file.

  const mainTitleStyle = {
    fontFamily: "ITCGalliardStdUltra, serif", // Use the custom font
    fontSize: "4rem",
    // Stronger gradient from black (#000) to darker red (#8B0000) to brighter red (#FF0000)
    background: "linear-gradient(to bottom, #000000 0%, #8B0000 50%, #FF0000 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    // Thicker white outline
    WebkitTextStroke: "2px #fff",
    // Stronger shadow
    textShadow: "3px 3px 8px rgba(0,0,0,1)",
    letterSpacing: "-0.02em", // Slightly narrower spacing
    margin: 0,
    textAlign: "center",
  };


  const screenContainerStyle = {
    position: "relative",
    width: "100%",
    height: "100vh",
    color: "white",
    textAlign: "center",
    overflow: "hidden",
    background: "#1a1a1a", // Or use swirl gradient from a CSS class
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
  };

  const swirlBackgroundStyle = {
    position: "absolute",
    top: 0,
    left: 0,
    width: "200%",
    height: "200%",
    background:
      "conic-gradient(from 0deg, #262626 0deg, #2a2a2a 30deg, #0a0a0a 60deg, #1a1a1a 90deg, #2b2b2b 120deg, #303030 150deg, #1a1a1a 180deg, #262626 210deg, #2a2a2a 240deg, #0a0a0a 270deg, #1a1a1a 300deg, #2b2b2b 330deg, #303030 360deg)",
    animation: "swirl 15s linear infinite",
    zIndex: 0,
  };

  const titleContainerStyle = {
    position: "relative",
    zIndex: 1,
  };

  const pressStartStyle = {
    fontSize: "1.5rem",
    fontWeight: "bold",
    marginBottom: "2rem",
    animation: "blink 1.5s infinite",
  };

  const copyrightStyle = {
    fontSize: "0.8rem",
    opacity: 0.8,
    lineHeight: 1.2,
  };

  return (
    <div style={screenContainerStyle}>
      {/* Swirl background (uses separate CSS keyframes if needed) */}
      <div style={swirlBackgroundStyle}></div>

      <div style={titleContainerStyle}>
        {/* The text "Super" on one line and "Smash Bros." on the next */}
        <h1 style={mainTitleStyle}>Super</h1>
        <h1 style={mainTitleStyle}>Smash Bros.</h1>
        <div style={pressStartStyle}>Press Start</div>
        <div style={copyrightStyle}>
          © 2001 Nintendo / HAL Laboratory, Inc. <br />
          Characters © Nintendo / HAL Laboratory, Inc.<br />
          Creatures Inc. / GAME FREAK inc. / APE inc.<br />
          INTELLIGENT SYSTEMS
        </div>
      </div>

      {/* Inline <style> to define the font-face and animations. */}
      <style>{`
        /* If your file is in src/, we can reference it as below.
           The "format('opentype')" matches .otf files. */
        @font-face {
          font-family: 'ITCGalliardStdUltra';
          src: url('./ITCGalliardStdUltra.otf') format('opentype');
          font-weight: normal;
          font-style: normal;
        }

        @keyframes swirl {
          0% {
            transform: translate(-25%, -25%) rotate(0deg);
          }
          100% {
            transform: translate(-25%, -25%) rotate(360deg);
          }
        }

        @keyframes blink {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
