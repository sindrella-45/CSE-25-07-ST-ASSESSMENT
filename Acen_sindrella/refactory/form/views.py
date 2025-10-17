from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import User
from .forms import SignupForm, LoginForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup.html', {'form': form})
            
            
            if User.objects.filter(phone_number=form.cleaned_data['phone_number']).exists():
                form.add_error('phone_number', 'Phone number already exists')
                return render(request, 'signup.html', {'form': form})
            
            
            user = User.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password']
            )
            
            context = {
                'success_message': True,
                'form': SignupForm()  
            }
            return render(request, 'signup.html', context)
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']
            
            user = None
            try:
                if '@' in email_or_phone:
                    user = User.objects.get(email=email_or_phone)
                else:
                    user = User.objects.get(phone_number=email_or_phone)
                
                if user and check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.full_name
                    request.session['user_email'] = user.email
                    return redirect('success')
                else:
                    return render(request, 'login.html', {'form': form})
                    
            except User.DoesNotExist:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def success_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    return render(request, 'success.html')
