

import numpy as np
import torch
from transformers import (
    MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING,
    WEIGHTS_NAME,
    AdamW,
    AutoConfig,
    AutoModelForTokenClassification,
    AutoTokenizer,
    get_linear_schedule_with_warmup,
)
tokens="你好吗"

device='cpu'
model_path="../model"
labels_file="../model/labels.txt"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)
model.to(device)
# result, predictions = evaluate(args, model, tokenizer, labels, pad_token_label_id, mode="test")
# input_ids = tokenizer.convert_tokens_to_ids(tokens)
# print(input_ids)
# Save results
# output_test_results_file = os.path.join(args.output_dir, "test_results.txt")
# 加拿大无毛猫并不是全身光溜溜的一点毛发也没有

print("输入文字中的实体和文字,提取关于实体的描述信息")
word=input("输入实体:")

text=input("输入文字:")

text=word+"[SEP]"+text
model.eval()
input_ids = torch.tensor(tokenizer.encode(text, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
labels = torch.tensor([1] * input_ids.size(1)).unsqueeze(0)  # Batch size 1
outputs = model(input_ids, labels=labels)
# print(outputs)
tmp_eval_loss, logits  = outputs[:2]
# print(loss, scores)
# print(logits.detach().cpu().numpy())
# print(torch.argmax(logits ,axis=2).tolist())
# preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
# out_label_ids = np.append(out_label_ids, inputs["labels"].detach().cpu().numpy(), axis=0)
ids=tokenizer.encode(text)
# print(ids)


f2=open(labels_file,'r')
lablels_dict={}
for i,line in enumerate( open(labels_file)):
    # l=line.split(" ")
    l=line.replace("\n",'')
    # print(l)
    lablels_dict[i]=l
print("\n".join([i for i in lablels_dict.keys()]))
all_ms=[]
for i,m in enumerate( torch.argmax(logits ,axis=2).tolist()[0]):
    print(m)
    print(m,ids[i],tokenizer.convert_ids_to_tokens(ids[i]),lablels_dict[m])
    word=tokenizer.convert_ids_to_tokens(ids[i])
    if m >len(lablels_dict):
        mark_lable="X"
    else:
        mark_lable=lablels_dict[m]

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
print(all_ms)

        # w=''





