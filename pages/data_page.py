import pandas as pd
import dash
from dash import dcc, html, Input, Output,State, callback
import plotly.express as px
import json
from db import con
from func import db_data_process, find_out

co = con(db_name = '后装数据库')           # 连接''数据库

dash.register_page(__name__)

layout = html.Div([
    
    html.H1('数据库管理'),
    dcc.Input(
            id='new_table_name',
            placeholder='输入要保存的名称',
            type='text',
            ),
    html.Button('刷新显示数据库列表',id='show', n_clicks=0),
    html.Button('上传数据到数据库',id='submit', n_clicks=0),
    
    # dcc.Store(id='table_name_store'),
    # html.Div(id='test_name_update'),
    dcc.Dropdown(id='table-select',style={ 'color': 'black'}),
    dcc.ConfirmDialogProvider(
        children=html.Button('删除所选数据',),
        id='drop',
        message='Danger danger! Are you sure you want to continue?'),
    html.Div(id='table_name'),
    html.Button('显示所选数据图像', id='show_select'),
    html.Div([
                    html.Label('数据库时间范围选框'),
                    dcc.DatePickerRange(
                            id='db-picker-range',
                            clearable = True,
                    ),
                ], style={ 'display': 'inline-block','float': 'right'}),
    html.Br(),
    dcc.Store(id='db_df_store'),
    html.Div([
        # html.H3('电压分析散点图'),
        html.Div(id='db_data_results', style={'float': 'left'}),
        html.Br(),
        html.Div([
            dcc.Graph(id='db_scatter-graph',className='hidden-graph'),
            ], style={'width': '49%', 'display': 'inline-block','margin-left':'-30px'}),
        html.Div([
            html.Div(id='db_hoverdata'),
            dcc.Graph(id='db_preview',className='hidden-graph')
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
        html.Br(),
        html.Div([
            html.H5(id = 'db_graph_title',
                    className='hidden-graph',
                    children='Comparison between Max and Min',
                    style={'width': '49%','display': 'inline-block','paddingButtom':'-5px'}),
            html.Div(id='db_show_time',style={'width': '49%','display': 'inline-block','text-align': 'right'})
        ]),  
        
        dcc.Graph(id='db_test_graph',className='hidden-graph'),
        # html.Div(id='test-hover1'),
        # html.Div(id='test-hover2'),
        dcc.Graph(id='db_scatter-graph2',className='hidden-graph'),
        dcc.Store(id='db_df_range_store')
    ])
])


# 数据库列表实时更新回调，打开数据
@callback(
        Output('table-select','options'),
        Input('name-date','children'),
        prevent_initial_call=True
)
def table_name_update(name):
    df_names = co.show_table_name()
    # table_name = name.split('：',1).replace('.','_').replace('-','_')
    return [o for o in df_names]

# 数据库列表实时更新回调，上传数据
@callback(
        Output('table-select','options',allow_duplicate=True),
        Input('submit','n_clicks'),
        prevent_initial_call=True
)
def table_name_update(clicks):
    df_names = co.show_table_name()
    return [o for o in df_names]

# 数据库列表实时更新回调，删除数据
@callback(
        Output('table-select','options',allow_duplicate=True),
        Input('drop','submit_n_clicks'),
        prevent_initial_call=True
)
def table_name_update(clicks):
    df_names = co.show_table_name()
    return [o for o in df_names]


# 上传表格数据回调
@callback(
    Output('table_name','children'),
    Input('submit','n_clicks'),
    State('new_table_name', 'value'),
    State('df_store','data'),
    State('file_name','data'),
    prevent_initial_call=True
)
def submit_click(click,new_table_name,df_json,df_name_json):
    if new_table_name == None:
        df = pd.read_json(df_json, orient='split')
        df_name = json.loads(df_name_json).replace('.','_').replace('-','_').replace('——','').replace(' ','')
        co.submit_data(df, newtable=df_name)
        return df_name+'上传成功'
    else:
        df = pd.read_json(df_json, orient='split')
        co.submit_data(df, newtable=new_table_name)
        return new_table_name+'上传成功'


# 显示表格名称
@callback(
    Output('table_name','children', allow_duplicate=True),
    Output('table-select','options',allow_duplicate=True),
    Input('show','n_clicks'),
    prevent_initial_call=True
)
def show_tables(click):
    df_names = co.show_table_name()
    df_names.to_list()
    return '请选择数据表', [o for o in df_names]


# 删除列表
@callback(
    Output('table_name','children', allow_duplicate=True),
    Input('drop','submit_n_clicks'),
    State('table-select','value'),
    prevent_initial_call=True
)
def drop_table(submit_n_clicks, select_table):
    if not submit_n_clicks:
        return select_table+'未删除'
    else:
        co.drop_table(select_table)
        return select_table+'删除成功'
    


@callback(
    Output('db_df_store','data'),
    Output('db-picker-range', 'start_date'),
    Output('db-picker-range', 'end_date'),
    Output('table_name','children', allow_duplicate=True),
    # Input('show_select','n_clicks'),
    Input('table-select', 'value'),
    prevent_initial_call=True
)
def start_end_time_db(table_name):
    df_select = co.read_data('{}'.format(table_name))
    df_select = db_data_process(df_select)
    start_date = df_select[df_select.columns[0]].iloc[0]
    end_date = df_select[df_select.columns[0]].iloc[-1]
    return df_select.to_json(date_format='iso', orient='split'),start_date,end_date,table_name+'读取成功'



# 显示选中图像
# 时间选框回调
# 筛选数据处理回调
@callback(
    Output('db_df_range_store','data'),
    Output('db_test_graph', 'figure'),
    Output('db_scatter-graph', 'figure'),
    Output('db_test_graph', 'className'),
    Output('db_scatter-graph', 'className'),
    Output('db_graph_title', 'className'),
    Output('db_show_time', 'children'),
    Output('db_data_results','children'),
    State('db-picker-range', 'start_date'),
    State('db-picker-range', 'end_date'),
    State('db_df_store','data'),
    Input('show_select', 'n_clicks'),
    prevent_initial_call=True
)
def scatter_graph(start_date, end_date, df_json,n_clicks):
    if n_clicks!=0:
        df = pd.read_json(df_json, orient='split')
        df_filter = df[(df[df.columns[0]] > start_date) & (df[df.columns[0]] < end_date)]
        df_range, time_max, time_min = find_out(df_filter)

        df_stray = df_range[df_range['labels']!=0].index.values

        fig_test = px.line(df_range,
                            x=df_range.index,
                            y=['max','min','range']
                            )
        # fig.update_traces(marker={'size':'10'})
        fig_test.update_layout(
                                paper_bgcolor = '#1f2c56',
                                # plot_bgcolor = '#1f2c56',
                                font=dict(family='sans-serif',
                                color='white',
                                size=15),
                                margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
                                hovermode='closest')

        fig_scatter = px.scatter(df_range,
                                x= 'var',
                                y='range',
                                color='labels',
                                hover_name=df_range.index,
                                color_continuous_scale=px.colors.sequential.Bluered
        )
        fig_scatter.update_layout(
                                title={'text':'Scatter_graph_Analysis',
                                        'y':0.95,
                                        'x':0.5,
                                       'xanchor': 'center',
                                        'yanchor': 'top'},
                                paper_bgcolor = '#1f2c56',
                                # plot_bgcolor = '#1f2c56',
                                font=dict(family='sans-serif',
                                color='white',
                                size=15),
        )
        return df_range.to_json(date_format='iso', orient='split'),  fig_test, fig_scatter,\
            'visible-graph', 'visible-graph', 'visible-graph',\
            'max_time:{},  min_time:{}'.format(df[df.columns[0]][time_max], df[df.columns[0]][time_min]), \
            '聚类挑出异常电芯：{}'.format(df_stray)



# 增加hover的callback
@callback(
    Output('db_preview', 'figure'),
    Output('db_preview', 'className'),
    Input('db_scatter-graph', 'hoverData'),
    State('db_df_store','data'),
    State('db-picker-range', 'start_date'),
    State('db-picker-range', 'end_date'),
    prevent_initial_call=True
)
def hover_scatter(hoverData,df_json,start_date,end_date):
    # return json.dumps(hoverData['points'][0]['hovertext'])   通过调用查看hoverdata内容
    df = pd.read_json(df_json, orient='split')
    df_filter = df[(df[df.columns[0]] > start_date) & (df[df.columns[0]] < end_date)]
    fig = px.scatter(df_filter,
                     x=df_filter.columns[0],
                     y=['Max', 'Min', 'Mean',hoverData['points'][0]['hovertext']],            # y=[hoverData,'Max', 'Min', 'Mean']
                     hover_data=['argMax', 'argMin']
    )
    # fig = px.scatter(df,
    #                  x=df.columns[0],
    #                  y=[hoverData['points'][0]['hovertext']])
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
                    title={'text':'Voltage_data_Overview',
                                        'y':0.95,
                                        'x':0.5,
                                       'xanchor': 'center',
                                        'yanchor': 'top'},
                    paper_bgcolor = '#1f2c56',
                    # plot_bgcolor = '#1f2c56',
                    font=dict(family='sans-serif',
                    color='white',
                    size=15),)
    # fig.update_layout(
    #     margin={"l": 20, "r": 0, "b": 15, "t": 5},
    #     dragmode="select",
    #     hovermode=False,
    #     newselection_mode="gradual",
    # )
    return fig, 'visible-graph'


# 增加test-graph对scatter的hover  callback
@callback(
    Output('db_scatter-graph2', 'figure'),
    Output('db_scatter-graph2', 'className'),
    # Output('test-hover2', 'children'),
    State('db_df_range_store','data'),
    Input('db_test_graph', 'hoverData'),
    # State('date-picker-range', 'start_date'),
    # State('date-picker-range', 'end_date'),
    prevent_initial_call=True
)
def test_graph2scatter_graph(df_range_json,hoverData):
    df_range = pd.read_json(df_range_json, orient='split')
    fig = px.scatter(df_range,
                            x= 'var',
                            y='range',
                            color='labels',
                            hover_name=df_range.index,
                            color_continuous_scale=px.colors.sequential.Bluered
    )             
    fig.update_traces(mode="markers",
                      selectedpoints=[hoverData['points'][0]['pointIndex']],
                      selected={"marker": {"color": "black"}},
                      unselected={"marker": {"opacity": 0.3}}
    )
    fig.update_layout(
                    paper_bgcolor = '#1f2c56',
                    # plot_bgcolor = '#1f2c56',
                    font=dict(family='sans-serif',
                    color='white',
                    size=15),
                    margin={"l": 20, "r": 0, "b": 15, "t": 5},
                    dragmode="select",
                    newselection_mode="gradual",
    )
    return fig, 'visible-graph'
    

