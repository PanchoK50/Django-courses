from django.shortcuts import render
from django.views.generic import View
from resume.models import Resume, ResumeCreateForm
from django.shortcuts import redirect


class ResumeView(View):

    def get(self, request, *args, **kwargs):
        context = {
            "resumes": Resume.objects.all()
        }
        return render(request, "resume/resume_list.html", context)


class ResumeCreateView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("/home")
        resume_create_form = ResumeCreateForm
        context = {
            "resume_create_form": resume_create_form
        }
        return render(request, "resume/resume_new.html", context)

    def post(self, request, *args, **kwargs):
        resume_create_form = ResumeCreateForm(request.POST)
        if request.user.is_authenticated and not request.user.is_staff:
            if resume_create_form.is_valid():
                resume_description = request.POST.get("description")
                Resume.objects.create(author=request.user, description=resume_description)
                return redirect("/home")
        return redirect("/home")
