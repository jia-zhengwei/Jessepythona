# -*- coding: utf-8 -*-

from mssql import mssql
from mysql import mysql
import re
import os
import shutil

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import csv


class order_da:
    def __init__(self):
        self.msdb = mssql()
        self.mysqldb = mysql()

    def inser_sql(self, list):
        '''
        生成insert
        :param list: 
        :return: 
        '''
        insertsql = "INSERT IPP3.dbo.Product (SOSysNo,UserId,Name) "
        if list:
            for order in list:
                if insertsql.find("VALUES") > 0:
                    insertsql += ",(%s,%s,'%s')" % (order[0], order[2], order[3])
                else:
                    insertsql += "VALUES (%s,%s,%s)" % (order[0], order[2], order[3])
        return insertsql

    def query_user(self):
        '''
        查询下过单用户
        :return: 
        '''
        sql = "SELECT DISTINCT CustomerSysNo FROM IPP3.dbo.SO_Master WITH(NOLOCK)"
        user_list = self.msdb.execQuery(sql)

        return user_list

    def query_list(self):
        '''
        查询订单数据
        :param db: 
        :return: 
        '''
        sql = "SELECT top 10 m.Status,m.CustomerSysNo, item.ProductSysNo,item.Quantity FROM  IPP3.dbo.SO_Master m WITH ( NOLOCK ) " \
              "INNER JOIN IPP3.dbo.SO_CheckShipping c WITH(NOLOCK) ON c.SOSysNo=m.SysNo " \
              "LEFT JOIN IPP3.dbo.SO_Item item WITH(NOLOCK) ON item.SOSysNo = m.SysNo " \
              "LEFT JOIN IPP3.dbo.Product p  WITH(NOLOCK) ON p.SysNo=item.ProductSysNo " \
              "WHERE c.IsPhoneOrder NOT IN(5,15) AND item.ProductType <>3"

        order_list = self.msdb.execQuery(sql)
        return order_list

    def query_log_visit(self):
        '''
        查询用户浏览数据
        :param db: 
        :return: 
        '''
        sql = "SELECT MAX(plv.custom_var_v1),MAX(plv.user_id),MAX(plv.idsite),pla.`name`,COUNT(pla.idaction) FROM piwik_log_visit plv " \
              "LEFT JOIN piwik_log_link_visit_action pllva ON pllva.idvisit=plv.idvisit " \
              "LEFT JOIN piwik_log_action pla on pla.idaction=pllva.idaction_url_ref " \
              "where pllva.idsite IN (SELECT idsite FROM piwik_site WHERE idsite NOT IN (1)) " \
              "AND (plv.custom_var_v1 is not null or plv.user_id is not null ) AND plv.custom_var_v1 >0 " \
              "AND pla.name like '%/product/%' AND pla.`name` NOT LIKE '%pre%' AND pla.`name` NOT LIKE '%arrivenotice%' " \
              "AND pla.`name` NOT LIKE '%/searchinstore/%' AND pla.`name` NOT LIKE '%/searchresult?%' " \
              "GROUP BY pla.`name`  LIMIT 10"

        visit_log = self.mysqldb.execQuery(sql)
        return visit_log

    def writer_csv(self, path, data):
        ###判断文件是否存在
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            self.delete_dir(path)
        with open(path, "w", newline='') as csvfile:
            fieldnames = ['CustomerSysNo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for u in data:
                writer.writerow({"CustomerSysNo": u[0]})
        return path

    def delete_dir(self, dir):
        '''
        删除整个目录
        :param dir: 
        :return: 
        '''
        if os.path.isdir(dir):
            paths = os.listdir(dir)
            for path in paths:
                filePath = os.path.join(dir, path)
                if os.path.isfile(filePath):
                    try:
                        os.remove(filePath)
                    except os.error:
                        print("remove %s error." % filePath)  # 引入logging
                elif os.path.isdir(filePath):
                    if filePath[-4:].lower() == ".svn".lower():
                        continue
                    shutil.rmtree(filePath, True)
        return True


if __name__ == '__main__':
    da = order_da()
    # print(os.getcwd())
    order_list = da.query_list()

    list = [(102, 101, 1), (102, 102, 3), (102, 103, 2), (102, 104, 1), (102, 102, 5), (102, 101, 1)]
    new_list = [x for x in list if x[1] == 103]
    print(new_list)


    # user_list = da.query_user()

    # for d in order_list :
    #     print(d.any("20028187"))

    # da = order_da()
    # # 用户列表
    # user_list = da.query_user()
    # path = "D:/Learning/Matlab/data/customer/%s.csv" %(2015)
    # path=da.writer_csv(path)

    # 订单列表
    # order_list = da.query_list()
    #
    # for u in user_list:
    #     pass
    #
    # list = []
    # for order in order_list:
    #     if order.count('yang') > 0:
    #         list.append(order)
    #         # print(order)
    # print(list)

    # 生成insert语句
    # print(da.inser_sql(list))


    # visit_log = da.query_log_visit()
    #
    # for v in visit_log:
    #     print("用户编号：%s 商品编号：%s 浏览次数 %s" % (v[0], re.findall("\d+", v[3]), v[4]))
