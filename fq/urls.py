from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^bgcms/', admin.site.urls),
    url(r'^', include('web.urls')),
    # 富文本编辑器
    url(r'ckeditor/', include('ckeditor_uploader.urls')),
    # 搜索功能
    url(r'search/', include('haystack.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
