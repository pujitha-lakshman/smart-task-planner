# planner/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Goal, Task
from .ai_helper import generate_plan

@api_view(['POST'])
def generate_plan_view(request):
    """
    Accepts:
    {
      "goal_text": "Build a portfolio site",
      "max_tasks": 6      # optional, integer
    }
    Returns:
    {
      "goal": "...",
      "tasks": [ {task_name, deadline, dependencies, status}, ... ]
    }
    """
    goal_text = request.data.get('goal_text')
    max_tasks = request.data.get('max_tasks', None)

    if not goal_text:
        return Response({"error": "Goal text is required"}, status=400)


    # Save goal
    goal = Goal.objects.create(goal_text=goal_text)

    # Generate tasks from AI
    ai_tasks = generate_plan(goal_text)

    saved_tasks = []
    for t in ai_tasks:
        task_obj = Task.objects.create(
            goal=goal,
            task_name=t.get("task_name", "Untitled Task"),
            deadline=t.get("deadline", "N/A"),
            dependencies=t.get("dependencies", ""),
            status="Pending"
        )
        saved_tasks.append({
            "task_name": task_obj.task_name,
            "deadline": task_obj.deadline,
            "dependencies": task_obj.dependencies,
            "status": task_obj.status
        })

    return Response({
        "goal": goal.goal_text,
        "tasks": saved_tasks
    })

from rest_framework import generics
from .models import CompletedTask
from .serializers import CompletedTaskSerializer

class CompletedTaskListCreateView(generics.ListCreateAPIView):
    queryset = CompletedTask.objects.all().order_by('-completed_at')
    serializer_class = CompletedTaskSerializer
