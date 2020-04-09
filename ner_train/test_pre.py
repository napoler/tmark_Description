

import numpy as np
import torch
from transformers import AutoModelForTokenClassification,AutoTokenizer
import os
import re


import tkitFile
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from config import *
from tqdm import tqdm
import time
import tkitText
from tkitMarker import *
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








class Pred_description:
    def __init__(self,model_path="../model",device='cpu'):
        self.model_path=model_path
        self.labels_file=os.path.join(model_path,"labels.txt")
        self.device=device
        pass
    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        model = AutoModelForTokenClassification.from_pretrained(self.model_path)
        model.to(self.device)
        f2=open(self.labels_file,'r')
        lablels_dict={}
        for i,line in enumerate(f2):
            # l=line.split(" ")
            l=line.replace("\n",'')
            # print(l)
            lablels_dict[i]=l
        f2.close()
        self.lablels_dict=lablels_dict
        return model,tokenizer
    def cut_text(self,text,lenth):
        """
        分割固定长度字符串
        """
        textArr = re.findall('.{'+str(lenth)+'}', text)
        textArr.append(text[(len(textArr)*lenth):])
        return textArr
    def pre(self,word,text,model,tokenizer):
        model.eval()
        text=word+"[SEP]"+text
        lenth=509-len(word)
        all_ms=[]
        for text_mini in self.cut_text(text,lenth):
            # text_mini=word+"[SEP]"+text_mini
            ids=tokenizer.encode_plus(word,text_mini,max_length=512, add_special_tokens=True)
            # print(ids)
            input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
            labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids, labels=labels)
            # print(outputs)
            tmp_eval_loss, logits  = outputs[:2]
            # ids=tokenizer.encode(text)
            # print(ids)

            # print("\n".join([i for i in self.lablels_dict.keys()]))
            words=[]
            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])

                if m >=len(self.lablels_dict):
                    mark_lable="X"
                else:
                    mark_lable=self.lablels_dict[m]

                if mark_lable=="E-描述"  and len(words)>0:
                    
                    words.append(word)
                    # words.append(word+mark_lable)
                    # print(words)
                    all_ms.append("".join(words))
                    words=[]
                elif mark_lable=="S-描述":
                    words=[]
                    words.append(word)
                    # words.append(word+mark_lable)
                    all_ms.append("".join(words))
                    words=[]
                elif mark_lable=="B-描述":
                    words=[]
                    words.append(word)
                    # words.append(word+mark_lable)
                elif mark_lable=="M-描述" and len(words)>0:
                    words.append(word)
                    # words.append(word+mark_lable)
                elif  mark_lable=="O" or mark_lable=="X":
                    words=[]
                    pass
        return all_ms

    def pre_ner(self,text,model,tokenizer):
        model.eval()
        text=text
        lenth=128
        all_ms=[]
        for text_mini in self.cut_text(text,lenth):
            # text_mini=word+"[SEP]"+text_mini
            ids=tokenizer.encode_plus(text_mini,max_length=512, add_special_tokens=True)
            # print(ids)
            input_ids = torch.tensor(ids['input_ids']).unsqueeze(0)  # Batch size 1
            labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
            outputs = model(input_ids, labels=labels)
            # print(outputs)
            tmp_eval_loss, logits  = outputs[:2]
            # ids=tokenizer.encode(text)
            # print(ids)

            # print("\n".join([i for i in self.lablels_dict.keys()]))
            words=[]
            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])
                # print(word,self.lablels_dict[m])
                if m >=len(self.lablels_dict):
                    mark_lable="X"
                else:
                    mark_lable=self.lablels_dict[m]

                if mark_lable=="E-实体"  and len(words)>0:
                    
                    words.append(word)
                    # print(words)
                    all_ms.append("".join(words))
                    words=[]
                elif mark_lable=="S-实体":
                    words=[]
                    words.append(word)
                    all_ms.append("".join(words))
                    words=[]
                elif mark_lable=="B-实体":
                    words=[]
                    words.append(word)
                elif mark_lable=="M-实体"  and len(words)>0:
                    words.append(word)
                elif  mark_lable=="O" or mark_lable=="X":
                    words=[]
                    pass
        return all_ms



# TNer=Pre()
# TNer.args['conf']="../model/tkitfiles/tkitMarker/config.json"
# TNer.args['load_path']="../model/tkitfiles/tkitMarker/pytorch_model.bin"
# TNer.args['vocab']="../model/tkitfiles/tkitMarker/vocab.txt"
# TNer.args['label_file']="../model/tkitfiles/tkitMarker/tag.txt"
# TNer.args['albert_path']="../model/tkitfiles/tkitMarker"
# TNer.args['albert_embedding']=312
# TNer.args['rnn_hidden']=400

# TNer.model_version='ner_rel'
# TNer.args['max_length']=50
# TNer.setconfig()

tt=tkitText.Text()

pred=Pred_description()
model,tokenizer=pred.load_model()
# 加载ner模型
ner_pred=Pred_description(model_path="../model/ner")
ner_pred_model,ner_pred_tokenizer=ner_pred.load_model()

while  True:
    print("\n"*4)
    print("输入文字中的实体和文字,提取关于实体的描述信息")
    keyword=input("输入搜索关键词:")
    for it in search_content(keyword):
        print("##"*10+it.title)
        text=it.title+"\n"+it.content
        words=ner_pred.pre_ner(text,ner_pred_model,ner_pred_tokenizer)
        words=list(set(words))
        for word in words:
            pall=pred.pre(word,text,model,tokenizer)
            print(word,pall)

# i=0
# for it in DB.content_pet.find({}):
#     i=i+1
#     if i==1000:
#         break

#     sents=tt.sentence_segmentation_v1(it['content'])
#     print("##"*10+it['title'])
#     text=it['title']+"\n"+it['content']
#     words=ner_pred.pre_ner(text,ner_pred_model,ner_pred_tokenizer)
#     # print(words)

#     # result=TNer.pre(sents) 
#     # # print(result)
#     # words=[]
#     # for it_re in result:
#     #     for w in it_re[1]:
#     #         # print("ner_w",ner_w)
#     #         # for w in ner_w:
#     #         print("w",w)
#     #         if w['type']=="实体":
#     #             words.append(w['words'])
#     words=list(set(words))
#     for word in words:
#         pall=pred.pre(word,text,model,tokenizer)
#         print(word,pall)
