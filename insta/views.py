from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignupForm,CommentForm, ImageForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Profile, Post


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    images=Post.objects.all()
    return render(request, 'index.html',{'images':images,})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/registration_form', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.' '<a href="/accounts/login/"> click here </a>')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='/accounts/register/')
def profile(request):
    images = request.user.profile.posts.all()
    user_object = request.user
    user_images = Post.get_user_img(user_object.id)
    return render(request, 'profile.html', locals())



def add_comment(request,post_id):
   post = get_object_or_404(Post, pk=post_id)
   if request.method == 'POST':
       form = CommentForm(request.POST)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.user = request.user
           comment.post = post
           comment.save()
   return redirect('index')


# def search_results(request):
#     if 'username' in request.GET and request.GET["username"]:
#         search_term = request.GET.get("username")
#         searched_users = Profile.objects.filter(username__icontains = search_term)
#         message = f"{search_term}"
#         profiles=  Profile.objects.all( )
        
#         return render(request, 'all-posts/search.html',{"message":message,"users": searched_users,'profiles':profiles})

#     else:
#         message = "You haven't searched for any term"
#         return render(request, 'all-posts/search.html',{"message":message})


def new_image(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = profile
            # image.profile = profile
            image.save()
        return redirect('index')

    else:
        form = ImageForm()
    return render(request, 'image.html', {"form": form})


