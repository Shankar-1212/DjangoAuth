from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from users.forms import SignupForm  # Update the path if necessary
from users.models import Profile

def view_profiles(request):
    profiles = Profile.objects.all()  # Get all Profile instances
    return render(request, 'profiles.html', {'profiles': profiles})

def home(request):
    return render(request, 'users/home.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from users.forms import SignupForm
from users.models import Profile

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
            user.profile.save()

            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.save()
            
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    
    context = {'form': form}
    return render(request, 'users/signup.html', context)
