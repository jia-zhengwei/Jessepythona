# -*- coding utf-8 -*-

import numpy as np
import pandas as pd
import os
import re
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

  
def read_order(path):
    # ./data_sql/orderdata/
    files = os.listdir(path)
    frames = []
    for f in files:
        name = path + f
        df = pd.read_csv(name, encoding="utf-8")
        frames.append(df)
    # 数据合并
    result = pd.concat(frames)
    return result


def read_visit(path):
    # ./data_sql/orderdata/
    files = os.listdir(path)
    frames = []
    for f in files:
        name = path + f
        df = pd.read_csv(name, encoding="utf-8")
        frames.append(df)
    # 数据合并
    result = pd.concat(frames)
    return result


def dfunc(url):
    return re.findall("\d+", url)


if __name__ == '__main__':

    # 订单数据
    dfp = read_order("./data_sql/orderdata/")
    # 浏览数据
    dfv = read_visit("./data_sql/visitdata/")
    #查找某个用户的数据 分组求和
    #as_index 不加列名会合并
    user_data = dfp[(dfp.customerSysNo == 664196)].groupby(
        ["productSysNo", "status"], as_index=False).sum()
    user_visit = dfv[(dfv.customerSysNo == 664196)].groupby(
        "url", as_index=False).count()
    print(user_data)
    print(user_visit)

    product_rating = []
    # 商品的订单数据
    buy_count = 0.0
    for (productSysNo, status, customerSysNo, qty) in user_data.itertuples(
            index=False):
        if status == -1 or status == -4 or status == 6 or status == 65:
            buy_count = float(qty) * 0.30
        else:
            buy_count = float(qty) * 0.50
        product_rating.append((productSysNo, buy_count))

    # 商品的浏览的数据
    view_count = 0.00
    reg = r"[0-9]+(?=[^0-9]*$)"
    for (url, customerSysNo, userId, qty) in user_visit.itertuples(
            index=False):
        r_str = re.findall(reg, url, re.I)
        r_productsysNo = 0
        if len(r_str) > 0:
            r_productsysNo = int(r_str[0])
            if r_productsysNo > 0:
                view_count = float(qty) * 0.01
                product_rating.append((r_productsysNo, view_count))
        else:
            continue

    print(product_rating)
