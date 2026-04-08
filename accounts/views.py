from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Use Django's built-in authenticate function
        from django.contrib.auth import authenticate
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        student_id = request.POST.get('student_id', '').strip()

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.student_id = student_id
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('/accounts/profile/')

    return render(request, 'accounts/profile.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        student_id = request.POST.get('student_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            student_id=student_id,
        )
        
        # Send welcome SMS if phone number provided
        if phone:
            try:
                from notifications.services import send_sms
                welcome_message = f"Welcome to MMU Lost & Found, {first_name}! Your account has been created successfully. You can now register and track your lost items."
                send_sms(phone, welcome_message)
            except Exception as e:
                # Log error but don't fail registration
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Welcome SMS failed: {str(e)}")
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f'Welcome, {first_name}! Your account has been created.')
        return redirect('/dashboard/')
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('/')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decouple import config
import datetime

@login_required  

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

def test_sms_view(request):
    """Temporary debug view — remove after fixing SMS."""
    from notifications.services import send_sms, AT_API_KEY, AT_USERNAME, AT_SMS_URL
    from accounts.models import User
    from django.contrib.auth.hashers import make_password
    
    # Check if password reset is requested
    if request.GET.get('reset_admin_password') == 'true':
        if request.user.role != 'ADMIN':
            return JsonResponse({'error': 'Admin only'}, status=403)
        
        # Reset admin passwords in production
        admin_users = User.objects.filter(role='ADMIN')
        reset_count = 0
        
        for admin in admin_users:
            admin.password = make_password('Admin1234!')
            admin.save()
            reset_count += 1
        
        return JsonResponse({
            'password_reset': True,
            'reset_count': reset_count,
            'new_password': 'Admin1234!',
            'message': f'Reset {reset_count} admin passwords to Admin1234!'
        })
    
    if request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Admin only'}, status=403)
    
    # Get all users from production database
    all_users = User.objects.all().order_by('-date_joined')
    users_with_phone = User.objects.filter(phone__isnull=False).exclude(phone='').order_by('-date_joined')
    
    # Look for tess@gmail.com specifically
    tess_user = User.objects.filter(email='tess@gmail.com').first()
    
    # Test SMS
    result = send_sms(
        request.user.phone or '+254799118934',
        'PRODUCTION DEBUG: Test SMS from MMU Lost & Found live system'
    )
    
    return JsonResponse({
        'sms_sent': result,
        'username': AT_USERNAME,
        'url': AT_SMS_URL,
        'api_key_set': bool(AT_API_KEY and AT_API_KEY != 'your-sandbox-api-key'),
        'api_key_prefix': AT_API_KEY[:8] + '...' if AT_API_KEY else 'NOT SET',
        'api_key_length': len(AT_API_KEY) if AT_API_KEY else 0,
        'app_url': config('APP_URL', default='NOT SET'),
        'user_phone': request.user.phone,
        'user_email': request.user.email,
        'environment': 'PRODUCTION' if config('DEBUG', default=False) == False else 'LOCAL',
        'timestamp': str(datetime.datetime.now()),
        'database_stats': {
            'total_users': all_users.count(),
            'users_with_phone': users_with_phone.count(),
            'tess_user_found': tess_user is not None,
            'tess_user_details': {
                'email': tess_user.email if tess_user else None,
                'name': f"{tess_user.first_name} {tess_user.last_name}" if tess_user else None,
                'phone': tess_user.phone if tess_user else None,
                'registered': str(tess_user.date_joined) if tess_user else None,
                'items': tess_user.reported_items.count() if tess_user else 0
            }
        },
        'admin_users': [
            {
                'email': admin.email,
                'name': f"{admin.first_name} {admin.last_name}",
                'role': admin.role,
                'is_staff': admin.is_staff,
                'is_superuser': admin.is_superuser
            }
            for admin in User.objects.filter(role='ADMIN')
        ]
    })


def public_users_view(request):
    """Public view to check users - no login required."""
    from accounts.models import User
    
    users = User.objects.all().order_by('-date_joined')
    admin_users = User.objects.filter(role='ADMIN')
    
    user_list = []
    for user in users[:10]:  # Show first 10 users
        user_list.append({
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}",
            'role': user.role,
            'phone': user.phone,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'date_joined': str(user.date_joined),
            'items_count': user.reported_items.count()
        })
    
    admin_list = []
    for admin in admin_users:
        admin_list.append({
            'email': admin.email,
            'name': f"{admin.first_name} {admin.last_name}",
            'role': admin.role,
            'is_staff': admin.is_staff,
            'is_superuser': admin.is_superuser,
            'is_active': admin.is_active
        })
    
    return JsonResponse({
        'total_users': users.count(),
        'admin_users_count': admin_users.count(),
        'recent_users': user_list,
        'admin_users': admin_list,
        'tess_user_found': User.objects.filter(email='tess@gmail.com').exists(),
        'mmuadmin_user_found': User.objects.filter(email='mmuadmin@lostfound.com').exists()
    })


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
