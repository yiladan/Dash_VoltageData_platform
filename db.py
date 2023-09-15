from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import pandas as pd
from dash import html 

# 连接mysql
# mysql_url = 'mysql+pymysql://root:bmser888@127.0.0.1/Dash?charset=utf8'
# engine = create_engine(mysql_url) 
# # con=pymysql.connect(host='localhost',password='bmser888',port=3306,user='root',charset='utf8')
# connection = engine.connect()
# df = pd.read_csv(r'C:\Users\hanjiangtao\Documents\Dash\鲁·B15758D 放电电压高于充电.csv')
# df.to_sql(con=connection, name='test', schema='Dash', index=False, if_exists='replace')

class con:
    def __init__(self, db_name):
        self.mysql_url = 'mysql+pymysql://root:bmser888@127.0.0.1/{}?charset=utf8'.format(db_name)
        self.engine = create_engine(self.mysql_url) 
    
    def read_data(self, table):
        res= pd.read_sql('select * from {}'.format(table), self.engine)
        return res
    
    def drop_table(self, table):
        sql = 'DROP TABLE IF EXISTS %s'%table
        session = sessionmaker(self.engine)
        Session = session()
        Session.execute(text(sql))
        Session.commit()
        Session.close()
    
    def submit_data(self,df,newtable):
        df.to_sql(newtable, self.engine, if_exists='fail')

    def show_table_name(self):
        df_name = pd.read_sql('show tables', self.engine)
        return df_name.iloc[:,0]
    
    def generate_table(self, df, max_rows=10):
        """产生表格"""
        return html.Table([
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody([html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))])
        ])

# conn = con()
# print(conn.show_table_name().values)
# conn.submit_data(df,'test1')
# conn.drop_table('t')
# print(type(conn.read_data('鄂c15537d')))