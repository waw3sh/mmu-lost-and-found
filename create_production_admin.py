"""
Create admin user directly in production
"""

# Read current accounts/views.py
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'r') as f:
    content = f.read()

# Add simple admin creation function
new_function = '''
def create_production_admin(request):
    """Create admin user - no login required."""
    from django.contrib.auth.hashers import make_password
    from accounts.models import User
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        if email and password:
            try:
                # Check if user exists
                if User.objects.filter(email=email).exists():
                    return render(request, 'accounts/create_admin.html', {
                        'error': 'User with this email already exists'
                    })
                
                # Create admin user
                admin_user = User.objects.create(
                    email=email,
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=make_password(password),
                    role='ADMIN',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True,
                    phone='+254700000000'
                )
                
                return render(request, 'accounts/create_admin.html', {
                    'success': f'Admin user {email} created successfully!'
                })
            except Exception as e:
                return render(request, 'accounts/create_admin.html', {
                    'error': f'Error: {str(e)}'
                })
    
    return render(request, 'accounts/create_admin.html')
'''

# Add new function at the end
lines = content.split('\n')
lines.append(new_function)

# Write back to file
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'w') as f:
    f.write('\n'.join(lines))

print("Production admin creation function added!")
