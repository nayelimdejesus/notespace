from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as DjangoLoginView
from .forms import StyledLoginForm

# Create your views here.
def landing(request):
    return render(request, 'accounts/landing.html', {})
class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = StyledLoginForm
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'w-full px-3 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': f'{field.label.lower()}'
        })


    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def auth_logout(request):
    logout(request)
    return redirect('landing')