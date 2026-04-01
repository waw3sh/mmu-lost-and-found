from django.db import models
from items.models import Item

class Report(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')
    finder_name = models.CharField(max_length=100, blank=True, null=True)
    finder_email = models.EmailField(blank=True, null=True)
    location_found = models.CharField(max_length=300)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.item.name} found at {self.location_found}"

    class Meta:
        ordering = ['-created_at']
