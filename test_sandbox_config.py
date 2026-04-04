"""
Test Africa's Talking Sandbox API configuration
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms, AT_API_KEY, AT_USERNAME, AT_SMS_URL

print("=" * 60)
print("AFRICA'S TALKING SANDBOX TEST")
print("=" * 60)

print("CURRENT CONFIGURATION:")
print("-" * 40)
print(f"Username: {AT_USERNAME}")
print(f"API Key: {AT_API_KEY}")
print(f"API URL: {AT_SMS_URL}")
print(f"Mode: {'SANDBOX' if AT_USERNAME == 'sandbox' else 'PRODUCTION'}")
print("-" * 40)

print("\nTESTING SANDBOX SMS:")
print("-" * 40)

# Test SMS
phone_number = '+254799118934'
message = 'SANDBOX TEST: This is a test SMS from MMU Lost & Found system using Africa\'s Talking sandbox API!'

print(f"Sending to: {phone_number}")
print(f"Message: {message}")
print()

result = send_sms(phone_number, message)

print("RESULTS:")
print("-" * 40)
print(f"Send Result: {result}")

if result:
    print("SUCCESS: Sandbox SMS sent!")
    print("Check your Africa's Talking sandbox dashboard")
    print("You should see the SMS in sandbox logs")
else:
    print("FAILED: Could not send sandbox SMS")
    print("Check your sandbox API key configuration")
    print("Make sure you're using a valid sandbox API key")

print("-" * 40)
print("\nNEXT STEPS:")
print("-" * 40)
print("1. Get your actual sandbox API key from Africa's Talking")
print("2. Replace 'your-sandbox-api-key' in .env file")
print("3. Test again with real sandbox key")
print("4. QR code scanning will send SMS in sandbox mode")
print("-" * 40)

print("\n" + "=" * 60)
print("SANDBOX TEST COMPLETE")
print("=" * 60)
