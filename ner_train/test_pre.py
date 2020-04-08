

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

            for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
                # print(m)
                # print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),self.lablels_dict[m])
                word=tokenizer.convert_ids_to_tokens(ids['input_ids'][i])
                if m >=len(self.lablels_dict):
                    mark_lable="X"
                else:
                    mark_lable=self.lablels_dict[m]

                if mark_lable=="E-描述" or mark_lable=="S-描述":
                    words.append(word)
                    # print(words)
                    all_ms.append("".join(words))
                    words=[]
                elif mark_lable=="B-描述":
                    words=[]
                    words.append(word)
                elif mark_lable=="M-描述":
                    words.append(word)
                elif  mark_lable=="O" or mark_lable=="X":
                    words=[]
                    pass
        return all_ms



while  True:
    print("\n"*4)
    print("输入文字中的实体和文字,提取关于实体的描述信息")
    keyword=input("输入搜索关键词:")
    word=input("输入实体:")

    # text=input("输入文字:")
    pred=Pred_description()
    model,tokenizer=pred.load_model()
    #  tokenizer.encode_plus(sentence_0, sentence_1, add_special_tokens=True, return_tensors="pt")

    # keywords=pred.cut_text(keyword,10)
    # words=['word']*len(keywords)
    # ids=tokenizer.encode(words,keywords,max_length=20)
    # print(ids)
    for it in search_content(keyword):
        print("##"*10+it.title)
        text=it.title+"\n"+it.content

        pall=pred.pre(word,text,model,tokenizer)
        print(pall)
