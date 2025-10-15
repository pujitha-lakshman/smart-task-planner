import React, { useEffect, useState } from "react";
import "./HistoryPage.css";
import { Link } from "react-router-dom";
import axios from "axios";

function HistoryPage() {
  const [completedTasks, setCompletedTasks] = useState({});

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/completed_tasks/")
      .then((res) => {
        const grouped = {};
        res.data.forEach((task) => {
          if (!grouped[task.goal_name]) grouped[task.goal_name] = [];
          grouped[task.goal_name].push(task);
        });
        setCompletedTasks(grouped);
      })
      .catch((err) => console.error("Error fetching history:", err));
  }, []);

  const goals = Object.keys(completedTasks);

  return (
    <div className="history-container">
      <h1>✅ Task History</h1>
      {goals.length === 0 ? (
        <p>No completed tasks yet.</p>
      ) : (
        goals.map((goal, index) => (
          <div key={index} className="goal-history">
            <h2>{goal}</h2>
            <ul>
              {completedTasks[goal].map((task, i) => (
                <li key={i} className="completed-task">
                  <strong>{task.task_name}</strong>
                  {task.deadline && <p>📅 {task.deadline}</p>}
                  <p>🕓 Completed: {new Date(task.completed_at).toLocaleString()}</p>
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
      <Link to="/planner" className="back-btn">← Back to Planner</Link>
    </div>
  );
}

export default HistoryPage;
