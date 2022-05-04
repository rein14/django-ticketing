from multiprocessing import context
from pyexpat import model
from re import template
from unicodedata import category
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import Folder, Ticket, Comment, File
from .forms import TicketForm, CommentForm, FileForm, TicketUpdateForm,TicketStatusUpdateForm, TicketDetailForm,CategoryForm
from cms.ajax import (AjaxCreateView, AjaxDetailView,
                      AjaxUpdateView, AjaxDeleteView, AjaxFilesUpload)
from cms.views import CoreDetailView, CoreListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# from django.views.generic.list import ListView
from account.models import User
from .permissions import permit_if_role_in
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView,DetailView

from webpush import send_user_notification

def handler404(request, exception):
    return render(request, 'blank.html')



@login_required
def home(request):
    # return render(request, 'blank.html', context={'title': 'Blank page'})
    if request.user.is_cleared:
        return redirect('app:ticket-list')

    elif not request.user.is_cleared:
        return redirect('app:inbox')
    # return redirect('app:inbox')


class FolderList(LoginRequiredMixin, CoreListView):
    model = Folder
 

class FolderDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Folder


class FolderCreate(LoginRequiredMixin, AjaxCreateView):
    model = Folder
    form_class = CategoryForm

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    # def get_redirect_url(self):
    #     return reverse_lazy('app:home')



class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Folder

   
    # Add the product of this category to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # This line retrieve all the products of this category
        if self.request.user.is_cleared: 
            context['tickets'] = Ticket.objects.filter(folder=self.object)
        else:
            context['tickets'] = Ticket.objects.filter(folder=self.object).filter(assigned_to=self.request.user)
        return context


# class TicketList(LoginRequiredMixin, CoreListView):
#     model = Ticket

#     def get_queryset(self):
#         if self.request.user.is_cleared:
#            # folders = get_object_or_404(Folder, self.)
#             return Ticket.objects.all()
#         else:
#             return Ticket.objects.filter(assigned_to=self.request.user)
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(TicketList, self).get_context_data(*args, **kwargs)
#         new_context_entry = "All Tickets"
#         context["title"] = new_context_entry
#         return context


class TicketList(LoginRequiredMixin, CoreListView):
    model = Ticket

    def get_context_data(self, *args, **kwargs):
        context = super(TicketList, self).get_context_data(*args, **kwargs)
        new_context_entry = "All Memos"
        context["title"] = new_context_entry
        return context

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserTicketList(LoginRequiredMixin, CoreListView):
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(UserTicketList, self).get_context_data(*args, **kwargs)
        new_context_entry = "Pending Memos"
        context["title"] = new_context_entry
        return context


class UnassignedTickets(LoginRequiredMixin, CoreListView):
    model = Ticket

    @permit_if_role_in(['is_cleared', ])
    # @method_decorator(user_is_registrar)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        users = User.objects.all()
        return Ticket.objects.all().exclude(assigned_to__in=users)

    def get_context_data(self, *args, **kwargs):
        context = super(UnassignedTickets, self).get_context_data(
            *args, **kwargs)
        new_context_entry = "Unassigned Memos"
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
        new_context_entry = "Completed memos"
        context["title"] = new_context_entry
        return context


class ArchiveList(LoginRequiredMixin, CoreListView):
    model = Ticket
    context_object_name = 'archive_list'

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

    @permit_if_role_in(['is_cleared', ])
    # @method_decorator(user_is_registrar)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(OpenTicketsList, self).get_context_data(
            *args, **kwargs)
        new_context_entry = "Open Tickets"
        context["title"] = new_context_entry
        return context

from notifications.signals import notify

