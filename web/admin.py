from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from web import models
from web.models import Article, Archives


class ArticleInline(admin.TabularInline):
    # 外键表
    model = Article


@admin.register(Archives)
class ArchivesAdmin(admin.ModelAdmin):
    # 被关联表
    inlines = [ArticleInline, ]


class UserInline(admin.TabularInline):
    # 外键表
    model = models.UserInfo
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserInline, ]


admin.site.register(models.ArcType)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
