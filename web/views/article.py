import math
from itertools import chain

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from web import models
from baidu import related


def listArticle(request, arctype_path):
    archives = models.Archives.objects.filter(type__sitepath=arctype_path).order_by('-id')
    arctype = models.ArcType.objects.all()

    # 获取当前页码
    num = int(request.GET.get('bn', 1))
    # 创建分页,少于4条合并到上页
    pager = Paginator(archives, 10, 4)
    # 获取当前分页
    try:
        archives = pager.page(num)
    except PageNotAnInteger:
        # 返回第一页
        archives = pager.page(1)
    except EmptyPage:
        # 返回最后一页
        archives = pager.page(archives.num_pages)

    # 每页home页码
    bn = (num - int(math.ceil(4.0 / 2)))
    if bn < 1:
        bn = 1
    # 每页end页码
    end = bn + 4
    if end > pager.num_pages:
        end = pager.num_pages
    if end <= 5:
        bn = 1
    else:
        bn = end - 4
    pageList = range(bn, end + 1)

    for type in arctype:
        if type.sitepath == arctype_path:
            typename = type.typename
            seotitle = type.seotitle
            keywords = type.keywords
            description = type.description
            write = type.write

    if arctype_path == 'book':
        return render(request, 'book.html', locals())
    if arctype_path == 'issue':
        return render(request, 'issue.html', locals())
    if arctype_path == 'tiwen':
        return render(request, 'form.html', locals())

    return render(request, 'list_article.html', locals())


# def article(request,sitepath, article_id):
def article(request, article_id):
    # 文章
    article = models.Archives.objects.filter(id=article_id)
    for item in article:
        title = item.title
        keywords = item.keywords
        description = item.description
        arc_red = related.main(title)
        arc_green = models.Archives.objects.filter(id=0)
        for i in arc_red:
            arc_green = chain(arc_green, models.Archives.objects.filter(id=i[0]))  # 合并QuerySet类型
        arc_green = list(set(arc_green))  # 去重
    # 自增+1浏览数
    click = models.Archives.objects.get(id=article_id)
    click.increase_read_count()

    return render(request, 'article_article.html', locals())


def file(request, year, month):
    # 归档
    article = models.Archives.objects.filter(pubdate__icontains=year + '-' + month)
    return render(request, 'file_article.html', locals())
