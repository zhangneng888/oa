# -*- coding: utf-8 -*-
#!/usr/bin/python
import mysql.connector
import time
import datetime

class MysqlDB:
    def __init__(self,host,user,password,port,database):
        try:
            self.dbConfig = {'host':host,'user':user,'password':password,'port':port,'database':database,'charset':'utf8'}
            self.cnn = mysql.connector.connect(**self.dbConfig)
            #print '数据库连接成功！'
        except  mysql.connector.Error as e:
            print '连接失败，原因',format(e)

    #查询
    def query_data(self,sql):
        cursor = self.cnn.cursor()
        select_data = []
        try:
            cursor.execute(sql)
            for id in cursor:
                group = (id)
                select_data.append(group)
            return select_data
        except mysql.connector.Error as e:
            print format(e)
        finally:
            cursor.close()
    #更新
    def update_data(self,sql):
        cursor = self.cnn.cursor()
        select_data = []
        try:
            cursor.execute(sql)
            self.cnn.commit()
            #return select_data
        except mysql.connector.Error as e:
            print format(e)
        finally:
            cursor.close()

host = '192.168.1.9'
password = 'Allin2018@prtg.com'
user = 'root'
port = '3306'
database = 'oa'
year = datetime.datetime.now().year
month = datetime.datetime.now().month
#查询并遍历部门信息
sql_department = 'select id from usermanager_department'
#查询资产表数据
sql_assets = 'select id,purchase_price,residual_value,depreciable_lives,applicaton_department_id,use_department_id from assets_assets'
my_db =  MysqlDB(host,user,password,port,database)
department_lists = my_db.query_data(sql_department)
assets_lists = my_db.query_data(sql_assets)
print '开始执行脚本:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
for item in department_lists:
    id = item[0]
    sql_userprice = 'select name_id,year,month from assets_userprice WHERE name_id = %s AND year = %s AND month = %s' % (item[0], year, month)
    #如果使用价值表中没有相应（部门+年+月）数据条目进行插入
    if not my_db.query_data(sql_userprice):
        insert_dept = 'INSERT INTO assets_userprice (name_id,year,month,price) VALUES (%s,%s,%s,%s)' % (item[0], year, month,0)
        my_db.update_data(insert_dept)
for item in assets_lists:
            purchase_price = item[1]
            residual_value = item[2]
            depreciable_lives = item[3]
            applicaton_department_id = item[4]
            use_department_id = item[5]
            depreciation_base = round(float(purchase_price) / (float(depreciable_lives) * 365.0), 2)
            if residual_value > 0 and residual_value > depreciation_base:
                # 更新使用部门使用价值
                if use_department_id:
                    price_sql = 'select price from assets_userprice where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\' ' % (
                    use_department_id, year, month)
                    price_date = my_db.query_data(price_sql)
                    price_value = float(price_date[0][0]) + float(depreciation_base)
                    update_price = 'update assets_userprice set price = %s where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\'' % (
                    price_value, use_department_id, year, month)
                    my_db.update_data(update_price)
                # 更新申请部门使用价值
                if not use_department_id:
                    price_sql = 'select price from assets_userprice where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\'' % (
                    applicaton_department_id, year, month)
                    price_date = my_db.query_data(price_sql)
                    price_value = float(price_date[0][0]) + float(depreciation_base)
                    update_price = 'update assets_userprice set price = %s where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\'' % (
                    price_value, applicaton_department_id, year, month)
                    my_db.update_data(update_price)
                # 更新资产表残余价值
                residual_value = float(residual_value) - float(depreciation_base)
                update_residual_value = 'update assets_assets set residual_value = %s where id = %s' % (residual_value, item[0])
                my_db.update_data(update_residual_value)
            if residual_value > 0 and residual_value < depreciation_base:
                # 更新使用部门使用价值
                if use_department_id:
                    price_sql = 'select price from assets_userprice where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\' ' % (
                        use_department_id, year, month)
                    price_date = my_db.query_data(price_sql)
                    price_value = float(price_date[0][0]) + float(residual_value)
                    update_price = 'update assets_userprice set price = %s where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\'' % (
                        price_value, use_department_id, year, month)
                    my_db.update_data(update_price)
                # 更新申请部门使用价值
                if not use_department_id:
                    price_sql = 'select price from assets_userprice where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\'' % (
                        applicaton_department_id, year, month)
                    price_date = my_db.query_data(price_sql)
                    price_value = float(price_date[0][0]) + float(residual_value)
                    update_price = 'update assets_userprice set price = %s where name_id = \'%s\' AND year = \'%s\' AND month = \'%s\'' % (
                        price_value, applicaton_department_id, year, month)
                    my_db.update_data(update_price)
                # 更新资产表残余价值
                residual_value = float(residual_value) - float(residual_value)
                update_residual_value = 'update assets_assets set residual_value = %s where id = %s' % (residual_value, item[0])
                my_db.update_data(update_residual_value)
print '完成执行脚本:',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
