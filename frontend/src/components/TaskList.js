import React from "react";
import axios from "axios";
import "./TaskList.css";

function TaskList({ tasks, goal, onComplete }) {

  const handleCheckbox = async (task) => {
    const newStatus = task.status === "Pending" ? "Done" : "Pending";

    try {
      // Update backend
      await axios.post("http://127.0.0.1:8000/api/completed_tasks/", {
        goal_name: goal,
        task_name: task.task_name,
        deadline: task.deadline || "",
        status: newStatus,
      });

      // Update parent state
      onComplete({ ...task, status: newStatus });
    } catch (err) {
      console.error("Error updating task:", err);
    }
  };

  if (!tasks || tasks.length === 0)
    return <p className="no-tasks">No tasks yet. Enter a goal to generate tasks.</p>;

  return (
    <div className="task-list">
      <h2>🧩 Tasks for: {goal}</h2>
      <div className="task-grid">
        {tasks.map((task, index) => (
          <div
            key={index}
            className={`task-tile ${task.status === "Done" ? "done" : ""}`}
          >
            <div className="tile-header">
              <input
                type="checkbox"
                checked={task.status === "Done"} // ✅ controlled checkbox
                onChange={() => handleCheckbox(task)}
                className="task-checkbox"
              />
              <strong>{task.task_name}</strong>
            </div>
            {task.deadline && <p>📅 {task.deadline}</p>}
            {task.dependencies && <p>🔗 {task.dependencies}</p>}
            <p className="task-status">{task.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TaskList;
