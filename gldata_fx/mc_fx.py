#分词
def split_english(text):
    # 初始化结果列表
    result = [text[0]]
    bj = False
    # 遍历字符串，将大写字母作为分隔符进行分词
    for i in range(1,len(text)):
        if bj:
            result.append("_") 
            bj=False
        elif text[i].isupper():
            if i != len(text)-1:
                if not(text[i-1].isupper()) or text[i+1].islower():
                    result.append("_")    
            elif not(text[i-1].isupper()) :
                result.append("_")
        elif text[i].isdigit():
            if not text[i-1].isdigit():
                result.append("_")   
            if i != len(text)-1 and not text[i+1].isdigit():
                bj = True
        result.append(text[i])
    # 将结果列表转换为字符串并返回
    return "".join(result).split('_')

#获取特定schema的表名
def get_schema(js, schema = None):
    #schema=7(emr),8(ip),9(op)  str
    
    db = js['dt'].get('db_0', {})
    iplb = []
    ind = 0  # 设置初始值为0
    while True:
        tb = f"table_{ind}"
        if tb in db:
            if schema :
                if schema in str(db[tb].get("TABLE_SCHEMA", "")):
                    iplb.append(db[tb]["name"])
            else:
                iplb.append(db[tb]["name"])
            ind += 1
        else:
            break
    return iplb

#获取所有字段名称
def get_fds(dbs):
    db = dbs['dt'].get('db_0', {})
    iplb = []
    ind = 0  # 设置初始值为0
    while True:
        tb = f"table_{ind}"
        if tb in db:
            for fd in db[tb]:
                if fd[:6] == 'field_':
                    iplb.append(db[tb][fd]['name'])
            ind += 1
        else:
            break
    return iplb

def is_any_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False
#将词汇释义拼接起来组成完整的名称解释
def mcfy(text, js):
    '''
    lb:list 该名称分词后所有的词汇
    js:json 存储词汇解释的字典
    '''
    lb = split_english(text)
    res = ''
    for i in lb:
        if i and i.lower() in js:
            res += js[i.lower()]+'__'
        elif i.isdigit():
            res += i+'__'
        elif len(i) < 3:
            res += i+'__'
        elif is_any_chinese(i):
            res += i+'__'
        else:
            print('目前该词汇字典没有收纳：'+i)
    return res