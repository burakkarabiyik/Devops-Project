from blog.models import Post
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AnonymousUser, User
from collections import defaultdict
from django.http import Http404, HttpResponse
from blogadmin.models import User
from blog.models import MyCategories
# Create your views here.


def yazarmi(request):
    if not request.user.is_authenticated:

        return False
    else:
        if request.user.is_yazar:
            return True
        else:
            return False


def adminmi(request):
    if not request.user.is_authenticated:
        return False
    if request.user.is_admin:
        return True
    else:
        return False


def login(request):

    if request.user.is_authenticated:
        return redirect('/')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if(request.POST):
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/admin/')
        else:
            pass
    return render(request, 'admin/login.html')


def blogadmin(request):

    if yazarmi(request):

        context = dict()
        context["makaleler"] = Post.objects.order_by("-publishing_date")
        a = Post.objects.all()

        appearances = defaultdict(int)
        for curr in a:
            appearances[curr.status] += 1

        context["UserList"] = User.objects.all()
        context["kategoriler"] = list(appearances.keys())
        context["degerler"] = list(appearances.values())
        return render(request, 'admin/index.html', context)


def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    ad = request.POST.get('ad')
    soyad = request.POST.get('soyad')
    if username:
        try:
            a = User.objects.get(username=username)
        except Exception as e:
            print(e)
            user = User.objects.create_user(
                username=username, password=password, ad=ad, soyad=soyad, yas=request.POST.get('yas'))

            return redirect('/login/')
    return render(request, 'admin/register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def products(request):
    if yazarmi(request):

        context = dict()
        context['makaleler'] = Post.objects.all()
        context['kategoriler'] = MyCategories.objects.all()

        return render(request, 'admin/products.html', context)


def add(request):
    if yazarmi(request):

        context = dict()
        context["kategoriler"] = MyCategories.objects.all()
        if(request.POST):
            if yazarmi(request):

                file = request.FILES['fileInput']
                fs = FileSystemStorage()
                image = fs.save('post/'+file.name, file)

                title = request.POST.get('name')
                icerik = request.POST.get('icerik')
                category = request.POST.get('category')
                post = Post.objects.create(
                    user=request.user, title=title, content=icerik, status=category, image=image)
                try:
                    post.save()
                    redirect('/admin/products/')
                except Exception as e:
                    print(e)

        return render(request, 'admin/add-product.html', context)


def productdetails(request, value):
    context = dict()
    makale = get_object_or_404(Post, slug=value)
    if request.POST:
        if yazarmi(request):

            file = request.FILES['fileInput']
            fs = FileSystemStorage()
            image = fs.save('post/'+file.name, file)

            title = request.POST.get('name')
            icerik = request.POST.get('icerik')
            category = request.POST.get('category')
            post = Post.objects.create(
                user=request.user, title=title, content=icerik, status=category, image=image)
            post.save()
            redirect('/admin/products/')
    context['makale'] = makale
    context['kategoriler'] = MyCategories.objects.all()
    context['slug'] = value
    return render(request, 'admin/edit-product.html', context)


def editsave(request):

    if request.POST:
        if yazarmi(request):

            makale = get_object_or_404(Post, slug=request.POST.get('slug'))

            if request.POST.get('degistimi') == '1':
                try:
                    file = request.FILES['fileInput2']
                    fs = FileSystemStorage()
                    image = fs.save('post/'+file.name, file)
                    makale.image = image
                except Exception as e:
                    print(e)
                    pass

            title = request.POST.get('name')
            icerik = request.POST.get('icerik')
            category = request.POST.get('category')
            makale.title = title
            makale.content = icerik
            makale.status = category
            makale.save()

            return redirect('/admin/products/')


def accounts(request):

    context = dict()
    context["users"] = User.objects.all()
    if request.POST:
        if adminmi(request):

            if(request.POST.get('username2')):
                username = request.POST.get('username2')
                user = User.objects.get(username=request.POST.get('username'))
                user.delete()
                return redirect("/admin/accounts/")
            user = User.objects.get(username=request.POST.get('username'))
            user.ad = request.POST.get('ad')
            user.username = request.POST.get('name')
            user.soyad = request.POST.get('soyad')
            if(request.POST.get('admin') == 'on'):
                user.is_admin = True
            else:
                user.is_admin = False
            if(request.POST.get('yazar') == 'on'):
                user.is_yazar = True
            else:
                user.is_yazar = False
            user.save()
            return redirect("/admin/")

    return render(request, 'admin/accounts.html', context)


def addcategory(request):
    if request.POST:
        if yazarmi(request):

            isim = request.POST.get("categoryname")
            if isim:

                kategori = MyCategories.objects.create(
                    categoryname=request.POST.get("categoryname"))
                kategori.save()
                return redirect('/admin/articles')
        else:
            return redirect('/admin/articles')
    return render(request, 'admin/add-kategori.html')


def deletemakale(request):

    if request.POST:
        if yazarmi(request):

            for key, value in request.POST.items():
                try:
                    makale = Post.objects.get(slug=key)
                    makale.delete()
                except Exception as e:
                    print(e)
                    pass

    return redirect("/admin/products/")


def deletecategory(request, categoryname):
    if adminmi(request):
        obje = MyCategories.objects.get(categoryname=categoryname)
        obje.delete()
        return redirect("/admin/products")
    else:
        return redirect('/admin/products')
