from django.shortcuts import render
from django.db.models import Count
from django.db import connection
from web import models


def arctype(request):
    # 栏目
    arctype = models.ArcType.objects.all()
    return locals()


def aside(request):
    # 归类
    # annotate() 统计数量
    category = models.Archives.objects.values('type__typename', 'type__sitepath').annotate(c=Count('*')).order_by('-c')
    # 热门
    hot = models.Archives.objects.all().order_by('-click')[:7]
    # 最新
    news = models.Archives.objects.all().order_by('-id')[:10]

    # 归档
    cusor = connection.cursor()
    cusor.execute(
        "select pubdate,count('*') c from web_archives GROUP BY DATE_FORMAT(pubdate,'%Y-%m') ORDER BY c desc,pubdate desc")
    file = cusor.fetchall()
    return locals()
