from mssql import query
import csv
import time


def datatofile(orderList, filename):
    csvfile = open(filename + '.csv', 'w', newline='')  # , encoding='utf-8'  
    writer = csv.writer(csvfile)
    writer.writerow(['CustomerSysNo', 'Status', 'ProductSysNo', 'Quantity'])
    for order in orderList:
        # 写入csv  
        writer.writerow([order[0], order[1], order[2], order[3]])
    csvfile.close()


def main(year_list: list):

    q = query()
    for year in year_list:
        data = q.demo(year)
        name = "./orderdata/" + str(year)
        datatofile(data, name)

        print(str(year) + "年订单数据导出完成")


if __name__ == '__main__':
    s_time = time.time()
    year_list = [2015, 2016, 2017]
    main(year_list)
    print("time spent: ", time.time() - s_time)