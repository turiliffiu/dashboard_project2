from django.urls import path
from . import views

app_name = 'procedures'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/procedure/<str:filename>/', views.get_procedure_content, name='get_procedure'),
    path('api/upload/', views.upload_procedure_file, name='upload_file'),
    path('api/category/<int:category_id>/update/', views.update_procedure_category, name='update_category'),
    path('api/category/<int:category_id>/delete/', views.delete_procedure_category, name='delete_category'),
    path('api/category/<int:category_id>/update-file/', views.update_procedure_file, name='update_file'),
    path('api/category/<int:category_id>/download/', views.download_procedure_file, name='download_file'), 
]