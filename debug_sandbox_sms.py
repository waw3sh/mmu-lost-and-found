"""
Debug sandbox SMS issue - check production vs local
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import send_sms, AT_API_KEY, AT_USERNAME
from accounts.models import User
from items.models import Item

print("=" * 70)
print("DEBUGGING SANDBOX SMS ISSUE")
print("=" * 70)

print("SYSTEM STATUS:")
print("-" * 50)
print(f"Username: {AT_USERNAME}")
print(f"API Key: {AT_API_KEY[:20]}...")
print(f"Environment: {'LOCAL' if os.getenv('DJANGO_SETTINGS_MODULE') == 'lostfound.settings' else 'PRODUCTION'}")
print("-" * 50)

print("\nCHECKING USERS WITH PHONE NUMBERS:")
print("-" * 50)
users_with_phone = User.objects.filter(phone__isnull=False).exclude(phone='')
for user in users_with_phone[:5]:
    print(f"User: {user.email} | Phone: {user.phone} | Items: {Item.objects.filter(reporter=user).count()}")

print("\nTESTING QR CODE SCANNING FLOW:")
print("-" * 50)

if users_with_phone.exists():
    owner = users_with_phone.first()
    items = Item.objects.filter(reporter=owner)
    
    if items.exists():
        item = items.first()
        
        print(f"Owner: {owner.first_name} {owner.last_name}")
        print(f"Phone: {owner.phone}")
        print(f"Item: {item.name}")
        print(f"UUID: {item.uuid}")
        
        # Simulate QR code scan
        message = f'Hello {owner.first_name}! Your item "{item.name}" was found near "Library - Main Desk". Log in to claim it: https://mmu-lost-and-found.onrender.com/claims/ - MMU Lost & Found'
        
        print(f"\nSending SMS...")
        result = send_sms(owner.phone, message)
        
        print(f"SMS Result: {result}")
        
        if result:
            print("SUCCESS: SMS sent to sandbox")
            print("Check your Africa's Talking sandbox dashboard")
            print("You should see the SMS in the sandbox logs")
        else:
            print("FAILED: SMS not sent")
    else:
        print("No items found for user")
else:
    print("No users with phone numbers found")

print("\n" + "=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)

print("\nIMPORTANT NOTES:")
print("-" * 50)
print("1. Local environment sends SMS to sandbox")
print("2. Production server sends SMS to sandbox")
print("3. Make sure you're testing on PRODUCTION server")
print("4. URL: https://mmu-lost-and-found.onrender.com")
print("5. Check sandbox dashboard for SMS logs")
print("-" * 50)
