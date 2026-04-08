"""
Test Africa's Talking Sandbox SMS fix
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms, AT_API_KEY, AT_USERNAME

print("=" * 60)
print("AFRICA'S TALKING SANDBOX SMS TEST")
print("=" * 60)

print(f"Username: {AT_USERNAME}")
print(f"API Key: {AT_API_KEY[:20]}...")
print(f"API Key Valid: {AT_API_KEY != 'your-sandbox-api-key'}")

if AT_API_KEY == 'your-sandbox-api-key':
    print("STATUS: API KEY NOT CONFIGURED")
    print("ACTION: Replace placeholder with real sandbox key")
else:
    print("STATUS: API KEY CONFIGURED")
    print("TESTING SMS...")
    
    result = send_sms('+254799118934', 'TEST: Africa\'s Talking Sandbox SMS is working!')
    
    print(f"SMS Result: {result}")
    
    if result:
        print("SUCCESS: SMS sent to sandbox!")
        print("Check your Africa's Talking sandbox dashboard")
    else:
        print("FAILED: Check network and API configuration")

print("=" * 60)
