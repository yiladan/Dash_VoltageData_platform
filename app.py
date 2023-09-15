import os
import json
from dash import Dash, dcc, html, Input, Output,State, callback
import dash
import dash_bootstrap_components as dbc
from func import *


app = Dash(__name__,title='后装数据分析', use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

# server = app.server

app.layout =  html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row([
            dbc.Col([ 
                html.H1('你好, 陌生人'),
                html.H3('Python web 框架')
            ], style={ 'textAlign':'left', 'margin-top':'-3rem'}),
            dbc.Col([
                html.Div([
                    html.Div(
                        dcc.Link(
                            f"{page['name']} - {page['path']}", href=page["relative_path"]
                                )
                            )
                            for page in dash.page_registry.values()
                        ], 
                            # style={ 'display': 'inline-block'}
                        )],
                    style={'textAlign':'center'}),
            dbc.Col([
                html.Img(id='img', alt='image',width='200px',height='200px')],
                style={'textAlign':'right','paddingRight':'-5rem','margin-top':'-6rem'}
            )
            ]),
        html.Br(),
        dbc.Col([
                html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    '上传csv或excel '
                                ]),
                                style={
                                    # 'width': '80%',
                                    'height': '80px',
                                    'lineHeight': '85px',
                                    'borderWidth': '1.5px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '20px',
                                    'textAlign': 'center',
                                    'margin': '5px',
                                    
                                },
                                # Allow multiple files to be uploaded
                                multiple=False
                            ),
                            # html.Br(),
                            html.H6('上传文件时间范围选框：'),
                            dcc.DatePickerRange(
                                    id='date-picker-range',
                                    clearable = True,
                            ),
                        ])],
                    ),
        
]),
    dcc.Store(id='df_store'),
    dcc.Store(id='file_name'),
    # html.Br(),
    html.Br(),
    html.Div(id='name-date', style={ 'display': 'inline-block'}),
    html.Div(id='motto', style={
                                'display': 'inline-block',
                                'color':'rgb(30,154,176)',
                                'textAlign': 'center',
                                'margin-left':'60px'}),
    html.Hr(),
    dash.page_container
])




# 上传文件读取
@callback(
          Output('df_store','data'),
          Output('name-date', 'children'),
          Output('file_name','data'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'),
          prevent_initial_call=True
          )
def update_output(content, filename, date):
    # if content is not None:
    df = parse_contents(content, filename, date)
    # print(type(df))#this will show data type as a pandas dataframe
    # print(datetime.datetime.fromtimestamp(date))
    return df.to_json(date_format='iso', orient='split'), str('当前文件为：{}').format(filename),json.dumps(filename)


@callback(
    Output('date-picker-range', 'start_date'),
    Output('date-picker-range', 'end_date'),
    Input('name-date', 'children'),
    State('df_store','data'),
    prevent_initial_call=True
)
def start_end_time(children, df_json):
    df = pd.read_json(df_json, orient='split')
    if children is not None:
        start_date = df[df.columns[0]].iloc[0]
        end_date = df[df.columns[0]].iloc[-1]
    return start_date, end_date


# 添加随机motto
@callback(
    Output('motto', 'children'),
    Input('name-date', 'children'),
    prevent_initial_call=True
)
def motto(content):
    with open('motto.txt', 'r',encoding = "utf-8") as f:   
        lines = f.readlines()       
    return lines[np.random.randint(0,len(lines))].split('、',1)[1].replace('\t','').replace('\n','')

# 添加动图
@callback(
    Output('img','src'),
    Input('url', 'pathname'),                                 # 由路径作为input，触发回调
)
def show_pic(pathname):
    file_list = os.listdir('./assets')
    pic_list = [i for i in file_list if i[-3:] != 'css']
    return app.get_asset_url(pic_list[np.random.randint(0,len(pic_list))])

if __name__ == '__main__':
    app.run(port=999,debug=True)
