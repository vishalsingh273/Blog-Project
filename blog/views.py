
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Blog, Comment, EmailSubscription
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login



def blog_list(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)
    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments})

@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def comment_on_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        comment = Comment.objects.create(blog=blog, user=request.user, text=text)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def share_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    subscribers = EmailSubscription.objects.filter(blog=blog)
    for subscriber in subscribers:
        send_mail(
            'Check out this blog!',
            f'Hi {subscriber.user.username},\n\n{blog.title}\n\n{blog.content}',
            'from@example.com',
            [subscriber.user.email],
            fail_silently=False,
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')  # Redirect to blog list after signup
        return render(request, self.template_name, {'form': form})



class CustomLoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Replace 'home' with the desired redirect URL after login
        return render(request, self.template_name, {'form': form})
