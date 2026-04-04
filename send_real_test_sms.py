"""
Send real test SMS to demonstrate system for defense
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms

print("=" * 60)
print("REAL SMS TEST FOR DEFENSE DEMONSTRATION")
print("=" * 60)

test_phone = '+254799118934'
test_message = 'TEST from MMU Lost & Found System - This is a REAL SMS sent via Africa\'s Talking API to demonstrate the system is working for defense presentation!'

print(f"Sending REAL TEST SMS to: {test_phone}")
print(f"Message: {test_message}")
print()
print("Initializing Africa's Talking API...")
print()

# Send the real SMS
result = send_sms(test_phone, test_message)

print("=" * 60)
print(f"SMS SEND RESULT: {result}")
print("=" * 60)

if result:
    print("SUCCESS: Real SMS sent to +254799118934")
    print("Check your phone - you should receive the message!")
    print("This proves the system is using REAL Africa's Talking API")
else:
    print("FAILED: SMS could not be sent")
    print("Check API configuration")

print()
print("Defense demonstration test complete!")
print("=" * 60)
