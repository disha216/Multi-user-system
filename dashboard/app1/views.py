from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import CustomUser
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
import re

# Login view
def login_view(req):
    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            if user.usertype == 'doctor':
                return render(req, "doctordashboard.html", {'user': user})
            else:
                return render(req, "clientdashboard.html", {'user': user})
        else:
            messages.error(req, "Invalid username or password")
            return redirect("login")
    return render(req, "login.html")

# Signup view
def signup_view(req):
    if req.method == 'POST':
        utype = req.POST.get('uservalue')
        fname = req.POST.get('firstname')
        lname = req.POST.get('lastname')
        email = req.POST.get('email')
        username = req.POST.get('username')
        password = req.POST.get('pass')
        cpass = req.POST.get('cpass')
        line1 = req.POST.get('line1')
        city = req.POST.get('city')
        state = req.POST.get('state')
        pincode = req.POST.get('pincode')
        profile_photo = req.FILES.get('pphoto')

        # Validate password
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            messages.error(req, "Password must be at least 8 characters long and contain both letters and numbers.")
            return redirect("signup")

        # Check if passwords match
        if password != cpass:
            messages.error(req, "Passwords do not match.")
            return redirect("signup")

        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(req, "Username already taken.")
            return redirect("signup")
        if CustomUser.objects.filter(email=email).exists():
            messages.error(req, "Email already registered.")
            return redirect("signup")

        # Save profile photo if provided
        profile_photo_path = None
        if profile_photo:
            profile_photo_path = default_storage.save(f"images/{profile_photo.name}", ContentFile(profile_photo.read()))

        # Create and save user
        user_instance = CustomUser.objects.create_user(
            usertype=utype,
            first_name=fname,
            last_name=lname,
            email=email,
            username=username,
            password=password,
            line1=line1,
            city=city,
            state=state,
            pincode=pincode,
            pphoto=profile_photo_path,
        )
        
        messages.success(req, "Account created successfully! You can now log in.")
        return redirect("login")
    return render(req, "signup.html")

# Doctor dashboard
def doctor_dashboard(req):
    if req.user.is_authenticated and req.user.usertype == 'doctor':
        return render(req, "doctordashboard.html", {'user': req.user})
    else:
        return HttpResponse("Unauthorized", status=401)

# Client dashboard
def client_dashboard(req):
    if req.user.is_authenticated and req.user.usertype == 'client':
        return render(req, "clientdashboard.html", {'user': req.user})
    else:
        return HttpResponse("Unauthorized", status=401)

# Logout view
def user_logout(req):
    logout(req)
    return redirect('login')

@login_required
def edit_details(request):
    if request.method == 'POST':
        # Get the logged-in user
        current_user = request.user

        # Update user information
        current_user.firstname = request.POST.get('firstname', current_user.first_name)
        current_user.lastname = request.POST.get('lastname', current_user.last_name)
        current_user.email = request.POST.get('email', current_user.email)
        current_user.line1 = request.POST.get('line1', current_user.line1)
        current_user.city = request.POST.get('city', current_user.city)
        current_user.state = request.POST.get('state', current_user.state)
        current_user.pincode = request.POST.get('pincode', current_user.pincode)
        if 'pphoto' in request.FILES:
            current_user.pphoto = request.FILES['pphoto']

        # Save the updated user information
        current_user.save()

        # Redirect based on user type
        if current_user.usertype == 'client':
            return redirect('client_dashboard')
        else:
            return redirect('doctor_dashboard')  # Assuming you have a doctor dashboard URL
    else:
        # Render the edit form with the current user information
        return render(request, 'edit_details.html', {'user': request.user})