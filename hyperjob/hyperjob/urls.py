"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from menu.views import MainMenu, MyLoginView, MySignupView
from menu.views import ProfileView
from resume.views import ResumeView, ResumeCreateView
from vacancy.views import VacancyView, VacancyCreateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MainMenu.as_view()),
    path("resumes", ResumeView.as_view()),
    path("resume/new", ResumeCreateView.as_view()),
    path("vacancies", VacancyView.as_view()),
    path("vacancy/new", VacancyCreateView.as_view()),
    path("login", MyLoginView.as_view()),
    path("signup", MySignupView.as_view()),
    path("logout", LogoutView.as_view()),
    path("home", ProfileView.as_view())
]
