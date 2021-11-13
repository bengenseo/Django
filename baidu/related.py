# coding:utf-8
import os, json, time, pymysql, sys
from whoosh import qparser
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import index
from jieba.analyse import ChineseAnalyzer
import random
import hashlib
# 数据库信息
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = ''
DBNAME = 'fq'

start = time.time()

try:
    db = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, db=DBNAME, port=3306, charset='utf8')
    db.commit()
    print('数据库连接成功')
except pymysql.Error as e:
    print('%s数据库连接失败：' % DBNAME + str(e))
    print('表格创建失败：' + str(e))


# 建立md5值
def get_md5(str):
    hash_md5 = hashlib.md5()
    hash_md5.update(str.encode('utf-8'))
    return hash_md5.hexdigest()


# whoosh建立索引函数
def new_index_sql():
    # 按照schema定义信息，增加需要建立索引的文档

    # 初始值
    n = 0
    # 建立索引，limitmb（M为单位），procs理解为线程数
    writer = ix.writer(limitmb=256, procs=4)

    # 获取数据表行数
    cur = db.cursor()
    cur.execute('SELECT count(1) from web_article')
    number = cur.fetchone()[0]

    with db:
        cur.execute('SELECT id,body from web_article')
        data = cur.fetchall()
        for line in data:
            id = line[0]
            body = line[1]
            # 将每行记录写入索引中，将keyword复制给section索引变量
            writer.add_document(id=id, body=body)

            # 输出百分比进度条
            n += 1
            percent = float(n) * 100 / float(number)
            sys.stdout.write("------ > 完成百分比：%.2f" % percent)
            sys.stdout.write("%\r")
            sys.stdout.flush()

    writer.commit()
    sys.stdout.flush()
    print('>>> found whoosh index done 完成 ...')


# 实现搜索功能函数 PS：需要索引创建完成，才能实现搜索功能
def search_index(words):
    xg_part = []
    with ix.searcher() as s:
        # group = qparser.OrGroup 表示可匹配任意查询词，而不是所有查询词都匹配才出结果
        qp = QueryParser('body', schema=ix.schema, group=qparser.OrGroup)

        # 下面两行表示可以使用通配符，如“窗前*月光”
        qp.remove_plugin_class(qparser.WildcardPlugin)
        qp.add_plugin(qparser.PrefixPlugin())

        # 随机数
        # num = random.randint(5, 10)
        num=11

        for word in words:
            q = qp.parse(u'%s' % word)

            # limit 表示多少条搜索结果
            results = s.search(q, limit=num)
            count = 0
            for i in results:
                if count > 0:  # 防止等于本身
                    xg_part.append((i['id'], i['body']))
                count += 1
    return xg_part


# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 创建schema，stored为True表示可以被检索
schema = Schema(body=TEXT(stored=True, analyzer=ChineseAnalyzer()), id=NUMERIC(stored=True))


def main(query):
    global ix
    indexdir = 'whoosh_related/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    try:
        # 获取内容
        ix = index.open_dir(indexdir)
    except:
        print('>>> 未被索引 ...')
        print('>>> 正在索引 ...')
        ix = create_in(indexdir, schema)
        new_index_sql()

    words = ['%s' % query]
    xgwprds = search_index(words)
    return xgwprds

    # 关闭数据库
    db.close()

# if __name__ == '__main__':
#     upshot = main('巴菲特')
#     art = ''
#     for index, item in upshot:
#         # item = item[1]
#         art += item + '\n'
#         print(index, item[:50], start, '\n')
#     # print(art, '字数：', len(art))