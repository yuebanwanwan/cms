from django.shortcuts import render, redirect, get_object_or_404
from focus.models import *
from focus.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import markdown2
from urllib.parse import urlparse,urljoin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from django.http import HttpResponse
# Create your views here.

def index(request):
    #按文章的发布时间顺序(升序或者逆序)获取文章的列表
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    #将数据封装到字典中
    context = {'latest_article_list':latest_article_list,'loginform':loginform}
    #可直接传递字典对象
    return render(request,'focus/index.html',context)

def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'focus/login.html',{'form':form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #验证输入的数据是否合法
        if form.is_valid():
            username = form.cleaned_data['uid']
            print(username)
            password = form.cleaned_data['pwd']
            print(password)
            #user = NewUser.objects.get_or_create(username=username,password=password)
            user = authenticate(username=username,password=password)
            if user==None:
                #让非superuser也能通过认证

                user = NewUser.objects.get(username=username,password=password)
                #user = NewUser.objects.get_or_create(username=username, password=password)[0]
            #发现只有创建的superuser才能通过认证
            if user:

                login(request,user)
                url = request.POST.get('source_url','/focus')
                return redirect(url)
            else:
                return render(request,'focus/login.html',{'form':form,'error':'用户名或密码错误!'})
        else:
            return render(request,'focus/login.html',{'form':form})


# decorator只处理登录的用户
@login_required
def log_out(request):

    url = request.POST.get('source_url','/focus/')
    logout(request)
    return redirect(url)

# 判断访问的用户是否已经赞过该文章
def article(request,article_id):
    logged_user = request.user
    article = get_object_or_404(Article, id=article_id)
    # 获取该用户对每篇文章的点赞记录
    polls = logged_user.poll_set.all()
    articles = []
    # 获取已点赞的文章集合
    for poll in polls:
        articles.append(poll.article)
    # 如果已经点赞
    ispoll = False
    if article in articles:
        ispoll = True
    print('111')

    #获取用户已经点赞的评论
    is_poll_comments = logged_user.comment_set.all()
    #article = get_object_or_404(Article,id=article_id)
    content = markdown2.markdown(article.content,extras=["code-friendly",
        "fenced-code-blocks","header-ids","toc","metadata"])
    commentform = CommmentForm()
    loginform = LoginForm()
    #这TM是如何关联的(在一对多关系中，一的一方可以直接通过多的一方的Model名称+_set.all()获取？)
    comments = article.comment_set.all()





    return render(request,'focus/my_article_page.html',{
        'article': article,
		'loginform':loginform,
		'commentform':commentform,
		'content': content,
		'comments': comments,
        'ispoll':ispoll,
        'is_poll_comments':is_poll_comments,
    })

@login_required
def comment(request,article_id):
    form = CommmentForm(request.POST)
    #url = urlparse.urljoin('/focus/',article_id)
    if form.is_valid():
        user = request.user
        article = Article.objects.get(id=article_id)
        new_comment = form.cleaned_data['comment']
        c = Comment(content=new_comment,article_id=article_id)
        c.user = user
        c.save()
        article.comment_num += 1
    return redirect("/focus/" + str(article_id) + "/articles/")

@login_required
def get_keep(request,article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    articles = logged_user.article_set.all()
    if article not in articles:
        article.user.add(logged_user)
        article.keep_num += 1
        article.save()

        return redirect('/focus/')
    else:
        url = urlparse.urljoin('/focus/',article_id)
        return redirect(url)

@login_required
def get_poll_article(request,article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    polls = logged_user.poll_set.all()
    articles = []
    for poll in polls:
        articles.append(poll.article)
    # 如果以及点赞就直接刷新页面
    if article in articles:
        #url = urlparse.urljoin('/focus/',article_id)
        return redirect("/focus/" + str(article_id) + "/articles/")
    else:
        article.poll_num+=1
        #拿出来更新直接保存就OK？NB
        article.save()
        poll = Poll(user=logged_user,article=article)
        poll.save()
        data={}
        return redirect('/focus/' + str(article_id) + '/articles/')

def register(request):
    error1 = "用户名已存在"
    valid = "该用户名可用"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'focus/register.html',{'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':  # if ajax
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'focus/register.html', {'form': form, 'msg': valid})
            else:
                return render(request, 'focus/register.html', {'form': form, 'msg': error1})

        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'focus/register.html', {'form': form, 'msg': "two password is not equal"})
                else:
                    user = NewUser(username=username, email=email, password=password1)
                    user.save()
                    # return render(request, 'login.html', {'success': "you have successfully registered!"})
                    return redirect('/focus/login')
            else:
                return render(request, 'focus/register.html', {'form': form})



def re_test(request,name):
    string = 'Are you ok!'
    return render(request,'focus/login.html',{'string':string})


def get_comments(request,article_id):
    print('get_comments')
    comment_list = []
    for i in Comment.objects.filter(article=article_id):
        comment_list.append([i.content,i.pub_date])
    return JsonResponse(comment_list,safe=False)

@login_required
def poll_comments(request,comment_id,article_id):
    logged_user = request.user
    comments = Comment.objects.filter(id=comment_id)[:1]
    for comment in comments:
        Comment.objects.filter(id=comment_id).update(poll_num=comment.poll_num + 1)
    return redirect("/focus/" + str(article_id) + "/articles/")


class MyBackend(object):
    def authenticate(self,request,username=None,password=None,**kwargs):
        print('Mybackend')
        user  = NewUser.objects.get_or_create(username=username,password=password)
        if user:
            return user
        return None

    def get_user(self,user_id):
        try:
            return NewUser.objects.get(id=user_id)
        except NewUser.DoesNotExist:
            return None


def comment_comment(request,user_id,comment_id):
    print(request.POST)
    user = NewUser.objects.get(id=user_id)
    comment = Comment.objects.get(id=comment_id)
    object_comment_comment = Comment_comment(user=user,comment=comment,content=request.POST.get("postcomment"))
    object_comment_comment.save()
    article_id = request.POST['articleid']
    return redirect("/focus/" + str(article_id) + "/articles/")


def comment_replys(request,comment_id):
    from django.core import serializers
    comment = Comment.objects.get(id=comment_id)
    replys = comment.comment_comment_set.all()
    reply_list = []
    for i in replys:
        reply_list.append([i.user.id,i.content])
        #print(type(i.content))
    print(reply_list)
    #reply_list = serializers.serialize("json",reply_list)
    # 添加safe=False是为了让非字典对象变得可序列化，缺点就是Django不保证安全
    return JsonResponse(reply_list,safe=False)



















































