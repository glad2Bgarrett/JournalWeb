from django.db import models
from django.utils import timezone


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    impact_level = models.IntegerField()
    num_times_read = models.IntegerField(blank=True, null=True)
    date_last_read = models.DateTimeField(blank=True, null=True)

    def entry_was_read(self):
        if self.num_times_read:
            self.num_times_read += 1
        else:
            self.num_times_read = 1
        self.date_last_read = timezone.now()
        self.save()

    def __str__(self):
        return self.title
