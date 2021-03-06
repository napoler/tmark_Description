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
import tkitFile

def _read_data( input_file):
    """Reads a BIO data."""
    max_length=480
    # num=max_length #定义每组包含的元素个数
    with open(input_file) as f:
        lines = []
        words = []
        labels = []
        # stop = ["。","!","！"]
        stop=[]
        
        for line in f:
            # print(line)
            contends = line.strip()
            
            # print(len(line.strip().split(' ')))
            word = line.strip().split(' ')[0]
            label = line.strip().split(' ')[-1]
            if word=='':
                continue

            if contends.startswith("-DOCSTART-"):
                words.append('')
                continue
            # if len(contends) == 0 and words[-1] == '。':
            # print(word,label)
            # words.append(word)
            
            # print("contends",contends)
            # if len(contends) == 0:
            #     # l = ' '.join([label for label in labels if len(label) > 0])
            #     # w = ' '.join([word for word in words if len(word) > 0])
            #     l=[label for label in labels if len(label) > 0]
            #     w = [word for word in words if len(word) > 0]
    
                

                # if l==w:
                #     # print('xian')
                #     pass
                # else:
                #     w_one=[]
                #     l_one=[]
                #     # n=0
                #     tags={}
                #     for i,it in enumerate(w):
                #         print(it)
                #         #基于句子分段
                #         if it in stop:
                #             w_one.append(w[i])
                #             l_one.append(l[i])
                #             tags[l[i]]=0
                #             # 如果标记内容过少则忽略
                #             if len(tags)>1:
                #                 lines.append([l_one, w_one])
                #             tags={}
                #             w_one=[]
                #             l_one=[]
                #         elif i==len(w)-1:
                #             if len(tags)>1:
                #                 lines.append([l_one, w_one])
                #             tags={}
                #             w_one=[]
                #             l_one=[]
                #         else:
                #             tags[l[i]]=0
                #             w_one.append(w[i])
                #             l_one.append(l[i])
                    
                #     # # 如果内容过长自动分段
                #     # if len(l)> max_length:
                #     #     for i in range(0,len(l),max_length):
                #     #         # print l[i:i+num]
                #     #         lines.append([l[i:i+max_length], w[i:i+max_length]])
                #     # else:
                #     #     lines.append([l, w])
                # words = []
                # labels = []
                # continue

            # print(word)
            # print(label)
            words.append(word)
            labels.append(label)
        one=[labels,words]
        lines.append(one)
        return lines

def load_pre(file="data.txt",save_data="save_data.txt"):
    """
    加载之前数据
    """
    with open(file) as f:
        lines = f.read()
        # print(type(lines))
        # print(lines)
    with open(save_data,'w',encoding = 'utf-8') as f1:
        f1.write(lines)
        f1.write("\n")
        f1.write("\n")

def save_data(data,file="data.txt"):
    """
    构建数据保存
    """
    with open(file,'a+',encoding = 'utf-8') as f1:
        for it in data:
            for m,w in zip(it[0],it[1]):
                # print(m,w)
                f1.write(w+" "+m+"\n")
            # print("end\n\n\n\n")
            f1.write("\n")


def save_labels(data,file="labels.txt"):
    """
    构建数据保存
    """
    labels={}
    with open(file,'w',encoding = 'utf-8') as f1:
        for it in data:
            for m in it[0]:
                labels[m]=1
                # print(m,w)
        keys=[]
        for key in labels.keys():
            keys.append(key)
        f1.write("\n".join(keys))

# f_path="../data/清道夫鱼/1586186362清道夫鱼吃什么食物_.txt上海.anns"
# one_data=_read_data(f_path)
# print(one_data)
# exit()




