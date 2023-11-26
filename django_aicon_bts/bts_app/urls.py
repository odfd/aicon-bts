# myapp/urls.py
from django.urls import path
from .views import main_view, get_image, generate_image, process_audio

urlpatterns = [
    path('', main_view, name='main_view'),
    path('get_image/', get_image, name='get_image'),
    path('generate_image/', generate_image, name='generate_image'),
    path('process_audio/', process_audio, name='process_audio'),
]
