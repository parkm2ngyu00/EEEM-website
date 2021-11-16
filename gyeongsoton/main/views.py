from typing import Text
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q, Count

from .models import communityText
from .models import manner
from .models import newterm
from .models import communityComment
from .models import certification
from .models import product
from .models import notification
from django.utils import timezone
from django.contrib import messages
import datetime
import random

# Create your views here.


def home(request):
    return render(request, "homepage.html")

#community
def community(request):
    community_alltext = communityText.objects.all()
    community_alltext = communityText.objects.order_by('-date')
    return render(request, "community.html", {"communities": community_alltext})


def communityDetail(request, id):
    community = get_object_or_404(communityText, pk=id)
    allComments = communityComment.objects.filter(communitytext=community)
    return render(
        request,
        "communityDetail.html",
        {"community": community, "comments": allComments},
    )


def addCommunity(request):
    if request.user.is_authenticated:
        community = communityText()
        community.date = timezone.datetime.now()
        community.like = 0
        community.dis_like = 0
        community.text = request.POST.get("communitytext")
        community.user = request.user
        community.title = request.POST.get("communitytitle")
        if community.text and community.title:
            community.save()
        return redirect("communityDetail", community.id)
    else:
        return redirect("404error")


def toaddCommunitypage(request):
    if request.user.is_authenticated:
        return render(request, "addCommunity.html")
    else:
        return redirect("404error")


