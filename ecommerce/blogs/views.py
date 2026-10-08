from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Blog, Rate, Comment


# Create your views here.
def blogs_view(request):

    blogs = Blog.objects.all()

    context = {
        'blogs': blogs
    }

    return render(request, 'blogs/blogs.html', context)

def blog_detail_view(request, id):

    blog = get_object_or_404(Blog, id=id)

    all_blogs = list(Blog.objects.all().order_by('id'))

    current_blog = 0

    for index, item in enumerate(all_blogs):
        if item.id == blog.id:
            current_blog = index
            break

    prev_blog = None
    next_blog = None

    if current_blog > 0:
        prev_blog = all_blogs[current_blog - 1]

    if current_blog < len(all_blogs) - 1:
        next_blog = all_blogs[current_blog + 1]

    rates = Rate.objects.filter(blog=blog)
    vote_count = rates.count()
    if vote_count > 0:
        total_score = sum(r.rate for r in rates)
        avg_rating = round(total_score / vote_count, 1)
    else:
        avg_rating = 0

    all_comments = Comment.objects.filter(blog=blog).order_by('created_at')
    parent_comments = []

    for cmt in all_comments:
        if cmt.level == 0:
            parent_comments.append(cmt)
            cmt.replies = []

    for cmt in all_comments:
        if cmt.level > 0:
            for p in parent_comments:
                if p.id == cmt.level:
                    p.replies.append(cmt)
                    break

    comments = Comment.objects.filter(blog=blog).order_by('created_at')

    context = {
        'blog': blog,
        'prev_blog': prev_blog,
        'next_blog': next_blog,
        'vote_count': vote_count,
        'avg_rating': avg_rating,
        'parent_comments': parent_comments,
        'comments': comments,
    }

    return render(request, 'blogs/blog_detail.html', context)

def blog_rate(request):

    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        rate = request.POST.get('rate')
        author_id = request.POST.get('author_id')
        try:
            blog = Blog.objects.get(id=blog_id)
            Rate.objects.update_or_create(
                blog_id=blog_id,
                user_id=author_id,
                defaults={'rate': int(rate)}
            )
            return JsonResponse({
                'success': True
            })

        except Blog.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Blog not found'
            })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })

def blog_comment(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        cmt = request.POST.get('comment')
        level = request.POST.get('level', 0)

        try:
            blog = Blog.objects.get(id=blog_id)

            new_comment = Comment.objects.create(
                blog=blog,
                user=request.user,
                cmt=cmt,
                level=int(level)
            )

            avatar_url = request.user.avatar.url if hasattr(request.user, 'avatar') and request.user.avatar else '/static/images/blog/man-two.jpg'

            return JsonResponse({
                'success': True,
                'comment_id': new_comment.id,
                'comment': new_comment.cmt,
                'user_name': request.user.username,
                'avatar': avatar_url,
                'hour': new_comment.created_at.strftime("%H:%M"),
                'time': new_comment.created_at.strftime("%d/%m/%Y")
            })

        except Blog.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Blog not found'
            })
        
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })