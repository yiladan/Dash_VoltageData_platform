import dash
from dash import html, dcc, Input, Output, State, callback

import plotly.express as px

from func import *


dash.register_page(__name__)

layout = html.Div([
    html.Div([
        html.Div([
            
            html.H3('Python web 图像可视化模块', )], style={'width': '30%','display': 'inline-block'}),
            
            ]),
        html.Br(),
        html.Button('显示图像结果',id='test',n_clicks=0),
        html.Br(),
        # html.H3('电压分析散点图'),
        html.Div(id='data_results', style={'float': 'left'}),
        html.Br(),
        html.Div([
            # html.H6('scatter_graph_analysis', style={'paddingBottom':'10px'}),
            dcc.Graph(id='scatter-graph',className='hidden-graph'),
            ], style={'width': '49%', 'display': 'inline-block','margin-left':'-30px'}),
        html.Div([
            html.Div(id='hoverdata'),
            dcc.Graph(id='preview',className='hidden-graph')
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
        html.Br(),
        html.Div([
            html.H5(id='graph_title',
                    children = 'Comparison between Max and Min',
                    className='hidden-graph',
                    style={'width': '49%','display': 'inline-block','paddingButtom':'-5px'}),
            html.Div(id='show_time',style={'width': '49%','display': 'inline-block','text-align': 'right'})
        ]),
        dcc.Graph(id='test_graph',className='hidden-graph'),
        # html.Div(id='test-hover1'),
        # html.Div(id='test-hover2'),
        dcc.Graph(id='scatter-graph2',className='hidden-graph'),
        dcc.Store(id='df_range_store')
])



# 时间选框回调
# 筛选数据处理回调
@callback(
    Output('df_range_store','data'),
    Output('test_graph', 'figure'),
    Output('scatter-graph', 'figure'),
    Output('test_graph', 'className'),
    Output('scatter-graph', 'className'),
    Output('graph_title','className'),
    Output('show_time', 'children'),
    Output('data_results','children'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
    State('df_store','data'),
    Input('test', 'n_clicks'),
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
                                # title={'text':'Comparison between Max and Min'},
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
            'visible-graph','visible-graph','visible-graph',\
            'max_time:{},  min_time:{}'.format(df[df.columns[0]][time_max], df[df.columns[0]][time_min]), \
            '聚类挑出异常电芯：{}'.format(df_stray)



# 增加hover的callback
@callback(
    Output('preview', 'figure'),
    Output('preview', 'className'),
    Input('scatter-graph', 'hoverData'),
    State('df_store','data'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
    prevent_initial_call=True
)
def hover_scatter(hoverData,df_json, start_date, end_date):
    # return json.dumps(hoverData['points'][0]['hovertext'])   通过调用查看hoverdata内容
    df = pd.read_json(df_json, orient='split')
    df_filter = df[(df[df.columns[0]] > start_date) & (df[df.columns[0]] < end_date)]
    fig = px.scatter(df_filter,
                     x=df_filter.columns[0],
                     y=['Max', 'Min', 'Mean',hoverData['points'][0]['hovertext']],            # y=[hoverData,'Max', 'Min', 'Mean']
                     hover_data=['argMax', 'argMin']
    )
    # fig.update_layout(
    #                 paper_bgcolor = '#1f2c56',
    #                 plot_bgcolor = '#1f2c56',
    # )
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
                    size=15),
    )
    # fig.update_layout(
    #     margin={"l": 20, "r": 0, "b": 15, "t": 5},
    #     dragmode="select",
    #     hovermode=False,
    #     newselection_mode="gradual",
    # )
    return fig, 'visible-graph'


# 增加test-graph对scatter的hover  callback
@callback(
    Output('scatter-graph2', 'figure'),
    Output('scatter-graph2','className'),
    # Output('test-hover2', 'children'),
    State('df_range_store','data'),
    Input('test_graph', 'hoverData'),
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


