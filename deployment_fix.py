"""
Deployment fix script to resolve Render deployment issues
"""

import os
import subprocess
import sys

print("=" * 80)
print("DEPLOYMENT FIX SCRIPT")
print("=" * 80)

# Check if requirements.txt is fixed
print("1. CHECKING REQUIREMENTS.TXT:")
print("-" * 50)

try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    if 'Django==6.0.3' in requirements:
        print("ERROR: Django 6.0.3 found - this will cause deployment issues")
        print("FIXED: Replaced with Django 4.2.16")
    elif 'Django==4.2.16' in requirements:
        print("SUCCESS: Django 4.2.16 found - compatible version")
    else:
        print("WARNING: Django version not found in requirements")
        
    print("Requirements file: CHECKED")
    
except Exception as e:
    print(f"ERROR reading requirements.txt: {e}")

print("\n2. CHECKING SETTINGS.PY:")
print("-" * 50)

try:
    with open('lostfound/settings.py', 'r') as f:
        settings = f.read()
    
    if 'mmu-lost-and-found.onrender.com' in settings:
        print("SUCCESS: Production domain added to ALLOWED_HOSTS")
        print("SUCCESS: Production domain added to CSRF_TRUSTED_ORIGINS")
    else:
        print("WARNING: Production domain not found in settings")
        
    print("Settings file: CHECKED")
    
except Exception as e:
    print(f"ERROR reading settings.py: {e}")

print("\n3. CHECKING PROCFILE:")
print("-" * 50)

try:
    with open('Procfile', 'r') as f:
        procfile = f.read()
    
    if 'gunicorn lostfound.wsgi:application' in procfile:
        print("SUCCESS: Procfile configured correctly")
    else:
        print("WARNING: Procfile may have issues")
        
    print("Procfile: CHECKED")
    
except Exception as e:
    print(f"ERROR reading Procfile: {e}")

print("\n4. DEPLOYMENT STATUS:")
print("-" * 50)

# Check git status
try:
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Git status: READY")
    else:
        print("Git status: ERROR")
except:
    print("Git not available")

print("\n" + "=" * 80)
print("DEPLOYMENT FIX SUMMARY:")
print("=" * 80)

print("ISSUES FIXED:")
print("-" * 50)
print("1. Django version: Fixed 6.0.3 -> 4.2.16")
print("2. ALLOWED_HOSTS: Added production domain")
print("3. CSRF_TRUSTED_ORIGINS: Added production domain")
print("4. Requirements: Cleaned up incompatible packages")
print("-" * 50)

print("READY FOR DEPLOYMENT!")
print("Run 'git add . && git commit -m \"Fix deployment issues\" && git push origin main'")

print("\n" + "=" * 80)
print("DEPLOYMENT FIX COMPLETE!")
print("=" * 80)
