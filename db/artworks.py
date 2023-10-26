import pymysql
import pandas as pd
from sqlalchemy import create_engine

#连接数据库
host = '192.168.1.198'
user = 'messiah'
password = 'messiah'
database = 'pixiv'
port = 3316
conn = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))

#从数据库中读取pid
def query(table, pid):

    # 检查数据是否已存在
    existing_data = pd.read_sql_query(f"SELECT * FROM {table} WHERE pid = {pid}", con=conn)
    return existing_data.empty


def insert(table, data, pid):
    # 创建一个包含要插入的数据的DataFrame
    df = pd.DataFrame(data)  # 'data' 应该是字典或字典列表

    # 检查数据是否已存在
    existing_data = pd.read_sql_query(f"SELECT * FROM {table} WHERE pid = {pid}", con=conn)

    if existing_data.empty:
        # 数据不存在，执行插入操作
        # 使用to_sql方法将数据插入到指定的表中,'append' 表示将新数据附加到已存在的表中。其他可能的选项包括 'fail'（如果表已经存在则不插入），'replace'（替换已存在的表），和 'truncate'（清空已存在的表再插入数据）
        df.to_sql(name=table, con=conn, if_exists='append', index=False)
    else:
        # 数据已存在，可以选择执行其他操作或不执行任何操作
        print("数据已存在，不执行插入操作：" + pid)

def insert_pid_no(table, data, pid, pid_no):

    # 创建一个包含要插入的数据的DataFrame
    df = pd.DataFrame(data)  # 'data' 应该是字典或字典列表

    # 检查数据是否已存在
    existing_data = pd.read_sql_query(f"SELECT * FROM {table} WHERE pid = {pid} and pid_no = {pid_no}", con=conn)

    if existing_data.empty:
        # 数据不存在，执行插入操作
        # 使用to_sql方法将数据插入到指定的表中,'append' 表示将新数据附加到已存在的表中。其他可能的选项包括 'fail'（如果表已经存在则不插入），'replace'（替换已存在的表），和 'truncate'（清空已存在的表再插入数据）
        df.to_sql(name=table, con=conn, if_exists='append', index=False)
    else:
        # 数据已存在，可以选择执行其他操作或不执行任何操作
        print("数据已存在，不执行插入操作：" + pid + "_" + pid_no)