from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from .models import GeneratedImage, DailyStats, RecentImage

def main_view(request):
    #create new generated image object
    generated_image = GeneratedImage(url="https://upload.wikimedia.org/wikipedia/commons/2/25/Blisk-logo-512-512-background-transparent.png")
    generated_image.save()

    #update most recent generated image
    #get most recent generated image, or create new one if none exist
    recent_image = RecentImage.objects.all().first()
    if recent_image is None:
        recent_image = RecentImage(image=generated_image)
    else:
        recent_image.image = generated_image
    recent_image.save()

    #update daily stats
    #get today's date    
    today = date.today()
    #get today's daily stats
    daily_stats = DailyStats.objects.filter(date=today)
    #if today's daily stats already exist, increment num_generated
    if daily_stats.exists():
        daily_stats[0].increment_num_generated()
    #else create new daily stats
    else:
        daily_stats = DailyStats(date=today, num_generated=1)
        daily_stats.save()

    #return the generated image
    return HttpResponse(generated_image.url)


#gets the image url of the most recent generated image
def get_image(request):
    #get most recent generated image
    recent_image = GeneratedImage.objects.all().order_by('-id')[0]    
    #return the url of the most recent generated image
    return HttpResponse(recent_image.url)