"""
Check Africa's Talking API configuration
Run this to verify if using real API or sandbox
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import AT_ENABLED, AT_API_KEY, AT_USERNAME

print("=" * 60)
print("AFRICA'S TALKING API STATUS")
print("=" * 60)

print(f"API Key Configured: {'YES' if AT_API_KEY else 'NO'}")
print(f"API Key Length: {len(AT_API_KEY) if AT_API_KEY else 0}")
print(f"Username: {AT_USERNAME}")
print(f"SMS Enabled: {'YES' if AT_ENABLED else 'NO'}")

if AT_API_KEY:
    print(f"\nAPI Key Type: {'PRODUCTION' if AT_API_KEY.startswith('atsk_') else 'UNKNOWN'}")
    
    if AT_USERNAME == 'sandbox':
        print("WARNING: Using sandbox username!")
    else:
        print("Using production username")
else:
    print("No API key configured - SMS will be logged only")

print("\n" + "=" * 60)
print("API STATUS CHECK")
print("=" * 60)

# Test actual SMS sending
from notifications.services import send_sms

test_phone = '+254799118934'
test_message = 'Test from MMU Lost & Found - API Status Check'

print(f"Testing SMS to: {test_phone}")
print(f"Message: {test_message}")
print()

result = send_sms(test_phone, test_message)

print(f"Send Result: {result}")

if AT_ENABLED:
    print("REAL Africa's Talking API is being used")
    print("SMS will be sent to actual phone numbers")
else:
    print("SANDBOX MODE - SMS will be logged only")
    print("No actual SMS will be sent")

print("\n" + "=" * 60)
print("CHECK COMPLETE")
print("=" * 60)
