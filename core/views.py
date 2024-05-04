from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from item.models import Category, Item

from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    
    return render(request, 'core/index.html',{
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('/login/')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {
        'form': form
    }) 
    
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    
    #return redirect('/')
    return render(request, 'core/logout.html')

@login_required
def profile(request):
    
    user = User
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            
            return redirect('/profile/')
    else:
        form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'core/profile.html', {
        'p_form': p_form,
        'form': form,
        'title': 'Update your details',
    })

