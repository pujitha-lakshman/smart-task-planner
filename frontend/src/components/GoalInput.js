// frontend/src/components/GoalInput.js
import React, { useState } from "react";
import axios from "axios";

function GoalInput({ onTasksGenerated }) {
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!goal.trim()) {
      setError("Please enter a goal first!");
      return;
    }
    setError("");
    setLoading(true);

    // build payload
    // build payload
    const payload = { goal_text: goal.trim() };


    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/generate-plan/",
        payload
      );
      onTasksGenerated(response.data);
    } catch (err) {
      console.error(err);
      setError("Error generating tasks. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="goal-input-container">
      <form onSubmit={handleSubmit} className="goal-form">
        <textarea
          value={goal}
          placeholder="Enter your goal (e.g., Launch a mobile app for my startup)"
          onChange={(e) => setGoal(e.target.value)}
          className="goal-input"
          rows={3}
        />

        

        <button type="submit" disabled={loading} className="generate-btn">
          {loading ? "Generating..." : "Generate Plan"}
        </button>
      </form>

      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default GoalInput;
