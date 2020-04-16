import tkitFile
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from config import *
from tqdm import tqdm
from albert_pytorch import classify

tclass = classify(model_name_or_path='../model/goodorbad/',num_labels=2,device='cpu')

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

        if len(item.title+item.content)<200:
            continue
        p=tclass.pre(item.content)
        # print(p)
        if p==0:
            continue
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



def _read_data( input_file):
    """Reads a BIO data."""
    max_length=100
    # num=max_length #定义每组包含的元素个数
    with open(input_file) as f:
        lines = []
        words = []
        labels = []
        stop = ["。","!","！"]
        for line in f:
            contends = line.strip()
            
            # print(len(line.strip().split(' ')))
            word = line.strip().split(' ')[0]
            label = line.strip().split(' ')[-1]

            if contends.startswith("-DOCSTART-"):
                words.append('')
                continue
            # if len(contends) == 0 and words[-1] == '。':
            if len(contends) == 0:
                # l = ' '.join([label for label in labels if len(label) > 0])
                # w = ' '.join([word for word in words if len(word) > 0])
                l=[label for label in labels if len(label) > 0]
                w = [word for word in words if len(word) > 0]
                if l==w:
                    # print('xian')
                    pass
                else:
                    w_one=[]
                    l_one=[]
                    # n=0
                    tags={}
                    for i,it in enumerate(w):
                        #基于句子分段
                        if it in stop:
                            w_one.append(w[i])
                            l_one.append(l[i])
                            tags[l[i]]=0
                            # 如果标记内容过少则忽略
                            if len(tags)>1:
                                lines.append([l_one, w_one])
                            tags={}
                            w_one=[]
                            l_one=[]
                        elif i==len(w)-1:
                            if len(tags)>1:
                                lines.append([l_one, w_one])
                            tags={}
                            w_one=[]
                            l_one=[]
                        else:
                            tags[l[i]]=0
                            w_one.append(w[i])
                            l_one.append(l[i])
                    
                    # # 如果内容过长自动分段
                    # if len(l)> max_length:
                    #     for i in range(0,len(l),max_length):
                    #         # print l[i:i+num]
                    #         lines.append([l[i:i+max_length], w[i:i+max_length]])
                    # else:
                    #     lines.append([l, w])
                words = []
                labels = []
                continue
            words.append(word)
            labels.append(label)
        return lines

 

# x= input("输入：")
while True:
    x= input("输入关键词：")
    data_pre_train_mongo_text(x,train_path='../data/' )
    


