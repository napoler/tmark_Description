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

```
search_to_txt.py
```




