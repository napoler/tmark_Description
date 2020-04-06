import tkitFile
import tkitText
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
# from elasticsearch_dsl import Q
from config import *
from tqdm import tqdm
import time
import numpy as np   
import math
def _read_data( input_file):
    """Reads a BIO data."""
    max_length=100
    # num=max_length #定义每组包含的元素个数
    with open(input_file) as f:
        lines = []
        words = []
        labels = []
        # stop = ["。","!","！"]
        stop=[]
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

def save_data(data,file="data.txt"):
    """
    构建数据保存
    """
    with open(file,'w',encoding = 'utf-8') as f1:
        for it in data:
            for m,w in zip(it[0],it[1]):
                # print(m,w)
                f1.write(w+"\t"+m+"\n")
            # print("end\n\n\n\n")
            f1.write("\n")


data_path='../data'
ttf=tkitFile.File()
tt=tkitText.Text()
data=[]
limit=480 #这里配置多少字分段
for f_path in ttf.all_path(data_path):
    
    if f_path.endswith(".anns"):
        # print(_read_data(f_path))
        one_data=_read_data(f_path)

        h=math.ceil(len(one_data[0][0])/limit)
        x = np.array(one_data[0][0]+["[PAD]"]*(limit*h-len(one_data[0][0])))     #x是一维数组
        y = np.array(one_data[0][1]+["X"]*(limit*h-len(one_data[0][0])))     #x是一维数组

        x = x.reshape((h,limit))                #将x重塑为2行4列的二维数组
        y = y.reshape((h,limit))                #将x重塑为2行4列的二维数组
        # print(x)
        m=[]
        w=[]
        for one_x,one_y in zip(x.tolist(),y.tolist()):

            one=[]   
            for i,(x,y) in enumerate(zip( one_x,one_y)) :
                if x.endswith("实体"):
                    # print(it)
                    # ner.append((it,one[0][1][i]))
                    m.append('实体')
                    w.append(y)
                    one_x[i]='O'
                elif x=='E-实体' or x=="S-实体":
                    # print(it)
                    # ner.append((it,one[0][1][i]))
                    m.append('实体')
                    m.append('[SEP]')
                    w.append(y)
                    w.append('X')
                    one_x[i]='O'   
                # print(one_y)
                # exit()
            one=((m+['X']+one_x,w+['[SEP]']+one_y))
                # one[1]=
            data.append(one)
# print(data)
c=int(len(data)*0.8)
print(len(data))
train_data=data[:c]
dev_data=data[c:]

save_data(train_data,file="../data/train.txt")
save_data(dev_data,file="../data/dev.txt")

 
        # print()
        # for line in open(f_path):
# line.endswith("实体")
