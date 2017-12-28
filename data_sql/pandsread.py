import pandas as pd
import numpy as np


def np_read():
    """
    numpy 读取文件
    形成矩阵
    """
    # fname：读取文件的文件名。例如C:/Dataset/iris.txt。
    # delimiter：数据之间的分隔符。如使用逗号","。
    # dtype：数据类型。如float，str等。
    # usecols：选取数据的列。 usecols=(0,1,2,3)
    # skiprows 读取时候跳过多少行
    fname = open("./orderdata/2015.csv", "rb")
    # np_matrix = np.loadtxt(fname, delimiter=",",skiprows=1000, usecols=(0, 1, 2, 3))
    np_matrix = np.loadtxt(fname, delimiter=",",skiprows=1000, usecols=(0, 1, 2, 3),dtype=float).astype(str)
    print("type：", type(np_matrix))
    print(np_matrix[:5])
    print("shape：", np_matrix.shape)

def pd_read():
    """
    pandas读取csv文件 
    形成矩阵
    """
    # nrows:读取多少行，
    # usecols：想要读取的列
    # df=pd.read_csv("./orderdata/2015.csv",nrows=1000,usecols=(0,1,2,3))
    df = pd.read_csv("./orderdata/2016.csv")
    print("type：", type(df))
    val = df.values
    print("type：", type(val))
    print(val)
    print("shape：", val.shape)


if __name__ == '__main__':
    pd_read()
    np_read()
