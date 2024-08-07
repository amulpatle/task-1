from django.db import models
from accounts.models import User
# Create your models here.


class BlogPost(models.Model):
    CATEGORY_CHOICES = (
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid-19', 'Covid-19'),
        ('Immunization', 'Immunization'),
    )
    title = models.CharField(max_length=255)
    image = models.ImageField()
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title