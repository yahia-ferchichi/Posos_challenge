from django.db import models

# Create your models here.
class Post(models.Model):
    x= models.CharField (max_length = 150)
    
    def __str__(self):
        return self.title
    
    
