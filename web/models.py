import re
from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags
from html.parser import HTMLParser

from system.storage import ImageStorage
from baidu import description, keywords

data_time = datetime.now().strftime("%Y%m%d")


class UserInfo(models.Model):
    name = models.CharField(verbose_name='昵称', max_length=20, null=True, blank=True)
    user = models.OneToOneField(verbose_name='用户ID', max_length=20, to=User, unique=True, )
    phone = models.CharField(verbose_name='手机号', max_length=50, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ArcType(models.Model):
    topid = models.IntegerField(null=True, blank=True)
    reid = models.ForeignKey(max_length=5, to='self', null=True, blank=True)
    typename = models.CharField(verbose_name='栏目名称', max_length=20, unique=True)
    seotitle = models.CharField(verbose_name='SEO标题', max_length=50, null=True, blank=True)
    keywords = models.CharField(verbose_name='关键字', max_length=30, null=True, blank=True)
    description = models.CharField(verbose_name='描述', max_length=200, null=True, blank=True)
    sitepath = models.SlugField(verbose_name='栏目URL', max_length=20, null=True, blank=True)
    write = RichTextUploadingField(verbose_name='封面主体', null=True, blank=True)

    def __str__(self):
        return self.typename

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'


class Archives(models.Model):
    type = models.ForeignKey(verbose_name='分类', to='ArcType')
    title = models.CharField(max_length=100, verbose_name='文章标题', unique=True)
    keywords = models.CharField(max_length=50, verbose_name='关键字', null=True, blank=True)
    description = models.CharField(max_length=300, verbose_name='描述', null=True, blank=True)
    litpic = models.ImageField(upload_to=data_time, storage=ImageStorage(), max_length=128, verbose_name='缩略图URL',
                               null=True,
                               blank=True)
    author = models.ForeignKey(verbose_name='作者', to=User)
    click = models.IntegerField(verbose_name='浏览数', default=0)
    senddate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    pubdate = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章标题'
        verbose_name_plural = '文章列表'

    def get_absolute_url(self):  # 反向生成url
        # return reverse('web:article', kwargs={'sitepath':self.type.sitepath,'article_id': self.id})  # http://127.0.0.1/article/1
        return reverse('web:article', kwargs={'article_id': self.id})  # http://127.0.0.1/article/1

    def increase_read_count(self):
        # 自增浏览量
        self.click += 1
        self.save(update_fields=['click'])

    # def __unicode__(self):
    #     return u'Archives:%s,%s,%s' % (self.id, self.title, self.author)

    # 重写保存的方法
    def save(self, *args, **kwargs):
        if not self.keywords:
            # 百度生成文章关键字
            url = keywords.get_url()
            ps_key = keywords.get_tag(url, self.title, self.article.body)
            self.keywords = HTMLParser().unescape(strip_tags(ps_key))

        if not self.description:
            # 百度生成文章描述
            new_title = self.title
            content = HTMLParser().unescape(strip_tags(self.article.body))
            url = description.get_url()
            ps_dtn = description.get_tag(url, new_title, content)
            # strip_tags 去掉html文本的全部html标签
            # HTMLParser().unescape() 不转义HTML字符
            self.description = HTMLParser().unescape(strip_tags(ps_dtn))
        # 调用父类的保存方法保存到数据库中
        super(Archives, self).save(*args, **kwargs)


class Article(models.Model):
    arc = models.OneToOneField(verbose_name='文章ID', to='Archives')
    body = RichTextUploadingField(verbose_name='文章主体', null=True, blank=True)

    def __str__(self):
        return self.arc.title

    class Meta:
        verbose_name = '文章主体'
        verbose_name_plural = '文章主体'

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        try:
            self.arc = Archives.objects.get(title=self.arc.title)
        except Archives.DoesNotExist:
            self.arc = Archives.objects.create(title=self.arc.title)
        #标题表外键表插入
        models.Model.save(self, force_insert=False, force_update=False, using=None,update_fields=None)
