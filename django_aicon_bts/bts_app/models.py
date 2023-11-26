from django.db import models

# Create your models here.


#store image url
class GeneratedImage(models.Model):
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.url  


#keep track of most recent generated image, with a foreign key to GeneratedImage, storing only the url of the most recent image, only a single row
class RecentImage(models.Model):
    image = models.ForeignKey(GeneratedImage, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url
    
#keep track of daily stats
class DailyStats(models.Model):
    date = models.DateField()
    num_generated = models.IntegerField()

    def __str__(self):
        return str(self.date) + " " + str(self.num_generated)
        
    def increment_num_generated(self):
        self.num_generated += 1
        self.save()


class AudioFile(models.Model):
    file = models.FileField(upload_to='audio_files/')

