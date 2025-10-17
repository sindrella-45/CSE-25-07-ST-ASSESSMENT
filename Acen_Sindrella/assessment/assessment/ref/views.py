from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Account
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            # just try to find a user by email or contact
            try:
                user = Account.objects.get(email=identifier)
            except Account.DoesNotExist:
                try:
                    user = Account.objects.get(phone_number=identifier)
                except Account.DoesNotExist:
                    user = None

            if user and check_password(password, user.password):
                # Successful login (you could use session or redirect)
                messages.success(request, f"Welcome {user.full_name}!")
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