data_path='../data'
ttf=tkitFile.File()
tt=tkitText.Text()
data=[]
limit=500 #这里配置多少字分段
anns=[]
bad=0
good=0
bad_files=[]
for f_path in ttf.all_path(data_path):
    # print(f_path)
    if f_path.endswith(".anns"):
        # print(f_path)
        anns.append(f_path)
        # print(_read_data(f_path))
        one_data=_read_data(f_path)
        # print(one_data)
        if  len(one_data)==0:
            print("no")
        m=[]
        w=[]
        # one_data_j=[]
        x_data=[]
        y_data=[]
        for one in one_data:
            x_data=x_data+one[0]
            y_data=y_data+one[1]
        for i,(x,y) in enumerate(zip(x_data,y_data)):
            # print(x)
            if x=='E-实体' or x=="S-实体":
                # print(x,y)
                # ner.append((it,one[0][1][i]))

                m.append('实体')
                m.append('X')
                w.append(y)
                w.append('#')

                x_data[i]='O'
            elif x=="B-实体" or x=="M-实体":
                # print('end')
                # print(it)
                # ner.append((it,one[0][1][i]))
                m.append('实体')
                w.append(y)

                x_data[i]='O'  
            # elif x=='':
            # print(x)
        w=w[:-1]
        w="".join(w)
        # print(w)
        w=list(set(w.split("#")))
        # print(w)
        w=list("#".join(w))
        m=["实体"]*len(w)
        if len(w)==0:
            print("没有标记忽略")
            bad_files.append(f_path)
            # print(f_path)
            bad+=1
            continue
        else:
            good+=1
        for wi,wit in enumerate(w):
            if w=="#":
                m[wi]="X"
        # print(w,m)


            


        # del(m[-1])
        # del(w[-1])
        # print(m,w)
        h=math.ceil(len(x_data)/limit)
        padd=(limit*h-len(x_data))
        x = np.array(x_data+["X"]*padd)     #x是一维数组
        y = np.array(y_data+["[PAD]"]*padd)     #x是一维数组

        x = x.reshape((h,limit))                #将x重塑为2行4列的二维数组
        y = y.reshape((h,limit))                #将x重塑为2行4列的二维数组
        # print(x)

        for one_x,one_y in zip(x.tolist(),y.tolist()):

            one=[]   
            # for i,(x,y) in enumerate(zip( one_x,one_y)) :
            #     if x.endswith("实体"):
            #         # print(it)
            #         # ner.append((it,one[0][1][i]))
            #         m.append('实体')
            #         w.append(y)
            #         one_x[i]='O'
            #     elif x=='E-实体' or x=="S-实体":
            #         # print(it)
            #         # ner.append((it,one[0][1][i]))
            #         m.append('实体')
            #         m.append('，')
            #         w.append(y)
            #         w.append('X')
            #         one_x[i]='O'   
                # print(one_y)
                # exit()
            one=((m+['X']+one_x,w+['[SEP]']+one_y))
                # one[1]=
            data.append(one)
            # 循环一次即退出
            break
            # print("1111")
# # print(data)
c=int(len(data)*0.7)
b=int(len(data)*0.85)
print(len(data))

# for it in data:
#     print(len(it[0]),len(it[1]))
print("缺少实体：",bad)
print("good实体：",good)
print(len(anns))
train_data=data[:c]
dev_data=data[c:b]
test_data=data[b:]

ttf=tkitFile.File()
ttf.mkdir("../output")


load_pre('../data/data/train.txt',"../output/train.txt")
load_pre('../data/data/dev.txt',"../output/dev.txt")
load_pre('../data/data/test.txt',"../output/test.txt")
save_data(train_data,file="../output/train.txt")
save_data(dev_data,file="../output/dev.txt")
save_data(test_data,file="../output/test.txt")
bad_files=list(set(bad_files))
for o in bad_files:
    print(o)

print(len(data))

# for it in data:
#     print(len(it[0]),len(it[1]))
print("缺少实体：",bad)
print("good实体：",good)
print(len(anns))

#一般无需重新生成labels文件
# save_labels(data,"../data/labels.txt")

 
        # print()
        # for line in open(f_path):
# line.endswith("实体")
