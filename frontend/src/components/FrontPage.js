import React from "react";
import { useNavigate } from "react-router-dom";
import "../FrontPage.css";
import backgroundImage from "../assets/snp.png";

function FrontPage() {
  const navigate = useNavigate();

  return (
    <div
      className="front-page"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <div
        className="click-area"
        onClick={() => navigate("/planner")}
      ></div>
    </div>
  );
}

export default FrontPage;
