from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from web.views import index, article, login, register, userInfo

app_name = 'web'
urlpatterns = [
    url(r'^$', index.index, name='index'),  # 首页
    url(r'^(?P<arctype_path>\w+)$', article.listArticle, name='list_article'),  # 栏目文章列表
    # url(r'^(?P<sitepath>\w+)/(?P<article_id>[0-9]+).html$', article.article, name='article'),  # 文章详情
    url(r'^(?P<article_id>[0-9]+).html$', article.article, name='article'),  # 文章详情
    url(r'^login/$', login.loginView, name='login'),  # 登录页
    url(r'^register/$', register.registerView, name='register'),  # 注册页
    url(r'^quit/$', login.quitView, name='quit'),  # 退出页
    url(r'^user/$', userInfo.userCenter, name='user'),  # 用户中心页
    url(r'^editprofile/$', userInfo.editProfile, name='editprofile'),  # 编辑页
    url(r'^changepwd/$', userInfo.changePassword, name='changepwd'),  # 修改密码页
    url(r'^(?P<year>\d+)/(?P<month>\d+)$', article.file, name='file'),  # 归档页
]
