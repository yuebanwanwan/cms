from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.utils.encoding import python_2_unicode_compatible
from cms import settings

class ArticleManager(models.Manager):

    def query_by_column(self,column_id):
        query = self.get_queryset().filter(column_id=column_id)

    def query_by_user(self,user_id):
        user = User.Objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list

    def query_by_polls(self):
        query = self.get_queryset().order_by('poll_num')
        return query

    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_by_keyword(self,keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query





# Create your models here.
@python_2_unicode_compatible
class NewUser(AbstractUser):
    profile = models.CharField('profile',default='',max_length=256)
    
    def __str__(self):
        return self.username

#文章所属的分类
@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('文章分类',max_length=256)
    intro = models.TextField('introduction',default='')

    def __str__(self):
        return self.name

    #添加模型的行为特性
    class Meta:
        verbose_name = '文章的分类'
        verbose_name_plural = 'column'
        ordering = ['name']


# Article模型的约束关系
# 1 文章的分类，属于多对一中的 多
# 2 文章的作者，同上
# 3 和普通用户的关系，多对多
@python_2_unicode_compatible
class Article(models.Model):

    column = models.ForeignKey(Column,blank=True,null=True,verbose_name='belong to',on_delete=models.CASCADE)
    # 1
    title = models.CharField('标题',max_length=256)
    author = models.ForeignKey('Author',on_delete=models.CASCADE)

    user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    content = models.TextField('content')
    # 2
    pub_date = models.DateTimeField(auto_now_add=True,editable=True)

    update_time = models.DateTimeField(auto_now=True,null=True)
    published = models.BooleanField('notDraft',default=True)

    # 3
    poll_num = models.IntegerField('点赞数',default=0)
    comment_num = models.IntegerField('评论数',default=0)
    keep_num = models.IntegerField('收藏数',default=0)

    objects = ArticleManager()#替代默认的model查询接口对象


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'




# 评论的约束关系
# 1 该评论属于哪个普通用户（NewUser）
# 3 该comment是基于哪篇Article
@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,null=True,on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField('更新日期',auto_now_add=True,editable=True)
    poll_num = models.IntegerField('点赞数',default=0)

    def __str__(self):
        return self.content

class Author(models.Model):
    name = models.CharField(max_length=256)
    profile = models.CharField('profile',default='',max_length=256)
    password = models.CharField('password',max_length=256)
    register_date = models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return self.name

# 记录一个点赞相关的信息
# 1 这个赞是哪个用户发起的
# 2 赞了哪篇文章
# 3
class Poll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,null=True,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,null=True,on_delete=models.CASCADE)

# 记录哪位用户点赞了哪篇文章
class ArticlePoll(models.Model):
    pass


# 评论的评论
class Comment_comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,null=True,on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content


























