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
    likes = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)



    def save_image(self):
        self.save()


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
class Comments(models.Model):
    comment = HTMLField()
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk=id)
        return comments


