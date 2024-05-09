
from django.urls import path
from . import views
from django.views.generic import TemplateView



urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('admin_view/', views.admin_view, name='admin_view'),
    path('list/', views.user_list, name='user_list'),
    path('create/', views.create_user, name='create_user'),
    path('edit/<int:user_profile_id>/', views.edit_user, name='edit_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('login/', views.login_view, name='login'),
    path('project/create/', views.create_project, name='project_create'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:project_id>/edit/', views.edit_project, name='project_edit'),
    # path('project/<int:project_id>/delete/', views.delete_project, name='project_delete'),

    path('create_work_experience/', views.create_work_experience, name='create_work_experience'),
    path('edit_work_experience/<int:work_experience_id>/', views.edit_work_experience, name='edit_work_experience'),
    path('delete_work_experience/<int:work_experience_id>/', views.delete_work_experience,name='delete_work_experience'),

    path('create_education/', views.create_education, name='create_education'),
    path('edit_education/<int:education_id>/', views.edit_education, name='edit_education'),
    path('delete_education/<int:education_id>/', views.delete_education, name='delete_education'),

    path('certification/create/', views.create_certification, name='create_certification'),
    path('certification/edit/<int:certification_id>/', views.edit_certification, name='edit_certification'),
    path('certification/delete/<int:certification_id>/', views.delete_certification, name='delete_certification'),

    path('base/<int:user_profile_id>/', views.base_view, name='base_view'),


]

