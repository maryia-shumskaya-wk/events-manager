from django.db import models

from users.models import User


class Event(models.Model):
    """Custom event model with definition of event data itself, parameters of participants and data on
    creation of event. Even while updating, 'creating_by' and 'created_at' remain immutable
    """

    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendees = models.ManyToManyField(User, related_name="events")
    max_attendees = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
