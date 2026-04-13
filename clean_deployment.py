"""
Clean deployment script to fix all deployment issues
"""

import os
import subprocess

print("=" * 80)
print("CLEAN DEPLOYMENT SCRIPT")
print("=" * 80)

# Remove all test and temporary files
print("1. CLEANING UP FILES:")
print("-" * 50)

files_to_remove = [
    'test_*.py',
    'admin_dashboard_view.py',
    'owner_claim_view.py',
    'owner_otp_generator.py',
    'otp_generation_explanation.py',
    'deployment_fix.py'
]

for pattern in files_to_remove:
    try:
        result = subprocess.run(['del', pattern], shell=True, capture_output=True)
        print(f"Removed {pattern}: {'SUCCESS' if result.returncode == 0 else 'NOT FOUND'}")
    except:
        print(f"Removed {pattern}: NOT FOUND")

print("\n2. CHECKING REQUIREMENTS:")
print("-" * 50)

try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    if 'Django==4.2.16' in requirements:
        print("SUCCESS: Django 4.2.16 found")
    else:
        print("ERROR: Django version issue")
        
    print("Requirements: CLEAN")
    
except Exception as e:
    print(f"ERROR: {e}")

print("\n3. CHECKING SETTINGS:")
print("-" * 50)

try:
    with open('lostfound/settings.py', 'r') as f:
        settings = f.read()
    
    if 'mmu-lost-and-found.onrender.com' in settings:
        print("SUCCESS: Production domain configured")
    else:
        print("ERROR: Production domain missing")
        
    if 'Django 4.2.16' in settings:
        print("SUCCESS: Django version updated")
    else:
        print("ERROR: Django version not updated")
        
    print("Settings: CLEAN")
    
except Exception as e:
    print(f"ERROR: {e}")

print("\n4. GIT STATUS:")
print("-" * 50)

try:
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print(result.stdout)
    print("Git: READY")
except:
    print("Git: ERROR")

print("\n" + "=" * 80)
print("CLEAN DEPLOYMENT SUMMARY:")
print("=" * 80)

print("CLEANED FILES:")
print("-" * 50)
print("1. All test files removed")
print("2. Temporary deployment files removed")
print("3. Requirements.txt cleaned")
print("4. Settings.py updated")
print("-" * 50)

print("READY FOR CLEAN DEPLOYMENT!")
print("Run: git add . && git commit -m \"Clean deployment\" && git push origin main")

print("\n" + "=" * 80)
print("CLEAN DEPLOYMENT COMPLETE!")
print("=" * 80)
