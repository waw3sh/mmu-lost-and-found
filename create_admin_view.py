"""
Add admin creation view to accounts/views.py
"""

# Read current accounts/views.py
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'r') as f:
    content = f.read()

# Add new admin creation function
new_function = '''
@login_required  
def create_admin_view(request):
    """Create new admin user - remove after fixing login."""
    from django.contrib.auth.hashers import make_password
    from accounts.models import User
    
    if request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Admin only'}, status=403)
    
    # Create new admin user
    try:
        new_admin = User.objects.create(
            email='mmuadmin@lostfound.com',
            username='mmuadmin@lostfound.com',
            first_name='MMU',
            last_name='Administrator',
            password=make_password('Admin1234!'),
            role='ADMIN',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            phone='+254700000000'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'New admin user created successfully!',
            'email': 'mmuadmin@lostfound.com',
            'password': 'Admin1234!',
            'role': 'ADMIN'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
'''

# Add the new function before the last function
lines = content.split('\n')
insert_position = -1

# Find the last function to insert before it
for i, line in enumerate(lines):
    if 'def test_sms_view(request):' in line:
        insert_position = i
        break

if insert_position > 0:
    lines.insert(insert_position, new_function)
    
    # Write back to file
    with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'w') as f:
        f.write('\n'.join(lines))
    
    print("Admin creation function added successfully!")
else:
    print("Could not find insertion point!")
