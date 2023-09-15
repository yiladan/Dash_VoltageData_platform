import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from dash import html
import base64
import io


# 定义函数，选出离群点
def find_out(df):
    # 最大值最小值极差选出值df1
    index1 = df.iloc[:,1:-5].max(axis=1).sort_values(ascending=False).index
    index2 = df.iloc[:,1:-5].min(axis=1).sort_values(ascending=True).index

    df1=pd.DataFrame(None, columns=df.columns[1:-5], index=range(3))
    df1.iloc[0] = df.loc[index1[0], df1.columns]
    df1.iloc[1] = df.loc[index2[0], df1.columns]
    df1.loc[2] = df1.loc[0]-df1.loc[1]
    # 方差变化选出df_var
    df_gra = pd.DataFrame(None, columns=df1.columns)
    for i in df_gra.columns:
        df_gra[i] = np.gradient(df[i])
    df_var = df_gra.var()
    df_var = df_var.sort_values(ascending= False)

    df_range = pd.concat([df1.T, df_var], axis=1)
    df_range.columns = ['max', 'min', 'range', 'var']

    # DBSCAN聚类操作
    A = df_range['var'].values
    B = df_range['range'].values
    C = np.vstack((A, B))
    dbModel = DBSCAN(eps = 0.05, min_samples = 3).fit(C.T)
    labels = dbModel.labels_ 
    df_range['labels'] = labels

    return df_range, index1[0], index2[0]



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    #global df      # define data frame as global
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
            df.sort_values([df.columns[0]], inplace=True, ignore_index=True)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
            df.sort_values([df.columns[0]], inplace=True, ignore_index=True)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    df['Max']=df[df.columns[1:]].max(axis=1)
    df['Min']=df[df.columns[1:-1]].min(axis=1)
    df['Mean']=df[df.columns[1:-2]].mean(axis=1)
    df['argMax']=df.columns[1:-3][np.argmax(df[df.columns[1:-3]], axis=1)]
    df['argMin']=df.columns[1:-4][np.argmin(df[df.columns[1:-4]], axis=1)]
    return df


def db_data_process(df):
    df.drop(['index'], axis=1, inplace=True)
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
    df.sort_values([df.columns[0]], inplace=True, ignore_index=True)

    return df