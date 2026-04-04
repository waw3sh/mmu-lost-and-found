"""
Test SMS in sandbox mode
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms, AT_ENABLED, AT_USERNAME, AT_API_KEY

print("=" * 60)
print("SMS SANDBOX MODE TEST")
print("=" * 60)

print(f"Username: {AT_USERNAME}")
print(f"API Key: {AT_API_KEY[:20]}...")
print(f"SMS Enabled: {AT_ENABLED}")

# Test SMS in sandbox mode
test_phone = '+254799118934'
test_message = 'SANDBOX TEST: This is a test message from MMU Lost & Found system in sandbox mode for defense demonstration!'

print(f"\nSending SMS to: {test_phone}")
print(f"Message: {test_message}")
print()

result = send_sms(test_phone, test_message)

print(f"Send Result: {result}")

if result:
    print("SUCCESS: Sandbox SMS sent!")
    print("Message logged in console (sandbox mode)")
else:
    print("FAILED: Could not send even in sandbox mode")

print("\n" + "=" * 60)
print("SANDBOX TEST COMPLETE")
print("=" * 60)
