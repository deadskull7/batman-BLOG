from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, ContactForm, SignUpForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .models import UserProfile
from .forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def post_list(request):
    query = request.GET.get("q")
    queryset_list = Post.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(author__username__icontains=query)|  # beacuse author is a foreign key as in models.py
            Q(content__icontains=query)
            ).distinct()

        posts = queryset_list
        return render(request, 'blog/search.html',{'posts': posts})

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


"""def email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'blog/email.html', {'form': form})


def thanks(request):
    return HttpResponse('Thank you for your message.')  """



def contact(request):
    if request.method == 'POST':
        # POST, generate bound form with data from the request
        form = ContactForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            # Insert into DB
            form.save()
            # redirect to a new URL:
            return HttpResponse("Great")
    else:
        # GET, generate unbound (blank) form
        form = ContactForm()
    return render(request,'blog/email.html',{'form':form})


def aboutme(request):
    return render(request,'blog/abme.html')


@login_required() # only logged in users should access this
def edit_user(request):
    # querying the User object with pk from url
    pk = request.user.pk
    user = User.objects.get(pk=pk)
 
    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)
 
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('website', 'bio', 'phone', 'city', 'country', 'organization'))
    formset = ProfileInlineFormset(instance=user)
 
    if request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST or None, request.FILES or None, instance=user)
            formset = ProfileInlineFormset(request.POST or None, request.FILES or None, instance=user)
 
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST or None, request.FILES or None, instance=created_user)
 
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('http://127.0.0.1:8000/')
 
        return render(request, "blog/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('http://127.0.0.1:8000/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'blog/change_password.html', 
        {'form': form}
    )


@login_required
def home(request):
    return render(request, 'blog/home.html')