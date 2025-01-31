import React from "react";
import "./App.css";

function App() {
  return (
    <div className="screen-container">
      <div className="swirl-background"></div>

      <div className="title-container">
        <h1 className="main-title">
          Super <br />
          Smash <br />
          Bros.
        </h1>
        <h2 className="subtitle">Melee</h2>

        <div className="press-start">Press Start</div>

        <div className="copyright">
          © 2001 Nintendo / HAL Laboratory, Inc. <br />
          Characters © Nintendo / HAL Laboratory, Inc.
          <br />
          Creatures Inc. / GAME FREAK inc. / APE inc.
          <br />
          INTELLIGENT SYSTEMS
        </div>
      </div>
    </div>
  );
}

export default App;
