from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Event
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile


def news_list(request):
    main_news = Article.objects.all()
    popular_categories = Category.objects.all()
    main_events = Event.objects.all()
    return render(request, 'home.html', {'main_news': main_news, 'popular_categories': popular_categories, 'main_events': main_events})


def event_list(request):
    main_events = Event.objects.all()
    return render(request, 'event_list.html', {'main_events': main_events})


def news_detail(request, pk):
    single_news = get_object_or_404(Article, pk=pk)
    return render(request, 'news_app/news_detail.html', {'single_news': single_news})


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Проверяем, существует ли уже профиль для данного пользователя
            if not Profile.objects.filter(user=user).exists():
                profile_user = profile_form.save(commit=False)
                profile_user.user = user
                profile_user.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('home')  # Замените 'home' на имя вашего представления главной страницы
            else:
                messages.error(request, 'Profile already exists for this user!')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')  # Replace 'home' with the name of your home view


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'event.html', {'event': event})
