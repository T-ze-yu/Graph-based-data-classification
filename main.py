from config_1 import Config
from graph import GRaphs
# from Bert_cla import content_relevance

import json

#读取json文件
def js_dic(path):
    with open(path) as fp:
        dic = json.load(fp)
    return dic

def main():
    cnf = Config('7474')  #加载配置文件，连接图谱
    Graphs = GRaphs(cnf.graph)    #Graphs类初始化
    
    # cnf.graph.delete_all() #清空图谱
    Graphs.jsto_graph(js_dic(cnf.fg_path))   #将分类分级法规字典转换为图谱
    # datas = js_dic(cnf.db_path) #获取数据资产信息的字典
    # Graphs.jsto_graph(datas,'db',js_dic(cnf.cihsy_path)) #将数据资产信息字典转换为图谱，cihsy_path词汇字典，当需要程序释义时传入该参数

    # cnf.graph.run("MATCH ()-[r:belong_to]-() DELETE r")  #清空图谱中数据资产与分类标准之间的关联关系
    Graphs.get_metadata(md='fz') #根据数据资产信息获取词义匹配的表和字段
    df1, df2 = Graphs.keyword_relevance(tb_yz=0.5, fd_yz=0.8, keywords_dict=cnf.keywords_dict, mgkw_dict=cnf.mgkey_dic) #词义匹配进行图谱关联
    df1.to_csv('match_res/wordmatch_res_tb2.csv',index=False,encoding='utf_8_sig')
    df2.to_csv('match_res/wordmatch_res_fd2.csv',index=False,encoding='utf_8_sig')

    
if __name__ == "__main__":
    main()
     
    # kw_pb = kwpb(cnf.graph) #采用关键字匹配技术关联图谱
    # ys_labe = js_dic(cnf.ys_path) #真实的标签映射（可传可不传）
    # res = kw_pb.keyword_relevance(get_fields_metadata(datas), cnf.keywords_dict, ys_labe)
    # print(res)
    # # res = ['Access_control']
    # df = pd.read_csv(cnf.content_path)  #采用内容识别技术关联图谱
    # content_relevance(cnf.graph, df,res)  
    

