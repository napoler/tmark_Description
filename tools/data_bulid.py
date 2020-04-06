import tkitFile
import tkitText
# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
# from elasticsearch_dsl import Q
from config import *
from tqdm import tqdm
import time

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
for f_path in ttf.all_path(data_path):
    
    if f_path.endswith(".anns"):
        # print(_read_data(f_path))
        one=_read_data(f_path)
        m=[]
        w=[]
        for i,it in enumerate( one[0][0]):
            if it.endswith("实体"):
                # print(it)
                # ner.append((it,one[0][1][i]))
                m.append('实体')
                w.append(one[0][1][i])
                one[0][0][i]='O'
            elif it=='E-实体' or it=="S-实体":
                # print(it)
                # ner.append((it,one[0][1][i]))
                m.append('实体')
                m.append('[SEP]')
                w.append(one[0][1][i])
                w.append('X')
                one[0][0][i]='O'          
        one[0][0]=m+['X']+one[0][0]
        one[0][1]=w+['[SEP]']+one[0][1]
        # print(one)
        data.append(one[0])
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
