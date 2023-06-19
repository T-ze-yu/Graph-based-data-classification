from py2neo import Graph

class Config(object):
    def __init__(self, port='7474'):
        self.graph = Graph("http://172.24.4.101:" + port, auth=("neo4j", "ad_neo4j"))
        self.keywords_dict = {
        '个人身份信息': ['患者身份信息','个人生物信息','病人记录'],
        
        #医疗应用数据
        '检查检验数据': ['细菌','药物敏感','检验项目条码','检查检验','检查项目','检查登记','检查','检验','检查项目明细','检验结果','结果'],
        '药物数据': ['药物','药物基本信息','药品名称','药品','发药账单明细','麻醉药物请求','处方明细','Drug'],
        '麻醉数据': ['麻醉','麻醉记录'],
        '输血数据': ['输血','血液','血型','输血记录','ABO型血'],
        '住院信息': ['住院数据','住院记录','诊断','住院医嘱','会诊','Consultation','住院诊断','DrugSend'],
        '门诊信息': ['门诊信息','门诊','病历','配方咨询'],
        '出院信息': ['出院','出院数据'],
        
        #医院运营数据
        '日常数据': ['日常','抗菌相关','抗菌药物相关','会诊','HIS接口日志','Anti','婴儿情况','病人担保','病区日志','预约','挂号','护理不良','单据'],
        '培训相关': ['培训','轮转信息'],
        '物资数据': ['物资','入库','出库','盘点','库房参数','药品入库申请','药品调价批次','药品基本信息','药品盘点','药品借药还药明细', '中标', '招标', '清算','调价','药品调价明细','药品调价','药品日结','药品库存日志'],
        '后勤相关': ['后勤', '膳食菜单','膳食基本项目明细'],
        '财务数据': ['项目分支价格','财务', '欠费','结算员日结明细','收费药房方案','门诊收款日结','固定收费项目','血液成分费用明细','调价','药房发票明细','损坏账单'],
        '人力数据': ['人力资源','审计','人员数据','人员','员工代码','员工信息变更','人员数据台帐','医生','护士信息','值班'],
        '临床数据': ['临床数据','Clinical','ClinicalPathway'],
        '日志数据': ['日志'],
        
        #医院基本数据
        '疾病数据': ['政策疾病','疾病类别','诊断类别'],
        '文书数据':['模板','日志'],
        '时间限制相关':['时间限制'],
        '科室数据': ['科室','科室设置','科室信息','科室代码','Dept'],
        '基础运行数据': ['基础数据','收费科室','国家','学历','Diagnose','病种分类','条码分类','诊断类别','常用诊断','房间','楼层'],
        
        #医疗资金和支付数据
        '医疗交易信息': ['费用', '结算', '住院费用', '门诊结算', '账单','预交金','住院费用汇总','交易记录','膳食交易记录','膳食结算信息','膳食预交金','膳食明细'],
        '保险信息': ['保险','社会保险','医保对账','医保项目对照','医保信息','医保'],
        }
        
        self.fg_path = '/home/tzy/Classification/datas/fg_for_gl.json'  #法规信息路径
        self.db_path = '/home/tzy/Classification/datas/gl_dbs.json'     #数据资产信息路径
        self.cihsy_path = '/home/tzy/Classification/datas/cihsy.json'     #词汇释义字典路径
        self.ys_path = '/home/tzy/Classification/datas/映射表.json'
        
        self.content_path = '/home/tzy/Classification/datas/test.csv'
        
        self.mgkey_dic = {
            '邮箱':['mail', 'notify_mails', 'auth_mail', 'email_address', 'InternalEMailAddress', 'mailboxesToSelect'],
            '电话号码':['tel', 'phone', 'telephone', 'mobile'],
            'qq':['qq'],
            '微信':['wechat', 'weixin', 'wx'],
            '密码':['password', 'pass', 'passwd', 'pwd'],
            '身份证号码':['shenfenzheng','IDcard', 'identitycard','sfzh'],
            '军官证号码':['junguanzheng', 'MilitaryID',],
            '居住证号码':['juzhuzheng', 'ResidentCard',],
            '驾驶证号码':['driver_license',],
            '社保卡':['shebaoka', 'socialsecurity_number',],
            '护照号码':['passport',],
            '银行':['bank_name','bank'],
            '银行号码':['bank_account', 'deposit_account',],
            '信用卡号码':['credit_card', 'debit_card',],
            '支付宝':['alipay',],
            '地点':['location', 'area', 'address', 'zone', 'region_zh', 'position',],
            '姓名':['family', 'xingming', 'contact', 'full_name', 'zh_name', 'customername', 'name_pinyin', 'employeeName', 'name_pinyin',],
            '户口':['household_registration',],
            '政治面貌':['politicalAffiliation',],
            '生日':['birthday',],
            '性别':['sex',],
            '职业':['job',],
            '婚姻状况':['married', 'single',],
            '种族':['race',],
            '学历':['educational_background', 'academic_qualifications',],
            '港澳通行证':['Exit-Entry_Permit',],
            '公司':['company',],
            '税务号码':['Tax_Identification_Number',],
            '牌照':['license_plate',],
            '公积金':['accumulation_fund',],
            '密钥':['key', 'private_key', 'public_key']
        }
        