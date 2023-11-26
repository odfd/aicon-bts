from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

from django.conf import settings
from .models import GeneratedImage, DailyStats, RecentImage
from openai import OpenAI

from .utils import update_image

def generate_image(request):
    #if image_prompt is empty, return error
    if request.method == 'POST':
        image_prompt = request.POST.get('image_prompt')
        if image_prompt == "":
            return HttpResponse("Error: image_prompt cannot be empty")

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        response = client.images.generate(
            model="dall-e-3",
            prompt= image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            )

        image_url = response.data[0].url

        update_image(image_url)

        return HttpResponse(image_url)
    return HttpResponse("Error: image_prompt variable not found")

def main_view(request):
    return render(request, 'main_view.html')


#gets the image url of the most recent generated image
def get_image(request):
    #get most recent generated image
    recent_image = GeneratedImage.objects.all().order_by('-id')[0]    
    #return the url of the most recent generated image
    return HttpResponse(recent_image.url)