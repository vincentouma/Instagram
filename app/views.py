from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Image, Profile,Comments
from django.contrib.auth.models import User
from .forms import SignupForm, ImageForm, ProfileForm, CommentForm, SigninForm
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .email import send_activation_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
@login_required(login_url='/accounts/login/')
def insta(request):
    post = Image.objects.all()
    return render(request,'insta.html',{"post":post})

def pics(request):
    pictures = Image.objects.all()

    return render(request, "insta.html", {"pictures": pictures})



def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        profiles = Profile.search_profile(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'profiles':profiles})
    else:
        message = 'Enter term to search'
        return render(request, 'search.html', {'message':message})


def profile(request, username):
    profile = User.objects.get(username=username)
    # print(profile.id)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Instagram photos and videos'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details, 'images':images})


@login_required(login_url='/accounts/login/')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.Profile = request.user
            upload.save()
        return redirect('profile', username=request.user)
    else:
        form = ImageForm()

    return render(request, 'profile/upload_image.html', {'form': form})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form': form})




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            to_email = form.cleaned_data.get('email')
            send_activation_email(user, current_site, to_email)
            return HttpResponse('Please activate your email')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='/accounts/login/')
def comment(request, image_id):

    image = Image.objects.get(id=image_id)

    if request.method == 'POST':
        current_user = request.user
        form = Comment(request.POST)
        if form.is_valid:
            comments = form.save(commit=False)
            comments.user = current_user
            comments.picture = image.id
            comments.save()

            return redirect('insta')
    else:
        form = Comment()

    comments = Comments.objects.filter(picture=image_id).all

    return render(request, "comment.html", {'form': form, "image": image, "comments": comments})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request)
        return redirect('login')
        return HttpResponse('Thank you for confirming email. Now login to your account')
    else:
        return HttpResponse('Activation link is invalid')

def login(request):
        form = SigninForm()

        
        return render(request, 'registration/login.html', {'form': form})
