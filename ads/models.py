from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
# Create your models here.

class Ad(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, 'Title must be more than 2 chars')])
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Many-To-Many Field
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    through='Comment',
                                    related_name='comments_owned')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,                             
                                    through='Favorite',
                                    related_name='favorite_ads')
    #Picture

    picture = models.BinaryField(null= True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, 'Comment cant be less than 3 chars!')]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        if len(self.text) < 15: return self.text
        else: return self.text[:11] + '...'

class Favorite(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ad', 'owner')
    
    def __str__(self):
        return '%s likes %s'%(self.owner.username, self.ad.title[:10])