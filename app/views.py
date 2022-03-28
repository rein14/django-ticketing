from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import Ticket, Comment, File
from .forms import TicketForm, CommentForm, FileForm, TicketUpdateForm
from cms.ajax import (AjaxCreateView, AjaxDetailView,
                      AjaxUpdateView, AjaxDeleteView, AjaxFilesUpload)
from cms.views import CoreListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView


@login_required
def home(request):
    # return render(request, 'blank.html', context={'title': 'Blank page'})
    # if request.user.is_staff:
    #     return redirect('app:ticket-list')

    # if request.user.is_authenticated:
    #     return redirect('app:inbox')
    return redirect('app:inbox')


class TicketList(LoginRequiredMixin, CoreListView):
    model = Ticket

    def get_context_data(self, *args, **kwargs):
        context = super(TicketList, self).get_context_data(*args, **kwargs)
        new_context_entry = "All Tickets"
        context["title"] = new_context_entry
        return context


class UserTicketList(LoginRequiredMixin, CoreListView):
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(UserTicketList, self).get_context_data(*args, **kwargs)
        new_context_entry = "Unassigned Tickets"
        context["title"] = new_context_entry
        return context


class UnassignedTickets(LoginRequiredMixin, CoreListView):
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(UnassignedTickets, self).get_context_data(
            *args, **kwargs)
        new_context_entry = "Unassigned"
        context["title"] = new_context_entry
        return context


class InboxList(LoginRequiredMixin, CoreListView):
    model = Ticket
    # queryset = Ticket.objects.filter(
    #     assigned_to=request.user).exclude(ticket_choices__exact=2)
    context_object_name = 'inbox'

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user).exclude(ticket_choices__exact=2)

    def get_context_data(self, *args, **kwargs):
        context = super(InboxList, self).get_context_data(*args, **kwargs)
        new_context_entry = "Inbox"
        context["title"] = new_context_entry
        return context


class CompletedList(LoginRequiredMixin, CoreListView):
    model = Ticket
    # queryset = Ticket.objects.filter(
    #     assigned_to=request.user).exclude(ticket_choices__exact=1)
    context_object_name = 'completed'

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user).exclude(ticket_choices__exact=1)

    def get_context_data(self, *args, **kwargs):
        context = super(CompletedList, self).get_context_data(*args, **kwargs)
        new_context_entry = "Completed Tickets"
        context["title"] = new_context_entry
        return context


class ArchiveList(LoginRequiredMixin, CoreListView):
    model = Ticket
    context_object_name = 'archive_list'

    def get_queryset(self):
        return Ticket.objects.filter(ticket_choices__exact=2)

    def get_context_data(self, *args, **kwargs):
        context = super(ArchiveList, self).get_context_data(*args, **kwargs)
        new_context_entry = "Archives"
        context["title"] = new_context_entry
        return context


class OpenTicketsList(LoginRequiredMixin, CoreListView):
    model = Ticket
    queryset = Ticket.objects.exclude(ticket_choices__exact=2)
    context_object_name = 'openticket_list'

    def get_context_data(self, *args, **kwargs):
        context = super(OpenTicketsList, self).get_context_data(
            *args, **kwargs)
        new_context_entry = "Open Tickets"
        context["title"] = new_context_entry
        return context


class TicketCreate(LoginRequiredMixin, AjaxCreateView):
    model = Ticket
    form_class = TicketForm

    # def get_redirect_url(self):
    #     return reverse_lazy('app:home')


class TicketUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Ticket
    form_class = TicketUpdateForm


class TicketDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Ticket


class TicketDetail(LoginRequiredMixin, AjaxDetailView):
    model = Ticket
    # form_class = TicketForm


class CommentList(LoginRequiredMixin, CoreListView):
    model = Comment

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser and self.request.user.is_superuser:
            return Comment.objects.all()
        else:
            return Comment.objects.filter(user=self.request.user)


class CommentCreate(LoginRequiredMixin, AjaxCreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
    # def form_valid(self, form):
    #     """Force the user to request.user"""
    #     self.object = form.save(commit=False)
    #     self.object.user_id = self.request.user.id
    #     self.object.save()

        return super(CommentCreate, self).form_valid(form)


class CommentUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Comment
    form_class = CommentForm


class CommentDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Comment


class CommentDetail(LoginRequiredMixin, AjaxDetailView):
    model = Comment


class FileList(LoginRequiredMixin, CoreListView):
    model = File


class FileUpload(LoginRequiredMixin, AjaxFilesUpload):
    model = File
    form_class = FileForm


class FileDelete(LoginRequiredMixin, AjaxDeleteView):
    model = File
