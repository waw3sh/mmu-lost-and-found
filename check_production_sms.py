"""
Check production SMS configuration and test
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms, AT_API_KEY, AT_USERNAME, AT_SMS_URL
from decouple import config

print("=" * 70)
print("PRODUCTION SMS CONFIGURATION CHECK")
print("=" * 70)

print("CURRENT SETTINGS:")
print("-" * 50)
print(f"Username: {AT_USERNAME}")
print(f"API Key: {AT_API_KEY[:20]}...")
print(f"API URL: {AT_SMS_URL}")
print(f"Mode: {'SANDBOX' if AT_USERNAME == 'sandbox' else 'PRODUCTION'}")
print(f"APP_URL: {config('APP_URL', default='NOT SET')}")
print("-" * 50)

print("\nTESTING PRODUCTION SMS:")
print("-" * 50)

# Test with the phone number you're using
test_phone = '+254799118934'
test_message = 'PRODUCTION TEST: This is a test from the live MMU Lost & Found system'

print(f"Sending to: {test_phone}")
print(f"Message: {test_message}")

result = send_sms(test_phone, test_message)

print(f"\nSMS Result: {result}")

if result:
    print("SUCCESS: SMS sent from production!")
    print("Check your Africa's Talking sandbox dashboard")
else:
    print("FAILED: SMS not sent from production")

print("\n" + "=" * 70)
print("DEBUGGING TIPS:")
print("-" * 50)
print("1. Check if production environment variables are set")
print("2. Verify Render.com has AT_API_KEY and AT_USERNAME")
print("3. Check sandbox dashboard for SMS logs")
print("4. Make sure phone number format is correct")
print("5. Verify QR code scanning triggers SMS function")
print("-" * 50)

print("\n" + "=" * 70)
print("CHECK COMPLETE")
print("=" * 70)
