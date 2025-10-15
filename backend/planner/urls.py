from django.urls import path
from .views import generate_plan_view
from .views import CompletedTaskListCreateView

urlpatterns = [
    path('generate-plan/', generate_plan_view, name='generate-plan'),
    path('completed_tasks/', CompletedTaskListCreateView.as_view(), name='completed_tasks'),
]
