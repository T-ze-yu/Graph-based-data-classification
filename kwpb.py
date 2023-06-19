from pypinyin import lazy_pinyin
import time
import torch
from similarities import Similarity
from py2neo import Relationship

class kwpb():
    def __init__(self,graph=None) -> None:
        self.sim_model = Similarity(model_name_or_path = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",device='cpu')
        self.graph = graph

    #判断是否中文
    def is_all_chinese(self, strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    #将中文关键字散射为拼音、英文等
    def scatter(self, word):
        # eng = self.translate(word)
        nzk = {
            '传真':['fax'],
        }
        eng = []
        if word in nzk:
            eng.extend(nzk[word])
        py_lb = lazy_pinyin(word)
        py1=''
        py2=''
        for i in py_lb:
            py1+=i
            py2+=i[0]
        eng.append(py1)
        eng.append(py2)
        return eng
        
    
    #根据关键字字典进行相似度匹配
    def get_res(self, keywords_dict, fields_metadata):        
        '''
        keywords_dict：dict，关键字字典，一般需要根据任务内置，
        例{'qq':['qq'],'微信':['wechat', 'weixin', 'wx'],'密码':['password', 'pass', 'passwd', 'pwd']}。
        fields_metadata：list，用来做词义匹配的名称，里面的元素可以是字符串或字典（字典一般包含名称和解释），
        例['pwd','sfz']或[{'field_name':'pwd','field_description':'登录密码'},
                            {'field_name':'sfz','field_description':'身份证号码'}]。
        '''
        nzk = {
            # 'del':'delete',
            'desc':'description'
        }
        res = []
        
        v1 = []
        n1 = []
        v2 = []
        n2 = []

        n=-1
        for fd in fields_metadata:         #对命名及解释的处理
            if isinstance(fd,str):
                v1.append(fd.lower())
                n+=1
                n1.append(n)
            else:
                # slb = re.split('[-_ ]',fd['field_name'].lower())
                # strs = ''
                # for i in slb:
                #     if i in nzk:
                #         strs+=nzk[i]+' '
                #     else:
                #         strs+=i+' '
                v1.append(fd['field_name'].lower())
                if fd['field_description']:                
                    dtem = fd['field_description'].lower().split('。')
                    v1.extend(dtem)
                    n+=len(dtem)
                n+=1
                n1.append(n)
        
        n=-1
        for itm in keywords_dict.items():      #对关键字的处理
            for kws in itm[1]:
                if self.is_all_chinese(kws):
                    itm[1].extend(self.scatter(kws))
            v2.extend(itm[1])
            n+=len(itm[1])
            n2.append(n)
        kylb = list(keywords_dict.keys())
            
        slys, indx = torch.max(self.sim_model.similarity(v1, v2), 1)
        
        cs = 0
        for i in n1:
            if i==cs:
                inx = self.find_inx(n2,indx[i])
                res.append((kylb[inx],slys[i],v2[indx[i]],v1[i]))
            else:
                sly,inx = torch.max(slys[cs:i+1],0)
                inx2 = self.find_inx(n2,indx[inx+cs])
                res.append((kylb[inx2],sly,v2[indx[inx+cs]],v1[inx+cs]))  #匹配到的类别、相似度、关键字、原字段名或解释
            cs = i+1
            
        return res    
    
    #插值查找
    def find_inx(self,nn,x):
        left = 0
        right = len(nn)-1
        if x<=nn[right]:
            while left<=right:
                if x<=nn[left]:
                    return left
                else:
                    left = left+((right-left)//(nn[right]-nn[left]))*(x-nn[left])+1    
                    if x<=nn[left-1]:
                        return left-1 

    
    def prid(self, keywords_dict,fields_metadata,lbe):
        t1=time.time()
        k = self.get_res(keywords_dict, fields_metadata)
        print('耗时：',time.time()-t1)
        acc=0
        if len(k)==len(lbe):
            for i in range(len(k)):
                print(k[i],lbe[i])

                if k[i][0]==lbe[i]:
                    acc+=1
            acc = acc/len(k)
            print('acc:',acc)
        else:
            print('标签错误')
            
    def keyword_relevance(self, fields_metadata, keywords_dict, ys_labe=None):
        ali = []
        k = self.get_res(keywords_dict, fields_metadata)
        for kk,f in zip(k,[i['field_name'] for i in fields_metadata]):
            if f in ys_labe:
                print(kk,f,ys_labe[f])
            else:
                print(kk,f)
        tab={'ps':'此结果由AI生成，存在不准确的现象'}
        for i in range(len(k)):
            if k[i][1] >= 0.7:
                # print(fields_metadata[i]['field_name'],k[i][0])
                a = self.graph.nodes.match("table",table_name=fields_metadata[i]['field_name']).first()
                b = self.graph.nodes.match("class",class_name=k[i][0]).first()
                try:
                    aaa = Relationship(a,"belong_to",b,**tab)
                    self.graph.create(aaa)
                except:
                    if a :
                        print('该class_name未找到：',k[i][0])
                    else:
                        print('该table_name未找到：',fields_metadata[i]['field_name'])
            else:
                # print(fields_metadata[i]['field_name'], k[i])
                ali.append(fields_metadata[i]['field_name'])
        return ali
    
if __name__ == "__main__":
    pass 
    
    