def communityCommentLikeUp(request, community_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(communityComment, pk=comment_id)
        if request.user!= comment.user:
            comment.like += 1
            if not comment.getcoin:
                if comment.like==10:
                    comment.getcoin=True
                    comment.user.coin+=5
                    comment.user.save()
                    new_notification=notification()
                    new_notification.user=comment.user
                    new_notification.text="커뮤니티에 다신 댓글이 좋아요를 많이 받아 5💰을 드립니다"
                    new_notification.save()
            comment.save()
        return redirect("communityDetail", community_id)
    else:
        return redirect("404error")


def communityCommentDisLikeUp(request, community_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(communityComment, pk=comment_id)
        if request.user!= comment.user:
            comment.dis_like += 1
            comment.save()
        return redirect("communityDetail", community_id)
    else:
        return redirect("404error")

def toEditCommunitypage(request,id):
    edit_community=communityText.objects.get(pk=id)
    return render(request,'editCommunity.html',{'community':edit_community})

def communityEdit(request,id):
    if request.user.is_authenticated:
        edit_community=communityText.objects.get(pk=id)
        edit_community.text=request.POST.get('communitytext',False)
        edit_community.title=request.POST.get('communitytitle',False)
        edit_community.date=timezone.datetime.now()
        edit_community.writer=request.user
        edit_community.save()
        return redirect('communityDetail',edit_community.id)
    else:
        return redirect('404error')
    

def communityDelete(request, id):
    if request.user.is_authenticated:
        community = get_object_or_404(communityText, pk=id)
        if request.user != community.user:
            messages.error(request, '삭제권한이 없습니다')
            return redirect('communityDetail', id=community.id)
        community.delete()
        return redirect('community')  
    else:
        return redirect('404error')

def communitySelect(request,id):
    if request.user.is_authenticated:
        comment=get_object_or_404(communityComment,pk=id)
        comment.user.coin+=10
        comment.user.save()
        comment_notification=notification()
        comment_notification.user=comment.user
        comment_notification.text="커뮤니티에 다신 댓글이 채택을 받아 10💰을 드립니다"
        comment_notification.save()
        request.user.coin+=2
        request.user.save()
        comment_notification=notification()
        comment_notification.user=request.user
        comment_notification.text="커뮤니티에 다신 댓글을 채택하여 2💰을 드립니다"
        comment_notification.save()
        community=get_object_or_404(communityText,pk=comment.communitytext.id)
        community.selected=True
        community.save()
        return redirect('communityDetail',community.id)
    else:
        return redirect('404error')


def trend(request):
    return render(request, "trend.html")

#매너를 지켜쥬
def manners(request):
    manner_alltext = manner.objects.all()
    manner_alltext = manner.objects.order_by('-date')
    try:
        user_certification = certification.objects.get(user=request.user.id)
    except certification.DoesNotExist:
        user_certification=None
    return render(request, "manner.html", {"manner": manner_alltext,"user_certification":user_certification})


def mannerOrder(request):
    manner_alltext = manner.objects.all()
    manner_alltext = manner.objects.order_by('-like')
    return render(request, "mannerorder.html", {"manner": manner_alltext})


def mannersDetail(request, id):
    manner_detail = get_object_or_404(manner, pk=id)
    return render(request, "mannersDetail.html", {"mannersdetail": manner_detail})


def mannerLikeUp(request, id):
    if request.user.is_authenticated:
        manner_detail = get_object_or_404(manner, pk=id)
        if manner_detail.user!=request.user:
            manner_detail.like += 1
            manner_detail.save()
            if manner_detail.like==10 and not manner_detail.getcoin:
                manner_detail.getcoin=True
                manner_detail.user.coin+=5
                manner_detail.user.save()
                comment_notification=notification()
                comment_notification.user=manner_detail.user
                comment_notification.text="매너를 지켜쥬에 다신 댓글이 좋아요를 많이 받아 2💰을 드립니다"
                comment_notification.save()
    return redirect("mannersDetail", id)

def mannerDisLikeUp(request, id):
    if request.user.is_authenticated:
        manner_detail = get_object_or_404(manner, pk=id)
        if manner_detail.user!=request.user:
            manner_detail.dis_like += 1
            manner_detail.save()
    return redirect("mannersDetail", id)


def mannerSearch(request):
    if 'kw' in request.GET:
        query = request.GET.get('kw')
        result = manner.objects.all().filter(
            Q(hashtag_me__icontains=query) |
            Q(hashtag_you__icontains=query)
        )
    return render(request, "mannerSearch.html", {'query': query, 'result': result})


def addManner(request):
    if request.user.is_authenticated:
        try:
            user_certification = certification.objects.get(user=request.user.id)
        except certification.DoesNotExist:
            user_certification=None
        return render(request, "addmanner.html",{"user_certification":user_certification})
    else:
        return redirect('404error')


def mannerCreate(request):
    if request.user.is_authenticated:
        if(request.method == 'POST'):
            post = manner()
            post.user = request.user
            post.text = request.POST['title']
            try:
                user_certification = certification.objects.get(user=request.user.id)
                post.hashtag_me = user_certification.job
                request.user.coin+=20
                request.user.save()
                comment_notification=notification()
                comment_notification.user=request.user
                comment_notification.text="인증 후 매너를 지켜쥬에 글을 올리셔서 20💰을 드립니다"
                comment_notification.save()
                post.secret=True
            except certification.DoesNotExist:
                post.hashtag_me = request.POST.get('hashtagMe',False)
                post.secret=False
            post.hashtag_you = request.POST['hashtagYou']
            post.hashtag_situation = request.POST['body']
            post.like = 0
            post.dis_like = 0
            post.save()
            return redirect('manner')
    else:
        return redirect('404error')


def mannerdelete(request, id):
    if request.user.is_authenticated:
        question = get_object_or_404(manner, pk=id)
        if request.user != question.user:
            messages.error(request, '삭제권한이 없습니다')
            return redirect('manner', id=question.id)
        question.delete()
        return redirect('manner')
    else:
        return redirect('404error')

def newproductdelete(request, id):
    if request.user.is_authenticated:
        question = get_object_or_404(product, pk=id)
        if request.user != question.user:
            messages.error(request, '삭제권한이 없습니다')
            return redirect('newproduct', id=question.id)
        question.delete()
        return redirect('newproduct')
    else:
        return redirect('404error')

def toEditMannerpage(request,id):
    if request.user.is_authenticated:
        edit_manner=manner.objects.get(pk=id)
        return render(request,'editManner.html',{'manner':edit_manner})
    else:
        return redirect('404error')

def toEditnewproduct(request, id):
    if request.user.is_authenticated:
        editproduct=product.objects.get(pk=id)
        return render(request, 'editproduct.html', {'editproduct' : editproduct})
    else:
        return redirect('404error')

def mannerEdit(request,id):
    if request.user.is_authenticated:
        edit_manner=manner.objects.get(pk=id)
        edit_manner.text=request.POST.get('text',False)
        edit_manner.hashtag_situation=request.POST.get('hashtag_situation',False)
        edit_manner.date=timezone.datetime.now()
        edit_manner.writer=request.user
        edit_manner.save()
        return redirect('mannersDetail',edit_manner.id)
    else:
        return redirect('404error')


def productEdit(request,id):
    if request.user.is_authenticated:
        edit_product=product.objects.get(pk=id)
        edit_product.productName=request.POST.get('productName',False)
        edit_product.productText=request.POST.get('productText',False)
        edit_product.date=timezone.datetime.now()
        edit_product.user=request.user
        edit_product.save()
        return redirect('newproductDetail',edit_product.id)
    else:
        return redirect('404error')

#newterms
def newterms(request):
    newterm_quiz = newterm.objects.all()
    tYear = datetime.datetime.today().year
    return render(request, "newterms.html", {"new_term": newterm_quiz, "year": tYear})


def newtermQuiz(request, id):
    newtermsum = newterm.objects.count()-1
    newtermCount = int(id)-1
    if id == 0:
        term = get_object_or_404(newterm, pk=id)
    else:
        previousTerm = get_object_or_404(newterm, pk=id)
        termId = int(id) + 1
        term = get_object_or_404(newterm, pk=termId)
        term.score = previousTerm.score
    term.randanswer = random.randint(0, 1)
    term.save()

    if term.randanswer == 0:
        return render(
            request,
            "newtermQuiz.html",
            {"term": term, "choice_1": term.answer,
                "choice_2": term.non_answer, "newtermCount": newtermCount,"newtermsum":newtermsum},
        )
    else:
        return render(
            request,
            "newtermQuiz.html",
            {"term": term, "choice_1": term.non_answer,
                "choice_2": term.answer,"newtermCount": newtermCount,"newtermsum":newtermsum},
        )


def newtermEnd(request, score):
    tYear = datetime.datetime.today().year
    now = datetime.datetime.now()
    newtermCount = newterm.objects.count()-1
    if score > newtermCount*0.5:
        if score > newtermCount*0.7:
            level = 3
        else:
            level = 2
    else:
        level = 1
    return render(request, "newtermEnd.html", {"score": score, "newtermCount": newtermCount, "year": tYear, "now": now, "level": level})


def newtermButton1(request, id):
    term = get_object_or_404(newterm, pk=id)
    newtermCount = newterm.objects.count()
    if term.randanswer == 0:
        term.correct = True
        term.score += 1
        term.save()
    else:
        term.correct = False
        term.save()
    c = newtermCount
    if int(id) < c:
        return redirect("newtermQuiz", id)
    else:
        return redirect("newtermEnd", term.score)


def newtermButton2(request, id):
    term = get_object_or_404(newterm, pk=id)
    newtermCount = newterm.objects.count()
    if term.randanswer == 1:
        term.correct = True
        term.score += 1
        term.save()
    else:
        term.correct = False
        term.save()
    c = newtermCount
    if int(id) < c:
        return redirect("newtermQuiz", id)
    else:
        return redirect("newtermEnd", term.score)


def addComment(request, id):
    if request.user.is_authenticated:
        comment = communityComment()
        comment.date = timezone.datetime.now()
        comment.like = 0
        comment.dis_like = 0
        comment.text = request.POST.get("commenttext")
        comment.user = request.user
        if comment.text:
            comment.communitytext = get_object_or_404(communityText, pk=id)
            comment.save()
        return redirect("communityDetail", id)
    else:
        return redirect("404error")


def notfound(request):
    return render(request, "404error.html")

#신문물
def newproduct(request):
    new_product = product.objects.all()
    new_product = product.objects.order_by('-date')
    now = datetime.datetime.now()  # 현재 시간. ~분전 하고 싶어서 .!
    return render(request, "newproduct.html", {'products': new_product, 'now': now})


def newproductOrder(request):
    new_product = product.objects.all()
    new_product = product.objects.order_by('-like')
    now = datetime.datetime.now()  # 현재 시간. ~분전 하고 싶어서 .!
    return render(request, "newproductorder.html", {'products': new_product, 'now': now})


def newproductDetail(request, id):
    product_detail = get_object_or_404(product, pk=id)
    return render(request, "newproductDetail.html", {"productDetail": product_detail})


def communitySearch(request):
    if 'kw' in request.GET:
        query = request.GET.get('kw')
        result = communityText.objects.all().filter(
            Q(title__icontains=query) |
            Q(text__icontains=query)
        )
    return render(request, "communitySearch.html", {'query': query, 'result': result})

def newproductSearch(request):
    if 'kw' in request.GET:
        query = request.GET.get('kw')
        result = product.objects.all().filter(
            Q(productName__icontains=query)
        )
    return render(request, 'newProductSearch.html', {'query': query, 'result': result})

def productLikeUp(request, id):
    if request.user.is_authenticated:
        productDetail = get_object_or_404(product, pk=id)
        productDetail.like += 1
        productDetail.save()
        if productDetail.like == 10 and not productDetail.getcoin:
            productDetail.getcoin=True
            like_notification=notification()
            like_notification.user=productDetail.user
            like_notification.text="신문물 소개에 작성하신 글이 좋아요를 많이 받아 5💰을 드립니다"
            like_notification.save()
        return redirect("newproductDetail", id)
    else:
        return render(request, "404error.html")

def addProduct(request):
    return render(request, "addProduct.html")


def productCreate(request):
    if request.user.is_authenticated:
        if(request.method == 'POST'):
            post = product()
            post.user = request.user
            post.date = timezone.datetime.now()
            post.productName = request.POST['productName']
            post.productText = request.POST['productText']
            post.like = 0
            if 'image' in request.FILES:
                post.image=request.FILES['image']
                post.save()
                return redirect('newproductDetail',post.id)
        else:
            return redirect('newproduct')
    else:
        return redirect('404error')
    
def toCertification(request):
    return render(request,"certification.html")


def addCertification(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                old_user_cf = certification.objects.get(user=request.user.id)
                old_user_cf.delete()
            except certification.DoesNotExist:
                old_user_cf=None
            cf=certification()
            cf.user=request.user
            cf.job=request.POST['job']
            if 'image' in request.FILES:
                cf.image=request.FILES['image']
                cf.save()
            return redirect('manner')
    else:
        return redirect('404error')
    
def stopCertification(request):
    if request.user.is_authenticated:
        old_user_cf = certification.objects.get(user=request.user.id)
        old_user_cf.delete()
        return redirect('manner')
    else:
        return redirect('404error')
    


def minuscoin(request, id):
    manner_detail = get_object_or_404(manner, pk=id)
    if request.user.is_authenticated:
        if request.user.coin >= 3 :
            request.user.coin -= 3
            request.user.save()
            comment_notification=notification()
            comment_notification.user=request.user
            comment_notification.text="인증된 글을 열람하여 3💰을 사용하였습니다."
            comment_notification.save()
            return render(request, "mannersDetail.html", {"mannersdetail": manner_detail})

        else :
            return redirect('manner')
    else:
        return redirect('404error')

