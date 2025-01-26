from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator




class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Review(models.Model):
    MEDIA_TYPES = [
        ('anime', 'Anime'),
        ('manga', 'Manga'),
        ('movie', 'Filme'),
        ('series', 'Série'),
        ('game', 'Jogo'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    media_title = models.CharField(max_length=200)
    review_title = models.CharField(max_length=200)
    review_text = models.TextField()
    rating = models.FloatField(
        validators=[
            MinValueValidator(0.5, "A nota mínima é 0.5"),
            MaxValueValidator(5.0, "A nota máxima é 5")
        ]
    )
    
    episode_number = models.CharField(max_length=50, blank=True, null=True)
    media_image = models.FileField(
        upload_to='review_media/', 
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])
        ]
    )
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.review_title} - {self.media_title}"