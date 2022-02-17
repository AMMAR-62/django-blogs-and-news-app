from .serializers import BlogSerializer
from rest_framework import viewsets
from .forms import BlogForm, NewUserForm
from django.shortcuts import render, redirect
from .models import BlogModel

# Create your views here.
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


API_KEY = 'd0b69496c18e463f888a273cb521ea9f'


def home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home.html', context=context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {'form': AuthenticationForm()}
        return render(request, 'login.html', context)
    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return render(request, 'logout.html')


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request, "register.html", {"register_form": form})


@login_required(login_url='login')
def news(request):
    country = request.GET.get('country')
    category = request.GET.get('category')

    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
    else:
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']

    context = {
        'articles': articles,
    }

    return render(request, 'news.html', context)


@login_required(login_url='login')
def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context=context)


@login_required(login_url='login')
def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context=context)


@login_required(login_url='login')
def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            if form.is_valid():
                content = form.cleaned_data['content']

            BlogModel.objects.create(
                user=user, title=title, content=content, image=image)
            return redirect('/add-blog/')

    except Exception as e:
        print(e)
    return render(request, 'add_blog.html', context=context)


@login_required(login_url='login')
def blog_update(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)

        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title, content=content, image=image)

        context['blog_obj'] = blog_obj
        context['form'] = form
        return redirect(request, 'update_blog.html', context=context)

    except Exception as e:
        print(e)

    return redirect('/see-blog/')


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('/see-blog/')


class BlogViewSet(viewsets.ModelViewSet):
   queryset = BlogModel.objects.all()
   serializer_class = BlogSerializer


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email": user.email,
					'domain': '127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'shaikhmohammedammar62@google.com',
						          [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
                        
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})