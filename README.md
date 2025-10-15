Smart Task Planner
we named it as "ShootNPlan"

It is a web application designed to help users break down their goals into actionable tasks with timelines using AI reasoning. It provides a simple, intuitive interface to input goals, generate task plans, track progress, and maintain task history.

This project was built using React for the frontend, Django + DRF for the backend, and integrates OpenAI GPT API for intelligent task planning.

Features

AI-Powered Task Generation:
Enter a goal and let the AI break it down into detailed tasks, each with suggested deadlines and dependencies.

Task Tracking:
Mark tasks as completed directly in the interface. The app maintains task status and ensures toggling works seamlessly.

Task History:
All completed tasks are recorded and can be accessed later on the history page.

Responsive UI:
Modern, minimal design with hover effects and clear readability.

Flexible Backend:
Django handles data storage, API endpoints, and integrates with OpenAI for task generation.

Tech Stack

Frontend: React, JavaScript, CSS

Backend: Django, Django REST Framework (DRF)

Database: PostgreSQL

AI Integration: OpenAI GPT via openrouter.ai

Other Tools: Axios for API calls, dotenv for environment variables, CORS enabled

Setup Instructions
1. Clone the Repository
git clone <your-repo-url>
cd smart-task-planner

2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install -r requirements.txt


Create a .env file in backend/ with the following variables:

DJANGO_SECRET_KEY=<your-secret-key>
LLM_API_KEY=<your-openai-api-key>

3. Database Setup

Update backend/settings.py if needed:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'planner_db',
        'USER': 'postgres',
        'PASSWORD': 'pgsql@123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


Then migrate the database:

python manage.py makemigrations
python manage.py migrate

4. Run Backend Server
python manage.py runserver


The backend will be available at http://127.0.0.1:8000/.

5. Frontend Setup
cd frontend
npm install
npm start


The frontend will open at http://localhost:3000/.

How to Use

Navigate to the Planner page.

Enter a goal (e.g., "Launch a mobile app").

Click Generate Plan to see AI-generated tasks.

Use checkboxes to mark tasks as completed.

Visit the History page to view completed tasks for all goals.

Folder Structure
backend/         # Django backend
  planner/
    models.py
    views.py
    urls.py
    ai_helper.py   # AI task generation logic
    serializers.py
  smartplanner/
    settings.py
frontend/        # React frontend
  src/
    components/
      GoalInput.js
      TaskList.js
      FrontPage.js
      HistoryPage.js
  App.js
  App.css

Task Flow

User submits a goal through React form.

Backend endpoint /api/generate-plan/ calls ai_helper.generate_plan().

AI returns tasks with deadlines and dependencies.

Tasks are saved in PostgreSQL and sent back to frontend.

Users mark tasks as completed; status is updated locally and sent to /api/completed_tasks/.

History page fetches completed tasks from backend.

Key Notes

Task checkboxes are controlled components to ensure proper toggle behavior.

AI-generated deadlines are normalized to YYYY-MM-DD.

Optional max_tasks input was removed for simplicity.

All API responses and errors are gracefully handled.

Screenshots

(Optional: Add screenshots of the planner UI and task history)

Future Enhancements

Add user authentication for personal goal tracking.

Allow custom deadlines and priorities.

Drag-and-drop tasks for reordering.

Enhance AI suggestions with smarter dependencies.

Contact

For questions, you can reach me at pujithalakshman976@gmail.com
This project was built as part of a personal project/interview submission.
