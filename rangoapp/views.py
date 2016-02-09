from django.shortcuts import render
from rangoapp.models import Category, Page
from rangoapp.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rangoapp/index.html', context_dict)


def about(request):
    count = request.session.get('visits')
    if not count:
        count = 0
    count += 1
    request.session['visits'] = count
    return render(request, 'rangoapp/about.html', {'visits': count})


def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass
    return render(request, 'rangoapp/category.html', context_dict)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rangoapp/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                instance = form.save(commit=False)
                instance.category = cat
                instance.save()
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()
    context_dict = {'form': form, 'category': cat}
    return render(request, 'rangoapp/add_page.html', context_dict)


#custom auth no longer needed, now using django-registration-redux package
# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#     return render(request, 'rangoapp/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 return HttpResponse('Your rango account is disabled.')
#         else:
#             print("Invalid login details {0}, {1}".format(username, password))
#             return HttpResponse('Invalid login details supplied.')
#     else:
#         return render(request, 'rangoapp/login.html', {})


# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/rango/')
