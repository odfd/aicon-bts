

#function to update the generated image, recent image, and daily stats
from datetime import date
from .models import RecentImage, GeneratedImage, DailyStats


def update_image(image_url):
    #create new generated image object
    generated_image = GeneratedImage(url=image_url)
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