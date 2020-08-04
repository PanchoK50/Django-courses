from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import redirect


class QueueManager:
    line_of_cars = {
        "ticket_count": 0,
        "change_oil": [],
        "inflate_tires": [],
        "diagnostic": []
    }

    # Order your services by hierarchy
    service_duration = {
        "change_oil": 2,
        "inflate_tires": 5,
        "diagnostic": 30
    }

    next_ticket_number = []

    def next_ticket():
        service_hierarchy = list(QueueManager.service_duration)
        for i in service_hierarchy:
            if len(QueueManager.line_of_cars[i]) != 0:
                return QueueManager.line_of_cars[i][0]

    def remove_finished_ticket():
        service_hierarchy = list(QueueManager.service_duration)
        for i in service_hierarchy:
            if len(QueueManager.line_of_cars[i]) != 0:
                QueueManager.line_of_cars[i].remove(QueueManager.line_of_cars[i][0])
                break

    def update_next_ticket():
        if len(QueueManager.next_ticket_number) != 0:
            QueueManager.next_ticket_number.remove(QueueManager.next_ticket_number[0])
        if QueueManager.next_ticket():
            QueueManager.next_ticket_number.append(QueueManager.next_ticket())



class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "tickets/menu.html")


class WaitQueue(TemplateView):
    template_name = "tickets/get_ticket.html"

    def time_to_wait(self, service):
        service_queue_duration = len(QueueManager.line_of_cars[service]) * QueueManager.service_duration[service]
        return service_queue_duration

    def total_time_to_wait(self, service):
        total_queue_duration = 0
        service_hierarchy = list(QueueManager.service_duration)
        service_index = service_hierarchy.index(service)
        for i in range(service_index + 1):
            total_queue_duration += self.time_to_wait(service_hierarchy[i])
        return total_queue_duration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_number"] = QueueManager.line_of_cars["ticket_count"] + 1
        service = kwargs["service"]
        context["service"] = service
        context["minutes_to_wait"] = self.total_time_to_wait(service)
        QueueManager.line_of_cars["ticket_count"] += 1
        QueueManager.line_of_cars[service].append(context["ticket_number"])
        return context


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        line_of_cars = QueueManager.line_of_cars

        context = {
            "oil_queue": len(line_of_cars["change_oil"]),
            "tires_queue": len(line_of_cars["inflate_tires"]),
            "diagnostic_queue": len(line_of_cars["diagnostic"]),
        }
        return render(request, "tickets/processing.html", context)

    def post(self, request, *args, **kwargs):
        QueueManager.update_next_ticket()
        QueueManager.remove_finished_ticket()
        return redirect("/processing")


class NextTicketView(View):

    def get(self, request, *args, **kwargs):
        if len(QueueManager.next_ticket_number) == 0:
            next_ticket = None
        else:
            next_ticket = QueueManager.next_ticket_number[0]
        context = {
            "number_of_ticket": next_ticket
        }
        return render(request, "tickets/next_ticket.html", context)
