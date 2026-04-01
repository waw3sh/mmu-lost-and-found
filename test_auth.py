#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_auth():
    """Test authentication system"""
    client = Client()
    
    print("=== TESTING AUTHENTICATION SYSTEM ===")
    
    # Test 1: Check if URLs resolve
    try:
        login_url = reverse('accounts:login')
        register_url = reverse('accounts:register')
        dashboard_url = reverse('dashboard')
        
        print(f"✅ Login URL: {login_url}")
        print(f"✅ Register URL: {register_url}")
        print(f"✅ Dashboard URL: {dashboard_url}")
        
    except Exception as e:
        print(f"❌ URL Resolution Error: {e}")
    
    # Test 2: Try to access dashboard without login
    response = client.get('/dashboard/')
    print(f"✅ Dashboard Access (no login): {response.status_code}")
    if response.status_code == 302:
        print("✅ Redirect working correctly")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
    
    # Test 3: Try to access admin panel without login
    response = client.get('/admin-panel/')
    print(f"✅ Admin Panel Access (no login): {response.status_code}")
    if response.status_code == 302:
        print("✅ Admin redirect working correctly")
    else:
        print(f"❌ Admin panel unexpected response: {response.status_code}")
    
    # Test 4: Check registration form rendering
    response = client.get('/accounts/register/')
    print(f"✅ Registration Page: {response.status_code}")
    if response.status_code == 200:
        print("✅ Registration page loads correctly")
    else:
        print(f"❌ Registration page error: {response.status_code}")
    
    print("\n=== AUTHENTICATION SYSTEM TEST COMPLETE ===")

if __name__ == '__main__':
    test_auth()
