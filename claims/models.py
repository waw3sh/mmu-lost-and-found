from django.db import models
from django.conf import settings
from items.models import Item

class Claim(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OTP_SENT', 'OTP Sent'),
        ('VERIFIED', 'Verified'),
        ('COLLECTED', 'Collected'),
        ('DISPUTED', 'Disputed'),
        ('REJECTED', 'Rejected'),
    ]
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='claim')
    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claims'
    )
    otp_code = models.CharField(max_length=64, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    handoff_method = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Claim by {self.claimant.get_full_name()} for {self.item.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']
