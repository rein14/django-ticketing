from django.urls import path, include
from .views import *

app_name = 'app'

urlpatterns = [

    path('', home, name='home'),

    path('notifications/', NotificationList.as_view(), name='notication-list'),

    
    path('folder/', FolderList.as_view(), name='folder-list'),
    path('folder/<int:pk>/folder', FolderDetailView.as_view(), name='folder-detail'),
    path('folder/create/', FolderCreate.as_view(), name='folder-create'),
    path('folder/delete/<int:pk>/', FolderDelete.as_view(), name='folder-delete'),
    path('folder/update/<int:pk>/', FolderUpdate.as_view(), name='folder-update'),
    path('memo/createfolder/', MemoFolderCreate.as_view(), name='memo-folder-create'),


    path('user-list/', UserMemoList.as_view(), name='user-memo-list'),
    path('inbox/', InboxList.as_view(), name='inbox'),
    path('completed/', CompletedList.as_view(), name='completed-memos'),

    path('openmemos/', OpenMemosList.as_view(), name='open-memos'),
    path('unassigned/', UnassignedMemos.as_view(), name='unassigned-list'),
    path('archive/', ArchiveList.as_view(), name='memo-archive'),

    path('memos/', MemoList.as_view(), name='memo-list'),
    path('memo/create/', MemoCreate.as_view(), name='memo-create'),
    path('memo/update/<int:pk>/', MemoUpdate.as_view(), name='memo-update'),
    path('memo/statusupdate/<int:pk>/',
         MemoStatusUpdate.as_view(), name='memo-status-update'),
    path('memo/delete/<int:pk>/', MemoDelete.as_view(), name='memo-delete'),
    path('memo/<int:pk>/', MemoDetail.as_view(), name='memo-detail'),
    path('memo/<int:memo>/files', FileList.as_view(), name='file-list'),
    path('memo/<int:memo>/files/upload',
         FileUpload.as_view(), name='file-upload'),
    path('memo/<int:memo>/file/<int:pk>/delete/',
         FileDelete.as_view(), name='file-delete'),

    path('memo/<int:memo>/comments',
         CommentList.as_view(), name='comment-list'),
    path('memo/<int:memo>/comment/create/',
         CommentCreate.as_view(), name='comment-create'),
    path('memo/<int:memo>/comment/update/<int:pk>/',
         CommentUpdate.as_view(), name='comment-update'),
    path('memo/<int:memo>/comment/delete/<int:pk>/',
         CommentDelete.as_view(), name='comment-delete'),
    path('memo/<int:memo>/comment/<int:pk>/',
         CommentDetail.as_view(), name='comment-detail'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),

]
