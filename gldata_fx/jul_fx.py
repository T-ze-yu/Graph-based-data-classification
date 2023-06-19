from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.cluster import KMeans, DBSCAN
from mc_fx import split_english, mcfy
from gensim.models import KeyedVectors
import numpy as np

class my_jul():
    def __init__(self, texts, cihsy_dc) -> None:
        '''
        texts:list 存放需要做聚类的文本
        cihsy_dc:json 词汇的释义字典
        '''
        self.jul_respath = '/home/tzy/Classification/gldata_fx/jul_res/'
        glove_file = 'glove.6B.100d.txt'
        self.model = KeyedVectors.load_word2vec_format(glove_file, binary=False)  # 加载预训练 GloVe 模型
        self.texts = texts
        self.cih_lb = [split_english(i) for i in texts] #分词
        self.syi = [mcfy(i,cihsy_dc) for i in texts] #释义
    
    def to_vec(self):
        # 将文本转换为向量表示
        vectors = []
        i = 0
        while i < len(self.cih_lb):
            # 取每个文本中所有单词向量的平均值作为该文本的向量表示
            vec_mean = np.mean([self.model[w.lower()] for w in self.cih_lb[i] if w.lower() in self.model], axis=0)
            if isinstance(vec_mean,np.ndarray):
                vectors.append(vec_mean)
                i+=1
            else:
                print(self.cih_lb.pop(i))
                print(self.syi.pop(i))
                print(self.texts.pop(i))
        return vectors
    
    
    def kmeans_jul(self, k, vectors):
        # 使用 KMeans 聚类算法进行聚类
        kmeans = KMeans(n_clusters=k, random_state=0).fit(vectors)
        # 输出聚类结果
        labels = kmeans.labels_
        with open(self.jul_respath+'km_res.txt','w') as f:
            for i in range(k):
                f.write(f'Cluster {i+1}:\n')
                for j, text in enumerate(zip(self.syi,self.texts)):
                    if labels[j] == i:
                        f.write(f'{text}\n')
            # 计算轮廓系数
            s = silhouette_score(vectors, labels, metric='euclidean')
            f.write(f"\n轮廓系数：{s}\n")
            # 计算DBI值
            dbi = davies_bouldin_score(vectors, labels)
            f.write(f"DBI: {dbi}\n")
    
    def dbcan_jul(self, vectors):
        clustering = DBSCAN(eps= 2,min_samples= 2).fit(vectors)
        # 输出聚类结果
        labels = clustering.labels_
        with open(self.jul_respath+'dbsc_res.txt','w') as f:
            for i in range(max(labels)+2):
                f.write(f'Cluster {i+1}:\n')
                for j, text in enumerate(zip(self.syi,self.texts)):
                    if labels[j] == i-1:
                        f.write(f'{text}\n')
            # 计算轮廓系数
            s = silhouette_score(vectors, labels, metric='euclidean')
            f.write(f"\n轮廓系数：{s}\n")
            # 计算DBI值
            dbi = davies_bouldin_score(vectors, labels)
            f.write(f"DBI: {dbi}\n")
    
    def __call__(self, md='both',k=114):
        vectors = self.to_vec()
        if md == 'kmeans':
            self.kmeans_jul(k, vectors)
        elif md == 'dbscan':
            self.dbcan_jul(vectors)
        else:
            self.kmeans_jul(114, vectors)
            self.dbcan_jul(vectors)
            
            
if __name__ == "__main__":
    import json
    from mc_fx import get_schema, get_fds
    with open("/home/tzy/Classification/datas/gl_dbs.json") as fp1:
        dbs = json.load(fp1)
    with open("/home/tzy/Classification/datas/cihsy.json") as fp1:
        cihsy = json.load(fp1)
        
    # tbs = get_schema(dbs) #获取所有表名
    tbs = get_fds(dbs) #获取所有字段名
    jl = my_jul(tbs, cihsy)
    jl()