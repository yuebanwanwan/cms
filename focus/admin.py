from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.db import models
from django import forms
from focus.models import *

class CommentAdmin(admin.ModelAdmin):
    # 这是model在数据库中对应表的字段的名称
    list_display = ('user_id','article_id','pub_date','content','poll_num')

class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField:{
            'widget':forms.Textarea(
                attrs={
                    'rows':41,
                    'cols':100,
                }
            )
        }
    }
    list_display = ('title','pub_date','poll_num','comment_num')
    list_per_page = 1
    list_editable = ['poll_num','comment_num']
    fk_fileds = ('poll_num')
    list_filter = ('pub_date','poll_num','comment_num')
    search_fields = ('comment_num',)



class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username','date_joined','profile')


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name','intro')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','profile')

class CommentcommentAdmin(admin.ModelAdmin):
    list_display = ('user','comment','content',)

admin.site.register(Comment,CommentAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Column,ColumnAdmin)
admin.site.register(NewUser,NewUserAdmin)
admin.site.register(Comment_comment,CommentcommentAdmin)















