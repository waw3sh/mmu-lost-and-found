"""
Test QR code scanning after fixing the function call
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import notify_owner_item_found
from accounts.models import User
from items.models import Item

print("=" * 70)
print("TESTING QR CODE SCANNING AFTER FIX")
print("=" * 70)

print("FINDING USERS WITH ITEMS:")
print("-" * 50)
users_with_items = User.objects.filter(
    phone__isnull=False
).exclude(phone='').filter(
    reported_items__isnull=False
).distinct()

for user in users_with_items[:3]:
    items = Item.objects.filter(reporter=user)
    print(f"User: {user.email}")
    print(f"Name: {user.first_name} {user.last_name}")
    print(f"Phone: {user.phone}")
    print(f"Items: {items.count()}")
    
    if items.exists():
        item = items.first()
        print(f"Test Item: {item.name}")
        print(f"UUID: {item.uuid}")
        
        # Test the notification function
        print(f"\nTesting SMS notification...")
        result = notify_owner_item_found(user, item, "Library - Main Desk")
        
        print(f"Notification Result: {result}")
        
        if result:
            print("SUCCESS: SMS notification sent!")
        else:
            print("FAILED: SMS notification not sent")
    
    print("-" * 50)

print("\n" + "=" * 70)
print("QR CODE SCANNING TEST COMPLETE")
print("=" * 70)

print("\nNEXT STEPS:")
print("-" * 50)
print("1. Wait 2-3 minutes for Render.com to redeploy")
print("2. Go to: https://mmu-lost-and-found.onrender.com")
print("3. Login with your user")
print("4. Find your item and generate QR code")
print("5. Scan QR code with your phone")
print("6. Fill finder form and submit")
print("7. Check Africa's Talking sandbox for SMS")
print("-" * 50)