class TicketCreate(LoginRequiredMixin, AjaxCreateView):
    model = Ticket
    form_class = TicketForm

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    # def get_redirect_url(self):
    #     return reverse_lazy('app:home')

    def form_valid(self, form):
        my_object = form.save()

        ticket = get_object_or_404(Ticket, id=my_object.id)

    #     notification_subject = " New Ticket"
    #     notification_body = "Hello,\n\n A new ticket ticket  (" + form.data['title'] +")" \
    #     +" See details at " "http://localhost:8000/inbox/" 
        
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = ['richmondnyamekye14@gmail.com', ]
    #     send_mail(notification_subject, notification_body,
    #               email_from, recipient_list)


    #     # notification_body = "Hi,\n\n a new comment has bee to ticket #" \
    #     #     + str(ticket.id) \
    #     #     + " (http://localhost:8000/ticket/" \
    #     #     + str(ticket.id) \
    #     #     + "/)\n\nTitle: " + str(ticket.user) \
    #     #     + "\n\n" + form.data['comment']
        sender = User.objects.get(id=1)
        recipient = User.objects.get(id=1)

        
        from webpush import send_user_notification

        user = self.request.user

        payload = {"head": "New Ticket", "body": ticket.title}
        send_user_notification(user=user, payload=payload, ttl=1000)
        notify.send(sender, recipient=recipient, verb=ticket.title,description=ticket.description)

        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()

    #     if form.is_valid():
    #         form.save()

    #         ticket = self.object

    #         # mail notification to owner of ticket
    #         # notification_subject = "[#"  + "] New followup"
    #         # notification_body = "Hi,\n\n new followup created for ticket #" \
    #         #                     + str('ticket.id') \
    #         #                     + " (http://localhost:8000/ticket/" \
    #         #                     + str('jdks') \
    #         #                     + "/)\n\nTitle: " + form.data['title'] \
    #         #                     + "\n\n" + form.data['description']

    #         subject = 'welcome to GFG world'
    #         # message = f'Hi {''}, thank you for registering in geeksforgeeks.'
    #         message = 'Hi, thank you for registering in geeksforgeeks.'
    #         email_from = settings.EMAIL_HOST_USER
    #         recipient_list = ['richmondnyamekye14@gmail.com', ]
    #         send_mail(subject, message, email_from, recipient_list)

    #     return super(TicketDetail, self).post(request, *args, **kwargs)


class TicketUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Ticket
    form_class = TicketUpdateForm

    def form_valid(self, form):

            form.instance.user = self.request.user

            my_object = form.save()

            ticket = get_object_or_404(Ticket, id=my_object.id)

            # notification_subject = "[#" +  "] New followup"
            # notification_body = "Hi,\n\n a new comment has been to ticket #" \
            #     + str(ticket.id) \
            #     + " (http://localhost:8000/ticket/" \
            #     + str(ticket.id) \
            #     + "/)\n\nTitle: " + str(ticket.user) \
            #     + "\n\n" + form.data['comment']
            # # message = f'Hi {''}, thank you for registering in geeksforgeeks.'
            # # message = 'Hi, thank you for registering in geeksforgeeks.'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = ['richmondnyamekye14@gmail.com', ]
            # send_mail(notification_subject, notification_body,
            #           email_from, recipient_list)
            sender = User.objects.get(id=1)
            recipient = User.objects.get(id=1)

            
            from webpush import send_user_notification

            user = self.request.user
            payload = {"head": 'Status update', "body": 'Status update for: '+ ticket.title}
            send_user_notification(user=user, payload=payload, ttl=1000)
            notify.send(sender, recipient=recipient, verb='Status Update', description='Status update for '+ ticket.title)

            return super().form_valid(form)


class TicketStatusUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Ticket
    form_class = TicketStatusUpdateForm


    def form_valid(self, form):

        form.instance.user = self.request.user

        my_object = form.save()

        ticket = get_object_or_404(Ticket, id=my_object.id)

        # notification_subject = "[#" +  "] New followup"
        # notification_body = "Hi,\n\n a new comment has been to ticket #" \
        #     + str(ticket.id) \
        #     + " (http://localhost:8000/ticket/" \
        #     + str(ticket.id) \
        #     + "/)\n\nTitle: " + str(ticket.user) \
        #     + "\n\n" + form.data['comment']
        # # message = f'Hi {''}, thank you for registering in geeksforgeeks.'
        # # message = 'Hi, thank you for registering in geeksforgeeks.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ['richmondnyamekye14@gmail.com', ]
        # send_mail(notification_subject, notification_body,
        #           email_from, recipient_list)
        sender = User.objects.get(id=1)
        recipient = User.objects.get(id=1)

        
        from webpush import send_user_notification

        user = self.request.user
        payload = {"head": 'Status update', "body": 'Status update for: '+ ticket.title}
        send_user_notification(user=user, payload=payload, ttl=1000)
        notify.send(sender, recipient=recipient, verb='Status Update', description='Status update for '+ ticket.title)

        return super().form_valid(form)


class TicketDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Ticket


class TicketDetail(LoginRequiredMixin, AjaxDetailView):
    model = Ticket
    form_class = TicketDetailForm

    # form_class = TicketForm
    def get_context_data(self, *args, **kwargs):
        context = super(TicketDetail, self).get_context_data(
            *args, **kwargs)
        b = Ticket.objects.get(pk=self.object.id)
        # b = Ticket.objects.all()
        # new_context_entry = "Open Tickets"
        context["comment_overlap"] = 'none of your business'
        context["comment_count"] = b.comment_set.all()
        context["file_count"] = b.file_set.all()
        return context


class CommentList(LoginRequiredMixin, CoreListView):
    model = Comment

    def get_queryset(self, **kwargs):
        if self.request.user.is_cleared:
            return Comment.objects.all()
        else:
            return Comment.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

   

class CommentCreate(LoginRequiredMixin, AjaxCreateView):
    model = Comment
    form_class = CommentForm

    # @permit_if_role_in(['is_cleared', ])
    # @method_decorator(user_is_registrar)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

   

    def form_valid(self, form):

        form.instance.user = self.request.user

        my_object = form.save()

        comment = get_object_or_404(Comment, id=my_object.id)

        # notification_subject = "[#" +  "] New followup"
        # notification_body = "Hi,\n\n a new comment has been to ticket #" \
        #     + str(ticket.id) \
        #     + " (http://localhost:8000/ticket/" \
        #     + str(ticket.id) \
        #     + "/)\n\nTitle: " + str(ticket.user) \
        #     + "\n\n" + form.data['comment']
        # # message = f'Hi {''}, thank you for registering in geeksforgeeks.'
        # # message = 'Hi, thank you for registering in geeksforgeeks.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ['richmondnyamekye14@gmail.com', ]
        # send_mail(notification_subject, notification_body,
        #           email_from, recipient_list)
        sender = User.objects.get(id=1)
        recipient = User.objects.get(id=1)

        
        from webpush import send_user_notification

        user = self.request.user
        payload = {"head": 'New comment for '+ str(comment.ticket), "body": comment.comment}
        send_user_notification(user=user, payload=payload, ttl=1000)
        notify.send(sender, recipient=recipient, verb='COMMENT', description=comment.comment)

        return super().form_valid(form)

    # def form_valid(self, form):
    #     """Force the user to request.user"""
    #     self.object = form.save(commit=False)
    #     self.object.user_id = self.request.user.id
    #     self.object.save()

    #     return super(CommentCreate, self).form_valid(form)


class CommentUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Comment
    form_class = CommentForm

    # @method_decorator(user_is_commissioner)
    # @method_decorator(user_is_registrar)
    @permit_if_role_in(['is_cleared', ])
    # @method_decorator(user_is_registrar)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CommentDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Comment


class CommentDetail(LoginRequiredMixin, AjaxDetailView):
    model = Comment

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, *args, **kwargs):
        self.event = 'detail'
        self.template = 'comment_detail'
        return super().dispatch(*args, **kwargs)

    

class FileList(LoginRequiredMixin, CoreListView):
    model = File

    #@permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class FileUpload(LoginRequiredMixin, AjaxFilesUpload):
    model = File
    form_class = FileForm

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class FileDelete(LoginRequiredMixin, AjaxDeleteView):
    model = File

    @permit_if_role_in(['is_cleared', ])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserDetail(LoginRequiredMixin, AjaxDetailView):
    model = User


