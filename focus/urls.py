#from django.conf.urls import include,url
from focus import views
from django.urls import path ,include,re_path

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('login/',views.log_in,name="login"),
    path('logout/',views.log_out,name="logout"),
    path('<int:article_id>/comment/',views.comment,name="comment"),
    #re_path('(?P<article_id>[0-9]+)/comment/',views.comment,name="comment"),
    re_path('(?P<article_id>[0-9]+)/poll/',views.get_keep,name="keep"),
    #re_path('(?P<article_id>[0-9]+)/poll/',views.get_poll_article,name="poll"),
    #会拦截该链接的所有子链接
    #re_path('(?P<article_id>[0-9]+)/',views.article,name="article"),
    #在Python正则表达式中，命名式分组语法为 (?P<name>pattern) ，其中name为名称(<int:name>)， pattern为待匹配的模式。
    re_path('(?P<name>[0-9]+)/test/',views.re_test,name="re_test"),
    #re_path('(?P<article_id>[0-9]+)/get_comments/',views.get_comments,name="get_comments"),
    #会拦截该链接的所有子链接
    re_path('(?P<article_id>[0-9]+)/articles/',views.article,name="article"),
    path('<int:article_id>/get_comments/',views.get_comments,name="get_comments"),
    path('<int:comment_id>/<int:article_id>/',views.poll_comments,name="poll_comments"),
    path('<int:article_id>/get_poll_article/',views.get_poll_article,name="get_poll_article"),
    path('<int:user_id>/<int:comment_id>/comment_comment/',views.comment_comment,name="comment_comment"),
    #获取指定评论的所有回复
    path('<int:comment_id>/replys/',views.comment_replys,name="comment_replys"),

    
]