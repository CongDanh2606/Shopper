from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Country

# Create your views here.
def update_account_view(request):

    user = request.user
    countries = Country.objects.all()
    if request.method == 'POST':
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        password = request.POST.get("password")

        if(password):
            user.set_password(password)
            update_session_auth_hash(request, user)
        user.id_country_id = request.POST.get("country")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")

        avatar = request.FILES.get("avatar")
        if avatar:
            if avatar.size > 1024 * 1024:
                return render(request, 'account_update.html', {
                    'user_info': user,
                    'countries': countries,
                    'error': 'Ảnh kích thước phải nhỏ hơn 1MB'
                })
            if not avatar.name.lower().endswith(('.png', '.jpeg', '.jpg')):
                return render(request, 'account_update.html', {
                    'user_info': user,
                    'countries': countries,
                    'error': 'Ảnh phải có định dạng (png, jpeg, jpg)'
                })
            user.avatar = avatar
        user.save()
        messages.success(request, 'Cập nhật thông tin tài khoản thành công!')
        return redirect('account_update')

    return render(request, 'account_update.html', {
        'user_info': user,
        'countries': countries,
    })
