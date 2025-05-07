import sqlite3
import os

# 创建数据库目录（如果不存在）
os.makedirs('instance', exist_ok=True)

# 数据库文件路径
DB_PATH = 'instance/flimgsys.db'

# 连接到SQLite数据库（如果不存在则创建）
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 读取SQL脚本
with open('create_db.sql', 'r', encoding='utf-8') as sql_file:
    sql_script = sql_file.read()

# 执行SQL脚本
cursor.executescript(sql_script)

# 提交更改并关闭连接
conn.commit()
conn.close()

print(f"数据库已成功创建在 {os.path.abspath(DB_PATH)}")
print("添加了管理员账户：username=admin, password=admin123") 