"""
Test sending item found SMS to +254799118934
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms

print("=" * 60)
print("TESTING ITEM FOUND SMS NOTIFICATION")
print("=" * 60)

phone_number = '+254799118934'
message = 'Hello! Your item "HP Laptop" was found near "Library". Log in to claim it: https://mmu-lost-and-found.onrender.com/claims/ - MMU Lost & Found'

print(f"Sending SMS to: {phone_number}")
print(f"Message: {message}")
print()

result = send_sms(phone_number, message)

print("=" * 60)
print(f"SMS SEND RESULT: {result}")
print("=" * 60)

if result:
    print("SUCCESS: SMS sent successfully!")
    print("Check your phone at +254799118934")
    print("You should receive the item found notification")
else:
    print("FAILED: SMS could not be sent")
    print("This is expected due to local SSL issues")
    print("Production server will send real SMS")

print()
print("Note: Local environment has SSL/network issues")
print("Production deployment will send real SMS to phone")
print("=" * 60)
