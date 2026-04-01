import uuid
from django.db import models
from django.conf import settings

class Item(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),  # Personal registered items
        ('found', 'Found'),    # Items reported as found by others
        ('claimed', 'Claimed'),
        ('recovered', 'Recovered'),
        ('deactivated', 'Deactivated'),
    ]
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('jewelry', 'Jewelry'),
        ('clothing', 'Clothing'),
        ('documents', 'Documents'),
        ('bags', 'Bags & Wallets'),
        ('books', 'Books'),
        ('keys', 'Keys'),
        ('glasses', 'Glasses'),
        ('other', 'Other'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    photo = models.ImageField(upload_to='items/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location_found = models.CharField(max_length=200, blank=True, null=True)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reported_items',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.reporter.get_full_name()} ({self.status})"

    class Meta:
        ordering = ['-created_at']
