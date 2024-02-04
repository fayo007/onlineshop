from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from main import models


def dashboard(request):
    categorys = models.Category.objects.all()
    products = models.Product.objects.all()
    users = User.objects.all()
    context = {
        'categorys':categorys,
        'products':products,
        'users':users,
    }
    return render(request, 'dashboard/index.html', context)


def create_category(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name=request.POST['name']
        )
        return redirect('dashboard:category')
    return render(request, 'dashboard/category/create.html')

def category_list(request):
    categorys = models.Category.objects.all()
    return render(request, 'category/list.html', {'categorys':categorys})


def category_detail(request, id):
    category = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=category, is_active=True)
    context = {
        'category':category,
        'products':products
    }
    return render(request, 'category/list.html', context)


def category_update(request, id):
    category = models.Category.objects.get(id=id)
    category.name = request.POST['name']
    category.save()
    return redirect('category_detail', category.id)


def category_delete(request, id):
    category = models.Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')


# products


def product_create(request):
    categorys = models.Category.objects.all()
    context = {
        'categorys':categorys
    }
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        quantity = request.POST['quantity']
        price = request.POST['price']
        currency = request.POST['currency']
        baner_image = request.FILES['baner_image']
        category_id = request.POST['category_id']
        images = request.FILES.getlist('images')
        product = models.Product.objects.create(
            name=name,
            description = description,
            quantity=quantity,
            price=price,
            currency=currency,
            baner_image=baner_image,
            category_id=category_id
        )
        for image in images:
            models.ProductImage.objects.create(
                image=image,
                product=product
            )

    return render(request, 'dashboard/products/create.html', context)




def product(request):
    product = models.Product.objects.all()
    context = {
        'product':product
    }
    return render(request, 'dashboard/product/list.html', context)


def product_update(request, id):
    product = models.Product.objects.get(id=id)
    if request.method == 'POST':
        category = models.Category.objects.get(id=request.POST['category_id'])
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.quantity = request.POST['quantity']
        product.price = request.POST['price']
        product.currency = request.POST['currency']
        # product.discount_price = request.POST['discount_price']
        product.category=category
        baner_image = request.FILES.get('product_image')
        if baner_image:
            product.baner_image = baner_image
        product.save()

    context = {
        'product':product,
        'categorys':models.Category.objects.all(),
    }
    return render(request, 'dashboard/product/update.html', context)


def product_delete(request, id):
    models.Product.objects.get(id=id).delete()
    return redirect('dashboard:product')