import pandas as pd
import torch
from py2neo import Relationship
from transformers import BertTokenizer


class Pre():
    def __init__(self) -> None:
        self.label_list = ['日期','时间','年份','月份','国家','省市','地点','姓名', '性别', '身份证号', '手机号', '座机号/传真','政治面貌','民族', '学历', '专业', 
            '公司', '职位', 'uuid', '邮箱','哈希值', '域名','ipv4地址','ipv6地址', 'mac地址', 'url', 'user_agent','车牌号','信用卡号','银行名称','组织机构代码',
            '统一社会信用代码','机关单位','医院','学校','港澳通行证号','台湾通行证号','永久居住证号','中国护照','税务登记证号','医师资格证书编号','医师执业证书编号',
            '营业执照','车辆识别代号','公积金号','开户许可证号','银行卡号','军官证号','道路运输经营许可证号','军密认证号']

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained('pretrained_bert')
        # self.model = torch.load('/home/tzy/Ty_bert_clas/datas/model/bert_model.pth', map_location=self.device)
        self.model = torch.load('/home/tzy/Classification/model/bert_model.pth', map_location=self.device)
        
        self.model.eval()
        
    def predict(self, batch_x):
        inputs = self.tokenizer.batch_encode_plus(
                batch_x,
                padding="max_length",
                max_length=32,
                truncation="longest_first",
                return_tensors="pt")
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs[0]
            sm = torch.nn.Softmax(dim=1)
            max_tt = torch.max(sm(logits), 1)
            sorce = max_tt[0].tolist()
            label = [self.label_list[i] for i in max_tt[1].tolist()]
            for i in range(len(label)):
                if sorce[i]<0.6 or (label[i]=='国家' and sorce[i]<0.85):
                    label[i]='其他'
            combined = {}
            for i in range(len(label)):
                key = label[i]
                value = sorce[i]
                if key in combined:
                    combined[key] += value
                else:
                    combined[key] = value
            total = sum(combined.values())
            normalized_dict = {} 
            for key, value in combined.items():
                normalized_value = value / total
                normalized_dict[key] = normalized_value
            max_key = max(normalized_dict, key=normalized_dict.get)
            max_value = normalized_dict[max_key]
            return{"paras":max_key,"confidence":max_value}
        
    def __call__(self, data):
        a = []
        if isinstance(data,pd.DataFrame):
            if len(data)>50:
                data = data.sample(n=50)
            for cc in data.columns:
                if data[cc].values.dtype != 'object':
                    data[cc] = [str(i) for i in data[cc].values]
                batch_x = data[cc].dropna().values
                a.append(self.predict(batch_x))
        else:
            for s in data:
                a.append(self.predict(s))
        return a

#使用内容识别关联图谱节点
def content_relevance(graph, df, rest=None):
    pp = Pre()
    res = pp(df)
    pars = {'ps':"结果由AI生成，存在不确定性风险"}
    for te, cc in zip(res, df.columns):
        print(te['paras']+'---'+cc)
        d = graph.nodes.match('content',content_name=te['paras']).first()
        b = graph.nodes.match('field',explain=cc).first()
        if d and b:
            graph.create(Relationship(b,'belong1_to',d,**pars))
        elif d:
            print('field未找到：',cc)
        else:
            print('content未找到：',te['paras'])
    
    #没有分类分级的表，根据其字段的类进行投票从而确定其类与级
    if rest:
        for i in rest:
            cql = """MATCH (c:class)-[:class_of]->(co:content)<-[:belong1_to]-(f:field)<-[:table_of]-(t:table) where t.table_name='{}' return max(c.class_name)""".format(i)    
            aa = graph.run(cql).data()[0]['max(c.class_name)']
            a = graph.nodes.match("class",class_name=aa).first()
            c = graph.nodes.match("table",table_name=i).first()
            if a and c:
                graph.create(Relationship(c,'belong',a,**pars))
            elif a:
                print('class未找到：',i)
            else:
                print('table未找到：',aa)

if __name__=='__main__':
    pre = Pre()
    data = ['26347653785357','+8618748315659','8804213127662','520322200214042592']
    print(pre(data))