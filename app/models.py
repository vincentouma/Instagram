from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


# Create your models here.
#profile model
class Profile(models.Model):
    prof_pic = models.ImageField(upload_to='picture/',null=True)
    bio = HTMLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=1)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    class Meta:
        ordering = ['bio']

    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains=name)
        return profile

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user=id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile


#image model
class Image(models.Model):
    image = models.ImageField(upload_to='picture/',null=True)
    image_name = models.CharField(max_length=60)
    image_caption = models.TextField()
    Profile = models.ForeignKey(User,null=True)
    likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)



    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete() 

    @classmethod
    def search_by_profile(cls,search_term):
        picture = cls.objects.filter(profile__name__icontains=search_term)
        return picture

    @classmethod
    def pics(cls):
        image = cls.objects.all()
        return image

    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(Profile__pk = profile)
        return images
#coment model
class Comment(models.Model):
    comment = models.CharField(null = True, max_length= 5000, verbose_name = 'name')
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, null=True)
    image = models.ForeignKey(Image, null= True)

    class Meta:
        verbose_name = "comments"
        verbose_name_plural = "comments"
        ordering = ['-date']        

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

