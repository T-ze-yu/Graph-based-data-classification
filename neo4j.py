from py2neo import Graph,Node
# 链接图数据库
graph = Graph("http://172.24.4.101:7474", auth=("neo4j", "ad_neo4j"))

def get_lj():
    # if fd:
    #     cql = '''match (l:level)<-[:level_of]-(c:class)<-[:class_of]-(:table{{table_name:'{}'}})<-[:table_of]-(:content{{content_name:'{}'}}) 
    #                 return c.class_name,l.level_name'''.format(table,fd)
    # else:
    #     cql = '''match (l:level)<-[:level_of]-(c:class)<-[:class_of]-(:table{{table_name:'{}'}})
    #                 return c.class_name,l.level_name'''.format(table,fd)
    # 根据表查询所属等级和类别
    print("""请选择输入对象。1:根据表查询所属等级和类别。2:根据字段查询所属等级。3:根据字段查询该字段所属的所有表
          4:查询某张表的所有字段。5:查询链接数大于1的所有字段。6:查询某个字段所属类和级别
          7:根据给定的表，查询表中的字段在哪些表中出现过,8:退出""")
    while True:
        insup = input("请输入1-8:")
        if insup ==  "1":
            table = input("请输入表名称:")
            
            cql = '''MATCH (t:table)-[:belong_to]->(class:class)-[:level_of]->(level:level)WHERE t.table_name = "{}"
                        RETURN level.level_id,class.class_name'''.format(table)
            if graph.run(cql).data() == []:
                print("该表暂无对应分类分级！")
            else:
                print('等级为:',graph.run(cql).data()[0]['level.level_id'],"类别为:",graph.run(cql).data()[0]['class.class_name'])
            # return graph.run(cql).data()
            
        elif insup ==  "2":
            field = input("请输入字段:")
            table = input("请输入表名称:,可选:")
            cql = """MATCH (field:field{{field_name:'{}'}})-[:belong1_to]->(content:content)<-[:class_of]-(class:class)<-[:bgclass_of]-(:bgclass), (class)-[:level_of]->(level:level) 
            RETURN level.level_name, class.class_name""".format(field)
            if graph.run(cql).data() == []:
                if table:
                    cql = """MATCH (field:field{{field_name:'{}'}})<-[:table_of]-(table:table{{table_name:'{}'}})-[:belong_to]->(class:class)<-[:bgclass_of]-(:bgclass), (class)-[:level_of]->(level:level) 
            RETURN level.level_name, class.class_name""".format(field,table)
                else:
                    t = 0
                    cql = """MATCH (field:field{{field_name:'{}'}})<-[:table_of]-(table:table)-[:belong_to]->(class:class)<-[:bgclass_of]-(:bgclass), (class)-[:level_of]->(level:level) 
            RETURN level.level_name, class.class_name""".format(field)
            if graph.run(cql).data() == []:
                if t == 0:
                    print("未直接对该字段进行分类定级，请输入所在表进行辅助分类定级")
                # 如果非直连 提示输入表 如果不对的话
                print("该字段暂无对应信息！")
            # print(graph.run(cql).data()[])
            else:
                for x in range(len(graph.run(cql).data())):
                    print('类别：',graph.run(cql).data()[x]['class.class_name'],graph.run(cql).data()[x]['level.level_name'])
        # 查询某个字段所属的所有表
        elif insup ==  "3":
            field = input("请输入字段：")
            cql = '''MATCH (field:field)<-[:table_of]-(table:table) where field.field_name='{}' return table.table_name
                    '''.format(field)
            if graph.run(cql).data() == []:
                print("未查询到相关信息！")
            else:
                print('查询到的表为：',[x['table.table_name'] for x in graph.run(cql).data()])
            # print(graph.run(cql).data())
            
        # 查询某张表的所有字段
        elif insup ==  "4":
            table = input("请输入表名称：")
            cql = """match (t:table)-[:table_of]->(field:field) where t.table_name='{}'return field.field_name,field.explain""".format(table)
            if graph.run(cql).data() == []:
                print("未查询到相关信息！")
            else:
                print('查询到的字段为：',[x['field.field_name'] for x in graph.run(cql).data()])

        # 查询连接数大于5的所有字段
        elif insup ==  "5":
            # table = input("请输入")
            cql = """MATCH (field:field)-[r]-() WITH field, count(r) as rel_count WHERE rel_count > 5 RETURN field.field_name"""
            if graph.run(cql).data() == []:
                print("未查询到相关信息！")
            else:
                print('查询到的字段为',[x['field.field_name'] for x in graph.run(cql).data()])
            # 输出字段名称
            
        # 给定一张表，(查询表中的字段) 在哪些表出现过，返回字段 不是表
        # 等价于给定一张表，返回这张表中链接关系大于1的字段
        elif insup == "6":
            table = input("请输入表名称")
            cql = """MATCH (field:field)<-[:table_of]-(:table{{table_name:'{}'}})<-[:database_of]-(database:database),count(r) as rel_count WHERE rel_count > 5 RETURN field.field_name
            MATCH (field)<-[:table_of]-(tables:table)
            return tables.table_name""".format(table)
            if graph.run(cql).data() == []:
                print("未查询到相关信息！")
            else:
                print('出现过的表为:',[x['tables.table_name'] for x in graph.run(cql).data()])

        elif insup == "8":
            return 0
        # 查询每个类下面的数据资产有多少，针对于表,从高到低排序
        """MATCH (c:class)
        OPTIONAL MATCH (c)<-[:belong_to]-(t:table)
        RETURN c.class_name, COUNT(t) as table_count
        ORDER BY table_count DESC"""
        
        # 总结cypher查询语法
        # 第一步使用MATCH构造查询方式
        # MATCH函数，如果存在则找到，如果不存在则新建，( )表示实体，[ ]表示关系
        # MATCH(定义名字，可以不写:实体名称)——(横线表示没有指向)[定义名字，后面如果没用到可以不写:关系名称]->(->或者<-表示指向关系，放到关系的后面) (目标名称:目标实体名称)
        # MATCH串入多关系线时，使用逗号分割
        # 
        '''MATCH (field:field)-[r]-() WITH field, count(r) as rel_count WHERE rel_count > 1
        MATCH p = (field)-[r]-() 
        RETURN p
        print(cql)
        return graph.run(cql).data()'''

    print(get_lj())
if __name__ == "__main__":
    get_lj()