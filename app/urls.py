from django.urls import path, include
from .views import *

app_name = 'app'

urlpatterns = [

    path('', home, name='home'),
    path('category/', Category.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('user-list/', UserTicketList.as_view(), name='user-ticket-list'),
    path('inbox/', InboxList.as_view(), name='inbox'),
    path('completed/', CompletedList.as_view(), name='completed-tickets'),

    path('tickets/', TicketList.as_view(), name='ticket-list'),
    path('opentickets/', OpenTicketsList.as_view(), name='open-tickets'),
    path('unassigned/', UnassignedTickets.as_view(), name='unassigned-list'),
    path('archive/', ArchiveList.as_view(), name='ticket-archive'),


    path('ticket/create/', TicketCreate.as_view(), name='ticket-create'),
    path('ticket/update/<int:pk>/', TicketUpdate.as_view(), name='ticket-update'),
    path('ticket/statusupdate/<int:pk>/',
         TicketStatusUpdate.as_view(), name='ticket-status-update'),

    path('ticket/delete/<int:pk>/', TicketDelete.as_view(), name='ticket-delete'),
    path('ticket/<int:pk>/', TicketDetail.as_view(), name='ticket-detail'),

    path('ticket/<int:ticket>/files', FileList.as_view(), name='file-list'),
    path('ticket/<int:ticket>/files/upload',
         FileUpload.as_view(), name='file-upload'),
    path('ticket/<int:ticket>/file/<int:pk>/delete/',
         FileDelete.as_view(), name='file-delete'),

    path('ticket/<int:ticket>/comments',
         CommentList.as_view(), name='comment-list'),
    path('ticket/<int:ticket>/comment/create/',
         CommentCreate.as_view(), name='comment-create'),
    path('ticket/<int:ticket>/comment/update/<int:pk>/',
         CommentUpdate.as_view(), name='comment-update'),
    path('ticket/<int:ticket>/comment/delete/<int:pk>/',
         CommentDelete.as_view(), name='comment-delete'),
    path('ticket/<int:ticket>/comment/<int:pk>/',
         CommentDetail.as_view(), name='comment-detail'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),

]
