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
        
        # Use Django's default ModelBackend directly
        from django.contrib.auth.backends import ModelBackend
        backend = ModelBackend()
        user = backend.authenticate(request, username=email, password=password)
        
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
