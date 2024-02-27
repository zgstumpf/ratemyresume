from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('details/<str:resume_id>/', views.details, name='details'),
    path('view_pdf/<str:resume_id>/', views.view_pdf, name='view_pdf'),
    path('upload/', views.upload, name='upload'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('groups/create/', views.creategroup, name='creategroup'),
    path('group/<str:group_id>/', views.grouppage, name='grouppage'),
    path('groups/', views.groups, name='groups'),
    path('invite/<str:group_id>/', views.sendinvite, name='sendinvite'),
    path('acceptinvite/<str:invite_id>/', views.acceptinvite, name='acceptinvite'),
    path('rejectinvite/<str:invite_id>/', views.rejectinvite, name='rejectinvite'),
    path('join/<str:group_id>/', views.sendrequest, name='sendrequest'),
    path('acceptrequest/<str:joinRequest_id>/', views.acceptrequest, name='acceptrequest'),
    path('rejectrequest/<str:joinRequest_id>/', views.rejectrequest, name='rejectrequest'),

]