from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    path('details/<str:resume_id>/', views.details, name='details'),
    path('view_pdf/<str:resume_id>/', views.view_pdf, name='view_pdf'),
    path('upload/', views.upload, name='upload'),
    path('user/<int:user_id>/', views.user, name='user')

]