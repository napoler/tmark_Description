import tkitFile
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from config import *
from tqdm import tqdm
import time
def search_content(keyword):
    client = Elasticsearch()
    q = Q("multi_match", query=keyword, fields=['title', 'body'])
    # s = s.query(q)

    # def search()
    s = Search(using=client)
    # s = Search(using=client, index="pet-index").query("match", content="金毛")
    s = Search(using=client, index="pet-index").query(q)
    response = s.execute()
    return response
    # for hit in response:
    #     print(hit.meta)
    #     print(hit.meta.score)
    #     print(hit)
def data_pre_train_mongo_text(keyword,train_path='../data/' ):
    """
    构建文本数据将单篇文章一个txt文件
    """
 
    # tt=tkitText.Text()
    #这里定义mongo数据
    # client = pymongo.MongoClient("localhost", 27017)
    # DB_kg_scrapy = client.kg_scrapy

    # q={}
    i=0
    # content_pet
    # for item in DB_kg_scrapy.kg_content.find(q):
    # time_path='0'
    ttf=tkitFile.File()
    ttf.mkdir(train_path+keyword)
    for item in tqdm(search_content(keyword)):
        i=i+1
        # if i%10000==0:
            
            # time_path =str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #     break
        name= str(int(time.time()))+item.title[:10]+".txt"
        # file_path=os.path.join(train_path,name)
        file_path=train_path+keyword+"/"+name
        # print(file_path)
        try:
            with open(file_path,'w',encoding = 'utf-8') as f1:
                f1.write(item.title+"\n")
                f1.write(item.content+"\n")
        except:
            pass
# x= input("输入：")
while True:
    x= input("输入关键词：")
    data_pre_train_mongo_text(x,train_path='../data/' )
    


