# myapp/urls.py
from django.urls import path
from .views import main_view, get_image, generate_image, process_audio, get_gpt_context_prompt

urlpatterns = [
    path('', main_view, name='main_view'),
    path('get_image/', get_image, name='get_image'),
    path('generate_image/', generate_image, name='generate_image'),
    path('process_audio/', process_audio, name='process_audio'),
    path('get_gpt_context_prompt/', get_gpt_context_prompt, name='get_gpt_context_prompt'),
]
