from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.generic import View, CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from resume.models import Resume, ResumeCreateForm
from vacancy.models import Vacancy, VacancyCreateForm


class MainMenu(View):
    def get(self, request, *args, **kwargs):
        return render(request, "menu/menu.html")


class MySignupView(CreateView):
    form_class = UserCreationForm
    template_name = "menu/signup.html"
    success_url = "/login"


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "menu/login.html"
    redirect_authenticated_user = True


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        try:
            user_vacancies = Vacancy.objects.filter(author=request.user)
            user_resumes = Resume.objects.filter(author=request.user)
        except:
            user_vacancies = None
            user_resumes = None
        vacancy_create_form = VacancyCreateForm()
        resume_create_form = ResumeCreateForm()
        context = {
            "username": request.user,
            "user_vacancies": user_vacancies,
            "user_resumes": user_resumes,
            "vacancy_create_form": vacancy_create_form,
            "resume_create_form": resume_create_form
        }
        return render(request, "menu/home.html", context)

    def post(self, request, *args, **kwargs):
        vacancy_create_form = VacancyCreateForm(request.POST)
        if request.user.is_authenticated and request.user.is_staff:
            if vacancy_create_form.is_valid():
                vacancy_description = request.POST.get("description")
                Vacancy.objects.create(author=request.user, description=vacancy_description)
                return redirect("/home")
        resume_create_form = ResumeCreateForm(request.POST)
        if request.user.is_authenticated and not request.user.is_staff:
            if resume_create_form.is_valid():
                resume_description = request.POST.get("description")
                Resume.objects.create(author=request.user, description=resume_description)
                return redirect("/home")
        return redirect("/home")

