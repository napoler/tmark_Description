# tmark_Description
基于实体提取对应文章中的描述。

## 标注工具
https://github.com/t-web/ChineseAnnotator



## 标注工具Ai_bert
https://github.com/t-web/ChineseAnnotator/tree/Ai_bert
加入了自动提取实体和描述
### 实体提取模型
https://www.kaggle.com/terrychanorg/bert-ner-model
放置在目录
tkitfiles/tmarker_bert_ner/
### 描述提取模型
https://www.kaggle.com/terrychanorg/tmarkdescriptionmodel
放置在目录下
tkitfiles/miaoshu/


## 生成的数据

tools目录下执行下面命令生成数据
```
$ python data_bulid.py
```
下面是放在kaggle上的数据
https://www.kaggle.com/terrychanorg/tmark-description


## 添加文章
tools目录下执行下面命令自动搜索文章
（此命令不适合所有人，是基于本地数据的搜索，没有共享大家可以放弃这个步骤）
数据使用elasticsearch作为搜索
不一定适合所有人
```
search_to_txt.py
```


## Kaggle上训练
基础模型
chinese_wwm_ext_pytorch

描述训练
https://www.kaggle.com/terrychanorg/bert-tmark-description

ner训练
https://www.kaggle.com/napoler/bert-ner-tmark

## 模型下载
标记精力和算力都有限，可以用来测试

https://www.kaggle.com/terrychanorg/tmarkdescriptionmodel

![alt text](https://github.com/napoler/tmark_Description/blob/master/ner_train/static/pre_test.png "效果测试")



## 使用模型
使用bert微调提取实体，描述这些信息。
```
pip install tkitMarker_bert
```
测试
```
from tkitMarker_bert import Marker

text="柯基犬是一个小短腿"
word="柯基犬"
#加载预测描述
pred=Marker(model_path="./model")
model,tokenizer=pred.load_model()
pall=pred.pre(word,text,model,tokenizer)
print(word,pall)
>>>柯基犬 ['是一个小短腿']

```

## 后续使用
上面产生的数据后续可以使用knn或者聚类等等进行聚合内容。
应该可以把各种有效元素进行聚合分类。

## 解决重复

从文本中提取的描述信息，会出现很多不同的表述，对于这种情况，对相似的内容进行合并是非常有必要的。
个人还是用到的bert模型，微调的同义句判断模型来解决的。
详情可以访问这个链接：
https://www.terrychan.org/transformers-SentenceSimilarity/

## 其他

不得不说Bert真是好用，就是资源有点浪费啊！


[By Terry Chan](https://www.terrychan.org)


