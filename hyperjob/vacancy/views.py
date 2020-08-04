from django.shortcuts import render
from django.views.generic import View
from vacancy.models import Vacancy, VacancyCreateForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class VacancyView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "vacancies": Vacancy.objects.all()
        }
        return render(request, "vacancy/vacancy_list.html", context)


class VacancyCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        vacancy_create_form = VacancyCreateForm
        context = {
            "vacancy_create_form": vacancy_create_form
        }
        return render(request, "vacancy/vacancy_new.html", context)

    def post(self, request, *args,**kwargs):
        vacancy_create_form = VacancyCreateForm(request.POST)
        if request.user.is_authenticated and request.user.is_staff:
            if vacancy_create_form.is_valid():
                vacancy_description = request.POST.get("description")
                Vacancy.objects.create(author=request.user, description=vacancy_description)
                return redirect("/home")
        raise PermissionDenied
