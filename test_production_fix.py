"""
Test production SMS fix after updating Render.com to sandbox
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms, AT_API_KEY, AT_USERNAME, AT_SMS_URL
from decouple import config

print("=" * 70)
print("PRODUCTION SMS FIX VERIFICATION")
print("=" * 70)

print("CURRENT PRODUCTION CONFIGURATION:")
print("-" * 50)
print(f"Username: {AT_USERNAME}")
print(f"API Key: {AT_API_KEY[:20]}...")
print(f"API URL: {AT_SMS_URL}")
print(f"Mode: {'SANDBOX' if AT_USERNAME == 'sandbox' else 'PRODUCTION'}")
print(f"APP_URL: {config('APP_URL', default='NOT SET')}")
print("-" * 50)

print("\nTESTING PRODUCTION SMS:")
print("-" * 50)

# Test with your phone number
test_phone = '+254799118934'
test_message = 'PRODUCTION FIX TEST: SMS from MMU Lost & Found after Render.com update to sandbox'

print(f"Sending to: {test_phone}")
print(f"Message: {test_message}")

result = send_sms(test_phone, test_message)

print(f"\nSMS Result: {result}")

if result:
    print("SUCCESS: Production SMS working with sandbox!")
    print("Your Africa's Talking sandbox should receive SMS now")
else:
    print("FAILED: Production SMS not working")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("-" * 50)
print("1. Wait 2-3 minutes for Render.com to redeploy")
print("2. Go to: https://mmu-lost-and-found.onrender.com")
print("3. Login with your user (waweruepl@gmail.com)")
print("4. Register item and generate QR code")
print("5. Scan QR code with your phone")
print("6. Check Africa's Talking sandbox dashboard")
print("7. You should receive SMS notification!")
print("-" * 50)

print("\n" + "=" * 70)
print("FIX COMPLETE")
print("=" * 70)
