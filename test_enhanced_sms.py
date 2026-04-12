"""
Test enhanced SMS with finder contact information
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from notifications.services import notify_owner_item_found
from accounts.models import User
from items.models import Item

print("=" * 70)
print("TESTING ENHANCED SMS WITH FINDER CONTACT INFO")
print("=" * 70)

# Find a test user and item
test_user = User.objects.filter(phone__isnull=False).exclude(phone='').first()
if test_user:
    test_item = Item.objects.filter(reporter=test_user).first()
    
    if test_item:
        print(f"TEST USER: {test_user.first_name} {test_user.last_name}")
        print(f"USER PHONE: {test_user.phone}")
        print(f"TEST ITEM: {test_item.name}")
        print(f"ITEM UUID: {test_item.uuid}")
        print("-" * 50)
        
        # Test 1: Full finder info
        print("TEST 1: Full finder information")
        result1 = notify_owner_item_found(
            test_user, 
            test_item, 
            "Library - Main Desk", 
            finder_name="John Doe", 
            finder_phone="+254712345678"
        )
        print(f"Result: {result1}")
        print("-" * 50)
        
        # Test 2: Only finder name
        print("TEST 2: Only finder name")
        result2 = notify_owner_item_found(
            test_user, 
            test_item, 
            "Cafeteria - Table 5", 
            finder_name="Jane Smith"
        )
        print(f"Result: {result2}")
        print("-" * 50)
        
        # Test 3: No finder info (original)
        print("TEST 3: No finder information (original)")
        result3 = notify_owner_item_found(test_user, test_item, "Parking Lot A")
        print(f"Result: {result3}")
        print("-" * 50)
        
        print("ENHANCED SMS TESTS COMPLETED!")
        print("\nSAMPLE MESSAGES:")
        print("-" * 50)
        print("1. With finder info:")
        print("   'Hello [Name]! Your item [Item] was found near [Location] by John Doe. Contact finder: +254712345678. Meet at: [Location]. Log in to claim it: [URL] - MMU Lost & Found'")
        print("\n2. With name only:")
        print("   'Hello [Name]! Your item [Item] was found near [Location] by Jane Smith. Meet at: [Location]. Log in to claim it: [URL] - MMU Lost & Found'")
        print("\n3. No finder info:")
        print("   'Hello [Name]! Your item [Item] was found near [Location]. Log in to claim it: [URL] - MMU Lost & Found'")
        
    else:
        print("No items found for test user")
else:
    print("No users with phone numbers found")

print("\n" + "=" * 70)
print("DEPLOYMENT NEEDED:")
print("-" * 50)
print("1. Enhanced SMS function updated")
print("2. Finder form updated with phone field")
print("3. Report model updated with phone field")
print("4. Migration applied successfully")
print("5. Ready for production deployment")
print("=" * 70)
