from django.shortcuts import render, redirect
from .models import Product, Brand, Category
from django.http import JsonResponse
from django.conf import settings
from PIL import Image
import json
import os

# Create your views here.

def my_product_view(request):
    products = Product.objects.filter(id_user=request.user)
    for product in products:
        if isinstance(product.image, str):
            try:
                product.image_filenames = json.loads(product.image)
            except json.JSONDecodeError:
                product.image_filenames = []
        elif isinstance(product.image, list):
            product.image_filenames = product.image
        else:
            product.image_filenames = []
    return render(request, 'myProduct.html', {
        'products': products,
    })

def add_product_view(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('productname')
        price = request.POST.get('productprice')
        category = request.POST.get('productcategory')
        brand = request.POST.get('productbrand')
        status = int(request.POST.get('productstatus'))
        sale = request.POST.get('productsale')
        company = request.POST.get('productcompany')
        files = request.FILES.getlist('productimages')
        detail = request.POST.get('productdetail')

        errors = {}
        if not name:
            errors['name'] = "Vui lòng nhập tên sản phẩm!"
        if not price:
            errors['price'] = "Vui lòng nhập giá sản phẩm!"
        else:
            try:
                price = float(price)
                if price < 0:
                    errors['price'] = "Giá sản phẩm phải lớn hơn 0, vui lòng nhập đúng!"
            except ValueError:
                errors['price'] = "Giá sản phẩm phải là dạng số, vui lòng nhập đúng!"
        if not category:
            errors['price'] = "Vui lòng chọn loại sản phẩm!"
        if not brand:
            errors['brand'] = "Vui lòng chọn thương hiệu sản phẩm!"
        if status ==  1 and not sale:
            errors['sale'] = "Vui lòng nhập phần trăm giảm giá sản phẩm!"
        if not company:
            errors['company'] = "Vui lòng nhập thông tin công ty sản xuất sản phẩm"
        if not files:
            errors['images'] = "Vui lòng chọn ít nhất 1 ảnh sản phẩm!"
        elif len(files) > 3:
            errors['images'] = "Chỉ được tải lên tối đa 3 ảnh sản phẩm!"
        else:
            for file in files:
                if file.content_type not in ['image/jpeg', 'image/png']:
                    errors['images'] = f"{file.name} không đúng định dạng ảnh hợp lệ"
                    break
                if file.size > 1024 * 1024:
                    errors['images'] = f"{file.name} ảnh không được quá 1MB"
                    break
        if not detail:
            errors['detail'] = "Vui lòng điền thông tin chi tiết sản phẩm!"
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
        saved_filenames = []
        for file in files:
            filename = file.name.replace(" ", "_")
            base, ext = os.path.splitext(filename)
            ext = ext.lower()
            save_folder = os.path.join(settings.MEDIA_ROOT, 'products')
            os.makedirs(save_folder, exist_ok=True)
            original_path = os.path.join(save_folder, f"{base}{ext}")
            with open(original_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            saved_filenames.append(f"{base}{ext}")
            img = Image.open(original_path)
            for size in [100, 200]:
                img_copy = img.copy()
                img_copy.thumbnail((size, size))
                resized_name = f"{size}_{base}{ext}"
                resized_path = os.path.join(save_folder, resized_name)
                img_copy.save(resized_path)
        Product.objects.create(
            id_user_id = request.user.id,
            name = name,
            price = price,
            id_category_id = category,
            id_brand_id = brand,
            status = status,
            sale = int(sale) if sale else 0,
            company = company,
            image = json.dumps(saved_filenames),
            detail = detail
        )
        return JsonResponse({
            'success': True,
            'status': 'success',
        })
    return render(request, 'addProduct.html', {
        'brands': brands,
        'categories': categories,
    })