"""
Create a completely new, robust login view
"""

# Read current accounts/views.py
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'r') as f:
    content = f.read()

# Find and replace login view
old_login = '''def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                
                # Redirect admins to admin dashboard
                if user.role == 'ADMIN':
                    return redirect('/accounts/admin-dashboard/')
                else:
                    return redirect('/dashboard/')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'accounts/login.html')'''

new_login = '''def login_view(request):
    """Handle user login - robust version."""
    if request.user.is_authenticated:
        # If already logged in, redirect based on role
        if request.user.role == 'ADMIN':
            return redirect('/accounts/admin-dashboard/')
        else:
            return redirect('/dashboard/')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        print(f"Login attempt: {email}")
        
        # Validate input
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'accounts/login.html')
        
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.email}, role: {user.role}")
            
            if user.check_password(password):
                print("Password correct, logging in...")
                login(request, user)
                
                # Redirect based on role
                if user.role == 'ADMIN':
                    print("Redirecting to admin dashboard")
                    messages.success(request, f'Welcome back, {user.first_name}! Admin access granted.')
                    return redirect('/accounts/admin-dashboard/')
                else:
                    print("Redirecting to regular dashboard")
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect('/dashboard/')
            else:
                print("Password incorrect")
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            print("User not found")
            messages.error(request, 'Invalid email or password. Please try again.')
        except Exception as e:
            print(f"Login error: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
    
    return render(request, 'accounts/login.html')'''

# Replace the login view
content = content.replace(old_login, new_login)

# Write back to file
with open('c:/Users/hp/.windsurf/2048/accounts/views.py', 'w') as f:
    f.write(content)

print("New robust login view created!")
