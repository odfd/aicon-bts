from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import AudioFileForm
from django.http import HttpResponse
from datetime import date

from django.conf import settings
from .models import GeneratedImage, DailyStats, RecentImage, AudioFile
from openai import OpenAI

from .utils import update_image

import os
from django.core.files import File

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


@csrf_exempt
@require_POST
def process_audio(request):
    form = AudioFileForm(request.POST, request.FILES)
    if form.is_valid():    
        
        #for each audiofile, get path and delete the file to make sure no audio is saved on the server
        for audio_file in AudioFile.objects.all():            
            audio_file_path = audio_file.file.path
            #delete the wav file, only if it exists
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            if os.path.exists(audio_file_path+ ".wav"):
                os.remove(audio_file_path+ ".wav")
            #delete the audio file object
            audio_file.delete()

        audio_file = form.save()

        # Rename the file to have a .wav extension
        old_path = audio_file.file.path
        new_path = os.path.splitext(old_path)[0] + '.wav'
        os.rename(old_path, new_path)


        # Make the API call using OpenAI Python client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=open(new_path, "rb"),
            response_format="text"
        )

        # Return the transcript as JSON response
        return JsonResponse({'transcript': transcript})

    return JsonResponse({'error': 'Invalid form data'}, status=400)