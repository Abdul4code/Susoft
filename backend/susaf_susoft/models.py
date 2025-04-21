from django.db import models
from django.contrib.postgres.fields import ArrayField

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True, editable=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Sprint(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    title = models.CharField(max_length=255) 

    def __str__(self):
        return f"Sprint: {self.title} for Project: {self.project.name}"
    

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    class ImpactChoices(models.TextChoices):
        SOCIAL = 'social', 'Social'
        INDIVIDUAL = 'individual', 'Individual'
        ENVIRONMENTAL = 'environmental', 'Environmental'
        ECONOMIC = 'economic', 'Economic'
        TECHNICAL = 'technical', 'Technical'

    class TypeChoices(models.TextChoices):
        POSITIVE = 'positive', 'Positive'
        NEGATIVE = 'negative', 'Negative'

    class StatusChoices(models.TextChoices):
        TO_DO = 'to_do', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        UNDER_REVIEW = 'under_review', 'Under Review'
        COMPLETED = 'completed', 'Completed'

    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    impact = ArrayField(
        models.CharField(
            max_length=20,
            choices=ImpactChoices.choices
        ),
        blank=True,
        size=5  # Maximum number of selections you allow
    )
    type = models.CharField(
        max_length=20,
        choices=TypeChoices.choices
    )
    title = models.CharField(
        max_length=250,
        null=True
    )

    status = models.CharField(
        max_length=250,
        choices=StatusChoices.choices,
        default=StatusChoices.TO_DO
    )

    def __str__(self):
        return f"Task for {self.sprint.title}: {self.description[:30]}"
    
class RetroNote(models.Model):
    id = models.AutoField(primary_key=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    note = models.CharField(max_length=255)
    board_position = models.IntegerField(blank=True, null=True)  # Optional field for board position
    
    def __str__(self):
        return f"{self.sprint.note}"
    
class Metrics(models.Model):
    id = models.AutoField(primary_key=True)
    class StatusChoices(models.TextChoices):
        TO_DO = 'to_do', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        IN_REVIEW = 'in_review', 'Under Review'
        COMPLETED = 'completed', 'Completed'
        

    text = models.CharField(max_length=255)  # Store the metric text
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='metrics')  # Reference to Task
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices
    )

    def __str__(self):
        return f"Metric for Task: {self.task.description[:30]} - Status: {self.get_status_display()}"


