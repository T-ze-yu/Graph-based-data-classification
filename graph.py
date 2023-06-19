from kwpb import kwpb
from py2neo import Relationship,Node
from mc_fx import mcfy
import pandas as pd

class GRaphs():
    def __init__(self, graph) -> None:
        self.graph = graph
        self.relat1 = ['database','table','field']
        self.relat2 = ['bgclass','class', 'content']
        self.mode = 'fg'
        self.lev_lb = []        #按序存放级别节点
        self.classes = []       #按序存放classes节点
        self.SCHEMA = []        #按序存放SCHEMA节点
        
        self.tbs = []        #存放表的词义匹配信息
        self.fds = []        #存放列的词义匹配信息
        
    
    #构建二级细分类和level节点
    def plug_fg(self,datas):
        if 'classes' in datas:
            id = 0
            for cla in datas['classes']:
                clas=datas['classes'][cla]
                nd = Node('classes',classes_id=id, classes_name=clas['name'],explain=clas['description'])
                id += 1
                self.graph.create(nd)
                self.classes.append(nd)    #按照索引顺序依次存储
                
        for lev in datas['level']:
            lev=datas['level'][lev]
            nd = Node('level',level_id=lev['name'], level_name=lev['name'],数据特点=lev['数据特点'],适用场合=lev['适用场合'],特征与案例=lev['特征与案例'],安全措施要点=lev['安全措施要点'])
            self.graph.create(nd)
            self.lev_lb.append(nd)
    
    #数据资产构建逻辑补充节点
    def plug_db(self,datas):
        if 'TABLE_SCHEMA' in datas:
            id = 0
            for cla in datas['TABLE_SCHEMA']:
                clas=datas['TABLE_SCHEMA'][cla]
                nd = Node('schema',schema_id=id, schema_name=clas['name'],explain=clas['description'])
                id += 1
                self.graph.create(nd)
                self.SCHEMA.append(nd)    #按照索引顺序依次存储
            
    #通过主要的三层关系构建图谱
    def chage(self, datas, relat, cihsy):
        graph = self.graph
        i = 0
        i1 = 0
        i2 = 0
        for db in datas:        #构建大类和与细分类的关系  或者构建库
            lib = Node(relat[0],**{relat[0]+'_id':i,relat[0]+'_name':datas[db]["name"],'explain':datas[db]["description"]})
            graph.create(lib)
            if 'classes' in datas[db]:
                for ii in datas[db]['classes']:
                    graph.create(Relationship(lib, 'bgclass_of' ,self.classes[ii]))  #根据bgclass下所有classes索引查找节点并建立关系
            if self.SCHEMA:
                for ii in self.SCHEMA:
                    graph.create(Relationship(lib, 'db_of', ii))  #根据bgclass下所有classes索引查找节点并建立关系
            i += 1
            
            for table in datas[db]:        #构建表和表与库的类型   或者构建类和类与大类与细分类与级的关系
                if table not in ["name", "description",'classes']:
                    name = datas[db][table]["name"]
                    description = datas[db][table]["description"]
                    if not description and cihsy:
                        description = mcfy(name, cihsy)
                    tb = Node(relat[1],**{relat[1]+'_id':i1,relat[1]+'_name':name,'explain':description})
                    graph.create(tb)
                    if 'classes' in datas[db][table]:
                        ii = datas[db][table]['classes']
                        graph.create(Relationship(self.classes[ii], 'classes_of', tb))  #根据classes索引查找节点并建立关系
                    elif 'TABLE_SCHEMA' in datas[db][table]:
                        ii = str(datas[db][table]['TABLE_SCHEMA']).split('、')
                        for i in ii:
                            graph.create(Relationship(self.SCHEMA[int(i)], 'SCHEMA_of', tb))  #根据SCHEMA索引查找节点并建立关系
                    else:
                        graph.create(Relationship(lib,relat[0]+'_of',tb))
                    i1 += 1
                    if self.mode == 'fg':
                        level = datas[db][table]["level"]
                        assert int(level)<=len(self.lev_lb),'所属级别超出范围，请在level中更正。'
                        graph.create(Relationship(tb,'level_of',self.lev_lb[int(level)-1]))
                        
                    for field in datas[db][table]:      #构建字段和字段与表的关系  或者构建内容和内容与类与级的关系
                        if field[:6] == 'field_' or field[:8] == 'content_':
                            field = datas[db][table][field]
                            field_name = field["name"]
                            explain = field["description"]
                            if cihsy:
                                explain = mcfy(field_name, cihsy) + '。 ' +explain
                            
                            #查找该内容或字段节点是否存在
                            d = graph.nodes.match(relat[2],**{relat[2]+'_name':field_name}).first()  
                            if not d:
                                d = Node(relat[2],**{relat[2]+'_id':i2,relat[2]+'_name':field_name,'explain':explain})
                                graph.create(d)
                            graph.create(Relationship(tb,relat[1]+'_of',d))
                            i2 += 1
                            if 'level' in field:
                                level = field["level"]
                                assert int(level)<=len(self.lev_lb),'所属级别超出范围，请在level中更正。'
                                graph.create(Relationship(d,'level_of',self.lev_lb[int(level)-1]))
                                
        print(self.mode,"finish!")
        return 0

    def jsto_graph(self, data, mode=None, cihsy=None):
        if mode:
            self.mode = mode
        if self.mode == 'fg':
            self.plug_fg(data)
            return self.chage(data['dt'],self.relat2, cihsy)
        else:
            self.plug_db(data)
            return self.chage(data['dt'], self.relat1, cihsy)

    #获取名称和解释转换为词义匹配格式
    def get_metadata(self, md='simple'):
        '''
        md:生成的模式 simple是简单模式列表元素是字符串，否则列表元素是字典
        '''
        for i in self.graph.nodes.match('table').all():
            if md == 'simple':
                self.tbs.append(i.get('table_name'))
            else:
                self.tbs.append({'field_name': i.get('table_name'), 'field_description': i.get('explain')})
                
        for j in self.graph.nodes.match('field').all():
            if md == 'simple':
                self.fds.append(j.get('field_name'))
            else:
                self.fds.append({'field_name': j.get('field_name'), 'field_description': j.get('explain')})

    #将表和列进行词义匹配，并取结果使图谱关联
    def keyword_relevance(self, tb_yz, fd_yz, keywords_dict, mgkw_dict):
        '''
        tb_yz：float 表进行词义匹配时的阈值
        fd_yz：float 表进行词义匹配时的阈值
        keywords_dict：关键词字典用来做词义匹配
        '''
        self.kwpb = kwpb()
        ps={'ps':'此结果由AI生成，存在不准确的现象'}
        res1 = self.kwpb.get_res(keywords_dict, self.tbs)
        res2 = self.kwpb.get_res(mgkw_dict, self.fds)
        
        df1 = pd.DataFrame(columns=['类别','相似度','关键字','原名称（表或字段名）'])
        df2 = pd.DataFrame(columns=['类别','相似度','关键字','原名称（表或字段名）'])
        x = 0
        for i,j in zip(res1,self.tbs):
            if isinstance(j,dict):
                j = j['field_name']
            if i[1]>tb_yz:
                df1.loc[x] = i[:3]+(j,); x += 1 
                table_node = self.graph.nodes.match("table",table_name=j).first()
                class_node = self.graph.nodes.match("class",class_name=i[0]).first()
                try:
                    rship = Relationship(table_node,"belong_to",class_node,**ps)
                    self.graph.create(rship)
                except:
                    if table_node:
                        print('该class_name未找到：',i[0])
                    else:
                        print('该table_name未找到：',j)
            else:
                df1.loc[x] = i[:3]+(j,); x += 1 
                
        for i,j in zip(res2,self.fds):
            if isinstance(j,dict):
                j = j['field_name']
            if i[1]>fd_yz:
                df2.loc[x] = i[:3]+(j,); x += 1 
                field_node = self.graph.nodes.match("field",field_name=j).first()
                class_node = self.graph.nodes.match("class",class_name='个人身份信息').first()
                ps.update({'敏感类型':i[0]})
                try:
                    rship = Relationship(field_node,"belong_to",class_node,**ps)
                    self.graph.create(rship)
                except:
                    if field_node:
                        print('该class_name未找到：',i[0])
                    else:
                        print('该field_name未找到：',j)
            else:
                df2.loc[x] = i[:3]+(j,); x += 1 
        return df1, df2

if __name__ == "__main__":
    pass
    # from py2neo import Graph
    # pp = jsto_graph(Graph("http://172.24.4.101:7000", auth=("neo4j", "ad_neo4j")))
        
    # import json
    # # with open("/home/tzy/Classification/fg2.json") as fp:
    # #     a = json.load(fp)
    # #     print(pp(a))

    # # with open("/home/tzy/Classification/json.json") as fp1:
    # #     a = json.load(fp1)
    # # print(pp(a,'hh'))
    # with open("/home/tzy/Classification/datas/sjzd.json") as fp1:
    #     a = json.load(fp1)
    # # print(a)
    # print(pp(a,'hh'))
    
    