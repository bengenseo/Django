# @Desc  :调用百度接口实现文章描述的提取
# coding:utf-8
import json
import requests

APIKey = "DKHTTB9iR6vQQtCcoG4Sc1Wo"
SecretKey = "daHYq6UqpQcqsxKmeGeiCZFwY6oM2kAq"

#创建请求url
def get_url():
    url=0
    #通过API Key和Secret Key获取access_token
    AccessToken_url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(APIKey,SecretKey)
    res = requests.post(AccessToken_url)#推荐使用post
    json_data = json.loads(res.text)
    #print(json.dumps(json_data, indent=4, ensure_ascii=False))
    if not json_data or 'access_token' not in json_data:
        print("获取AccessToken的json数据失败")
    else:
        accessToken=json_data['access_token']
        #将得到的access_token加到请求url中
        url='https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary?charset=UTF-8&access_token={}'.format(accessToken)
    return url

#创建请求，获取数据
def get_tag(url,title,content):
    #创建Body请求
    body={
        "title": title,
        "content":content,
        "max_summary_len":200
    }
    body2 = json.dumps(body)#将字典形式的数据转化为字符串,否则报错
    #创建Header请求
    header={
        'content-type': 'application/json'
    }
    res = requests.post(url,headers=header,data=body2)# 推荐使用post
    json_data = json.loads(res.text)
    if not json_data or 'error_code' in json_data:
        #print(json.dumps(json_data, indent=4, ensure_ascii=False))
        print("获取关键词的Json数据失败")
    else:
        return json_data.get("summary")

# if __name__ == '__main__':
#     title='iphone手机出现“白苹果”原因及解决办法，用苹果手机的可以看下'
#     content = '''国家这个经济的这个主力的变化，所以这个房产会发生在未来十年，它不是一天发生的个位会在未来十年会在未来十年会发生一个重大的变化，然后呢？很多现在银行里的断供越来越多了，银行里的房子的断供越来越来越多了，很多的地，然后为由于房产这个变化呢，所以你的资产量，特别是中小城市这种投资的房产，因为另外一拨资产降得特别便宜了，大家明白吗？如果他不强的话，其实没有我问大家水往高处流还是水你我们说的是十年，今天，未来十年十年做布局做准备，你才不枉就是你才不枉未来的十年就跟你08年，是为18年在做准备，你的心中很有数，我只要不断地配置房子就是我的方向，这才会有大的方向，好了，时间原因啊今天。'''
#     url=get_url()
#     ps_key = get_tag(url,title , content)
#     print(ps_key)