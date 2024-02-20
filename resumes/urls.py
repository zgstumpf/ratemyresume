from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    path('details/<int:resume_id>/', views.details, name='details'),
    path('view_pdf/<int:resume_id>/', views.view_pdf, name='view_pdf'),
    path('upload', views.upload, name='upload'),

]