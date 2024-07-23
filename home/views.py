from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm
from .models import Writer


class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')


class UserRegisterView(View):
    form_class = RegisterForm
    template_name = 'home/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            user.save()
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
            messages.success(request, 'Wellcome!', extra_tags='success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class WriterListView(View):
    def get(self, request):
        writers = Writer.objects.all()
        return render(request, 'home/writers.html', {"writers": writers})


class AboutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'home/home.html')
