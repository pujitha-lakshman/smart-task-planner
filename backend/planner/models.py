from django.db import models

class Goal(models.Model):
    goal_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goal_text


class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Done', 'Done'),
    ]

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=255)
    deadline = models.CharField(max_length=100, null=True, blank=True)
    dependencies = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.task_name

class CompletedTask(models.Model):
    goal_name = models.CharField(max_length=255)
    task_name = models.CharField(max_length=255)
    deadline = models.CharField(max_length=100, blank=True, null=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_name} ({self.goal_name})"
