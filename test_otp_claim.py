"""
Test complete OTP claim process
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from items.models import Item
from accounts.models import User
from claims.models import Claim
import random

print("=" * 70)
print("TESTING COMPLETE OTP CLAIM PROCESS")
print("=" * 70)

# Get a test user and found item
test_user = User.objects.filter(phone__isnull=False).exclude(phone='').first()
found_item = Item.objects.filter(status='found').first()

if test_user and found_item:
    print(f"TEST USER: {test_user.first_name} {test_user.last_name}")
    print(f"USER EMAIL: {test_user.email}")
    print(f"USER PHONE: {test_user.phone}")
    print("-" * 50)
    
    print(f"TEST ITEM: {found_item.name}")
    print(f"ITEM ID: {found_item.id}")
    print(f"ITEM UUID: {found_item.uuid}")
    print(f"ITEM STATUS: {found_item.status}")
    print(f"REPORTER: {found_item.reporter.email}")
    print("-" * 50)
    
    # Generate test OTP
    test_otp = f"{random.randint(100000, 999999)}"
    print(f"GENERATED OTP: {test_otp}")
    print("-" * 50)
    
    # Create a test claim
    try:
        claim = Claim.objects.create(
            item=found_item,
            claimant=test_user,
            otp_code=test_otp,
            handoff_method="pickup"
        )
        
        print("CLAIM CREATED SUCCESSFULLY!")
        print(f"CLAIM ID: {claim.id}")
        print(f"CLAIM STATUS: {claim.status}")
        print(f"OTP CODE: {claim.otp_code}")
        print(f"HANDOFF METHOD: {claim.handoff_method}")
        print(f"CREATED AT: {claim.created_at}")
        print("-" * 50)
        
        # Test claim detail view
        print("TESTING CLAIM DETAIL VIEW:")
        print(f"Claim Detail URL: https://mmu-lost-and-found.onrender.com/claims/{claim.id}/")
        print("-" * 50)
        
    except Exception as e:
        print(f"CLAIM CREATION FAILED: {str(e)}")
    
    print("\n" + "=" * 70)
    print("TEST CLAIM LINKS:")
    print("-" * 50)
    
    # Generate claim URL
    claim_url = f"https://mmu-lost-and-found.onrender.com/claims/create/{found_item.id}/"
    print(f"CLAIM URL: {claim_url}")
    print("-" * 50)
    
    print("TEST INSTRUCTIONS:")
    print("-" * 50)
    print("1. Login with test user credentials")
    print("2. Navigate to claim URL above")
    print("3. Enter OTP code: " + test_otp)
    print("4. Select handoff method")
    print("5. Submit claim")
    print("6. Verify claim appears in claims list")
    print("=" * 70)
    
else:
    print("❌ COULD NOT FIND TEST USER OR FOUND ITEM")
    print("Please create a user with phone number and an item with 'found' status")

print("\n" + "=" * 70)
print("ALL FOUND ITEMS WITH CLAIM URLS:")
print("-" * 50)

found_items = Item.objects.filter(status='found')
for item in found_items:
    claim_url = f"https://mmu-lost-and-found.onrender.com/claims/create/{item.id}/"
    print(f"{item.name}: {claim_url}")

print("=" * 70)
