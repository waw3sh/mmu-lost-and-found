"""
Run this script to populate system with demo data for defense.
Usage: python manage.py shell < demo_data.py
Or paste into Django shell: python manage.py shell
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from accounts.models import User
from items.models import Item
from reports.models import Report
from claims.models import Claim
import hashlib

print("Creating demo data for MMU Lost & Found defense...")

# Create users
admin, _ = User.objects.get_or_create(
    email='admin@mmu.ac.ke',
    defaults={
        'username': 'admin@mmu.ac.ke',
        'first_name': 'Dr. James',
        'last_name': 'Omondi',
        'role': 'ADMIN',
        'phone': '+254711000001',
        'is_staff': True,
        'is_superuser': True,
    }
)
if _:
    admin.set_password('Admin1234!')
    admin.save()
    print("Admin created: admin@mmu.ac.ke / Admin1234!")

student1, _ = User.objects.get_or_create(
    email='amina@students.mmu.ac.ke',
    defaults={
        'username': 'amina@students.mmu.ac.ke',
        'first_name': 'Amina',
        'last_name': 'Wanjiru',
        'role': 'STUDENT',
        'phone': '+254722000002',
        'student_id': 'MMU/CS/2021/001',
    }
)
if _:
    student1.set_password('Student1234!')
    student1.save()
    print("Student 1 created: amina@students.mmu.ac.ke / Student1234!")

student2, _ = User.objects.get_or_create(
    email='brian@students.mmu.ac.ke',
    defaults={
        'username': 'brian@students.mmu.ac.ke',
        'first_name': 'Brian',
        'last_name': 'Kipchoge',
        'role': 'STUDENT',
        'phone': '+254733000003',
        'student_id': 'MMU/CS/2021/002',
    }
)
if _:
    student2.set_password('Student1234!')
    student2.save()
    print("Student 2 created: brian@students.mmu.ac.ke / Student1234!")

staff1, _ = User.objects.get_or_create(
    email='grace@mmu.ac.ke',
    defaults={
        'username': 'grace@mmu.ac.ke',
        'first_name': 'Grace',
        'last_name': 'Akinyi',
        'role': 'STAFF',
        'phone': '+254744000004',
        'student_id': 'MMU/STAFF/004',
    }
)
if _:
    staff1.set_password('Staff1234!')
    staff1.save()
    print("Staff created: grace@mmu.ac.ke / Staff1234!")

# Create items
items_data = [
    {
        'reporter': student1,
        'name': 'HP Laptop',
        'description': 'Black HP laptop 15 inch with MMU sticker on the cover. '
                       'Has a small crack on the bottom right corner. '
                       'Contains important project files and research data.',
        'category': 'electronics',
        'status': 'active',
    },
    {
        'reporter': student1,
        'name': 'Maasai Mara University ID Card',
        'description': 'Student ID card for Amina Wanjiru, Computer Science '
                       'department, Year 3. Has a small scratch on the front.',
        'category': 'documents',
        'status': 'found',
    },
    {
        'reporter': student1,
        'name': 'Black Umbrella',
        'description': 'Medium sized black umbrella with wooden handle. '
                       'Has initials AW written on the handle. '
                       'Slightly faded from sun exposure.',
        'category': 'other',
        'status': 'recovered',
    },
    {
        'reporter': student2,
        'name': 'Samsung Galaxy Buds',
        'description': 'White Samsung Galaxy Buds in a white charging case. '
                       'The case has a small scratch on the lid. '
                       'Right earbud has slight discoloration.',
        'category': 'electronics',
        'status': 'active',
    },
    {
        'reporter': student2,
        'name': 'Room Keys',
        'description': 'Bunch of 3 keys on a blue keychain with a small '
                       'soccer ball charm. One key is for hostel room, '
                       'one for locker, and one for bicycle lock.',
        'category': 'keys',
        'status': 'claimed',
    },
    {
        'reporter': student2,
        'name': 'Blue Jansport Backpack',
        'description': 'Dark blue Jansport backpack with a red zipper pull. '
                       'Has name written inside the top pocket. '
                       'Contains textbooks and notebooks.',
        'category': 'bags',
        'status': 'active',
    },
    {
        'reporter': staff1,
        'name': 'Reading Glasses',
        'description': 'Black rimmed reading glasses in a brown leather case. '
                       'Prescription: +2.0 for reading. '
                       'Case has MMU Finance Department logo.',
        'category': 'glasses',
        'status': 'active',
    },
    {
        'reporter': staff1,
        'name': 'Staff ID Card',
        'description': 'MMU Staff ID card for Grace Akinyi, Finance Department. '
                       'Has access to main building and finance office.',
        'category': 'documents',
        'status': 'found',
    },
]

created_items = []
for data in items_data:
    item, created = Item.objects.get_or_create(
        name=data['name'],
        reporter=data['reporter'],
        defaults={
            'description': data['description'],
            'category': data['category'],
            'status': data['status'],
        }
    )
    created_items.append(item)
    if created:
        print(f"Item created: {item.name} ({item.status})")

# Create reports
reports_data = [
    {
        'item_name': 'Maasai Mara University ID Card',
        'finder_name': 'Peter Otieno',
        'finder_email': 'peter@students.mmu.ac.ke',
        'location_found': 'Library Ground Floor, near the printer station',
        'message': 'Found it on the floor next to the printing station. '
                   'Looked like someone dropped it while collecting their printouts.',
    },
    {
        'item_name': 'Room Keys',
        'finder_name': 'Faith Wambui',
        'finder_email': 'faith@students.mmu.ac.ke',
        'location_found': 'Cafeteria Table 5, Main Block',
        'message': 'The keys were left on the table after lunch. '
                   'I secured them with the cafeteria staff.',
    },
    {
        'item_name': 'Black Umbrella',
        'finder_name': 'John Kamau',
        'finder_email': 'john@students.mmu.ac.ke',
        'location_found': 'Lecture Hall 3, Row C, Seat 12',
        'message': 'Left under the seat after the 2pm Computer Science lecture. '
                   'I picked it up so it wouldn\'t get stolen.',
    },
    {
        'item_name': 'Staff ID Card',
        'finder_name': 'Anonymous Student',
        'finder_email': 'anonymous@mmu.ac.ke',
        'location_found': 'Car Park near Administration Block',
        'message': 'Found it on the ground near the parking space for visitors. '
                   'Looked like it fell from someone\'s pocket.',
    },
]

for rdata in reports_data:
    try:
        item = Item.objects.get(name=rdata['item_name'])
        report, created = Report.objects.get_or_create(
            item=item,
            location_found=rdata['location_found'],
            defaults={
                'finder_name': rdata.get('finder_name'),
                'finder_email': rdata.get('finder_email'),
                'message': rdata.get('message', ''),
            }
        )
        if created:
            print(f"Report created for: {item.name}")
    except Item.DoesNotExist:
        print(f"Item not found: {rdata['item_name']}")

# Create a completed claim (recovered umbrella)
try:
    umbrella = Item.objects.get(name='Black Umbrella', reporter=student1)
    claim, created = Claim.objects.get_or_create(
        item=umbrella,
        defaults={
            'claimant': student1,
            'otp_verified': True,
            'status': 'COLLECTED',
            'handoff_method': 'Security Desk',
        }
    )
    if created:
        print("Completed claim created for Black Umbrella")
except Item.DoesNotExist:
    print("Umbrella not found")

# Create a pending claim (room keys)
try:
    keys = Item.objects.get(name='Room Keys', reporter=student2)
    otp = '123456'
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    claim, created = Claim.objects.get_or_create(
        item=keys,
        defaults={
            'claimant': student2,
            'otp_code': otp_hash,
            'otp_verified': False,
            'status': 'OTP_SENT',
        }
    )
    if created:
        print("Pending claim created for Room Keys (OTP: 123456)")
except Item.DoesNotExist:
    print("Room Keys not found")

print("")
print("=" * 50)
print("DEMO DATA COMPLETE!")
print("=" * 50)
print("Login credentials for defense:")
print("Admin:    admin@mmu.ac.ke     / Admin1234!")
print("Student:  amina@students.mmu.ac.ke  / Student1234!")
print("Student:  brian@students.mmu.ac.ke  / Student1234!")
print("Staff:    grace@mmu.ac.ke     / Staff1234!")
print("Pending OTP for Room Keys claim: 123456")
print("=" * 50)
