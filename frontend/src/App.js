import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import FrontPage from "./components/FrontPage";
import GoalInput from "./components/GoalInput";
import TaskList from "./components/TaskList";
import HistoryPage from "./components/HistoryPage";
import "./App.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [goal, setGoal] = useState("");
  const [completedTasks, setCompletedTasks] = useState({}); // goal -> completedTasks

  // Update tasks when AI generates plan
  const handleTasksGenerated = (data) => {
    setTasks(data.tasks || []);
    setGoal(data.goal || "");
  };

  // Toggle task status
  const handleTaskComplete = (updatedTask) => {
    // Update tasks array to reflect status change
    setTasks((prevTasks) =>
      prevTasks.map((t) =>
        t.task_name === updatedTask.task_name ? updatedTask : t
      )
    );

    // Update completedTasks history
    setCompletedTasks((prev) => {
      const updated = { ...prev };
      if (!updated[goal]) updated[goal] = [];

      if (updatedTask.status === "Done") {
        // Add if not already in history
        const exists = updated[goal].some(
          (task) => task.task_name === updatedTask.task_name
        );
        if (!exists) updated[goal].push(updatedTask);
      } else {
        // Remove if unchecked
        updated[goal] = updated[goal].filter(
          (task) => task.task_name !== updatedTask.task_name
        );
      }
      return updated;
    });
  };

  return (
    <Routes>
      <Route path="/" element={<FrontPage />} />
      <Route
        path="/planner"
        element={
          <div className="app-container">
            <header>
              <h1>Smart Task Planner</h1>
              <p className="objective">
                Break user goals into actionable tasks with timelines using AI reasoning.
              </p>
            </header>

            <GoalInput onTasksGenerated={handleTasksGenerated} />
            <TaskList
              tasks={tasks}
              goal={goal}
              onComplete={handleTaskComplete}
            />

            <footer>
              <a href="/history" className="history-link">
                View History
              </a>
              <p>© 2025 Smart Task Planner</p>
            </footer>
          </div>
        }
      />
      <Route
        path="/history"
        element={<HistoryPage completedTasks={completedTasks} />}
      />
    </Routes>
  );
}

export default App;
