from py2neo import Graph

class Config(object):
    def __init__(self, port='7474'):
        self.graph = Graph("http://172.24.4.101:" + port, auth=("neo4j", "ad_neo4j"))
        self.keywords_dict = {
        '人口统计信息': ['婚姻状态','国家','地区','性别','收入','民族','职业','教育','家庭关系'],
        # '个人身份信息': ['婴儿信息','患者信息','患者身份信息','个人生物信息','病人记录','患者登记信息','身份证号码', '军官证号码', '居住证号码', '驾驶证号码', '社保卡','护照号码' ],
        '个人通讯信息': ['邮箱','电话号码','qq','微信','账号密码','患者登记信息'],
        '个人支付信息': ['银行', '银行号码', '信用卡号码', '支付宝'],
        '患者个人信息': ['病人信息表','卡信息表','患者身份','患者'],
        
        #医疗应用数据
        '检查检验数据': ['细菌结果','药物敏感','检验项目条码','检查检验','检查项目','检查登记','检查','检验','检查项目明细','检验结果','结果'],
        '用药数据': ['发药账单明细','麻醉药物请求','处方审核','RecipeAudit'],
        '麻醉数据': ['麻醉','麻醉记录'],
        '输血数据': ['输血等待','血液类型','血液处方','输血','血液','血型','输血记录','ABO型血','血液组件'],
        '住院信息': ['住院数据','住院记录','诊断','住院医嘱','会诊','Consultation','住院诊断','DrugSend'],
        '门诊信息': ['转诊','门诊信息','门诊','病历','配方咨询','登记历史','自我评估','自助处方','处方明细','处方种类','处方操作'],
        '出院信息': ['出院','出院数据'],
        '手术数据': ['手术路径','手术信息','手术过程','手术申请','手术工作人员','手术情况'],
        '妊娠数据': ['妊娠'],
        '病情数据': ['患者跟踪','病情'],
        '医嘱数据': ['医嘱','医嘱治疗','医嘱执行','ExternalRecipe','ItemFreq','血液医嘱'],
        '临床数据': ['临床路径','临床住院','临床数据','Clinical','ClinicalPathway'],
        '治疗数据': ['治疗','治疗用法','治疗申请','治疗执行','患者固定项目','治疗内容','护理内容'],

        #医院运营数据
        '日常数据': ['挂号科室权限管理','登记等待池','归档记录','拓展数据来源','日常','抗菌相关','抗菌药物相关','会诊','HIS接口日志','Anti','婴儿情况','病人担保','病区日志','预约','挂号','护理不良','单据','护理评估','医生授权'],
        '培训相关': ['培训','轮转信息'],
        '物资数据': ['药品发送','药品库存','物资','入库','出库','盘点','库房参数','药品入库申请','药品调价批次','药品盘点','药品借药还药明细', '中标', '招标', '清算','调价','药品调价明细','药品调价','药品日结','药品库存日志','打印','物流'],
        '后勤相关': ['后勤', '膳食菜单','膳食基本项目明细'],
        '财务数据': ['住院医生账本记录','医生账本类型','血液费用','材料收费','费率规则','财务', '欠费','结算员日结明细','收费药房方案','门诊收款日结','固定收费项目','血液成分费用明细','调价','药房发票明细','损坏账单','费用设置规则','就诊费用设置数据'],
        '人力数据': ['ShiftRelief','交接班','人力资源','审计','人员数据','人员','员工代码','员工信息变更','人员数据台帐','医生','护士信息','值班','Staff'],
        '维护数据': ['账户项目','用户医嘱日志','可扩展','ScalableField','解决方案设置','基础设置','设置','项目数据','服务器数据','特殊字符数据','同步脚本','系统配置','短信服务','消息处理','用户对象','应用'],
        '图表数据': ['图表数据'],
        '质量数据': ['评估记录','非法记录','非法任务','不良反应事件','投诉','质量问题'],
        '报告数据': ['报告数据','报告主题数据'],
        '科室管理': ['OperationDept','手术设备扩展','手术器械管理','OperationAttachMent','ETOReportData','ETOReportItem','ETOReport','手术室报表'],
        '错误相关': ['ConsultationToPdfError','OrderToPdfError','MedicalRecordToPdfError'],
        
        #医院基本数据
        '分类数据': ['测量种类','班次种类','项目种类','床位种类','排序种类','就诊种类','离开种类','出院医保结算种类','就诊原因种类','医嘱种类','会诊种类','通知种类','患者体征种类','缴费种类','身份种类'],
        '疾病数据': ['政策疾病','疾病类别','诊断类别'],
        '文书数据':['模板','日志','药材模板数据','档案管理','归档','住院文档'],
        '时间限制相关':['时间限制'],
        '科室数据': ['科室','科室设置','科室信息','科室代码','Dept','父部门','部门种类'],
        '基础运行数据': ['MetricUnit','VW_InFstpages','VW_County','VW_Province','VW_City','医院','基础数据','收费科室','国家','学历','Diagnose','病种分类','条码分类','诊断类别','常用诊断','房间','楼层','模板','版本','手术字典','手术费用模板'],
        '区域配置数据':['输血配置','屏幕配置'],
        '药品信息':['基础药品','药品限制','药品种类','药物基本信息','药品名称','药品用法','Drug'],

        #医疗资金和支付数据
        '医疗交易信息': ['ChargeItemMRFeeRelation','住院患者押金','患者押金','结算','EMRAccItem','OPYBAccItem','OPAccItem','IPAccItem','住院账户','住院','费用', '结算', '住院费用', '门诊结算', '账单','预交金','住院费用汇总','交易记录','膳食交易记录','膳食结算信息','膳食预交金','膳食明细','结算','治疗费用','就诊费用'],
        '保险信息': ['保险','社会保险','医保对账','医保项目对照','医保信息','医保','国际疾病分类'],

        # 其他类(看不出来有什么作用或者不知道分到哪一类的)
        # '其他' : ['条形码配置(BarcodeConfig)','工作站(Workstation)','文件夹(Folder)','个人','保证__ (Guarantee)']
        }
        

        self.fg_path = '/home/tzy/Classification/datas/fg_for_dh.json'  #法规信息路径
        self.db_path = '/home/tzy/Classification/datas/gl_dbs.json'     #数据资产信息路径
        self.cihsy_path = '/home/tzy/Classification/datas/cihsy.json'     #词汇释义字典路径
        self.ys_path = '/home/tzy/Classification/datas/映射表.json'
        
        self.content_path = '/home/tzy/Classification/datas/test.csv'
        
        self.mgkey_dic = {
            '邮箱':['mail', 'notify_mails', 'auth_mail', 'email_address', 'InternalEMailAddress', 'mailboxesToSelect'],
            '电话号码':['tel', 'phone', 'telephone', 'mobile'],
            'qq':['qq'],
            '微信':['wechat', 'weixin', 'wx'],
            '账号密码':['password', 'pass', 'passwd', 'pwd'],
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
        