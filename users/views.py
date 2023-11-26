from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from users.forms import SignupForm  # Update the path if necessary
from users.models import Profile
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, 'users/home.html')
def doctor_home(request):
    return render(request, 'users/doctor_home.html')
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Ensure the name attribute in the HTML form matches the key in request.FILES
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                user.profile.profile_picture = profile_picture
                user.profile.save()
            
            # Update other profile fields if needed
            user.profile.address_line1 = form.cleaned_data.get('address_line1')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.pincode = form.cleaned_data.get('pincode')
            user.profile.user_type = form.cleaned_data.get('user_type')
            user.profile.save()

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.save()
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print("User Type during login:", user.profile.user_type)
            print("Authenticated User:", user)
            login(request, user)
            print(request.session) 
            if user.profile.user_type == 'patient':
                return redirect('home')
            else:
                return redirect('doctor_home')
    else:
        form = SignupForm()
    
    context = {'form': form}
    return render(request, 'users/signup.html', context)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User is authenticated
                login(request, user)

                # Redirect to the dashboard based on user type
                if user.profile.user_type == 'patient':
                    return redirect('home')
                elif user.profile.user_type == 'doctor':
                    return redirect('doctor_home')
            else:
                # Authentication failed
                form.add_error(None, 'Invalid username or password')

    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)