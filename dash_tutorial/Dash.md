# Dash—交互式数据可视化搭建
依靠着薄弱的python基础，希望搭建一个能够应用的数据分析工具，而不是需要安装python、配置环境的脚本文件🧑‍💻。碰巧的是，在网上看plotly画图的时候，找到了一个有趣的数据可视化web；依附于Flask的轻量级web框架，结合plotly数据可视化的功能，Dash就出来了😎

## Dash简介🚩
Dash是一个用于构建Web应用程序的高效Python框架。

Dash写在Flask，Plotly.js和React.js之上，非常适合在纯Python中，使用高度自定义的用户界面，构建数据可视化应用程序。它特别适合使用Python进行数据分析的人。

通过几个简单的模式，Dash抽象出构建基于Web的交互式应用程序所需的所有技术和协议。

Dash应用程序在Web浏览器中呈现，可以将应用程序部署到服务器，然后通过URL进行共享。

由于Dash应用程序是在Web浏览器中进行查看，因此Dash本质上是跨平台和移动端的。

Dash是一个开源库，在许可的MIT下发布，Plotly开发Dash，并提供了一个在企业环境中轻松部署Dash应用程序的平台。

🏳️‍🌈Dash官网：[Dash Documentation & User Guide | Plotly](https://dash.plotly.com/)
😌Dash主题框架 Dash Bootstrap Components官网：
http://dash-bootstrap-components.opensource.faculty.ai/

## Dash体系架构 
***
###  😋Flask和React
Dash应用程序是运行[Flask](https://links.jianshu.com/go?to=http%3A%2F%2Fflask.pocoo.org%2F)，并通过HTTP请求传递JSON数据包的Web服务器。Dash的前端使用React.js渲染组件，React.js是由Facebook编写和维护的Javascript用户界面库。

Flask很棒，已被Python社区广泛采用，并部署于众多生产环境中。Dash应用的开发者可以设置Flask的底层实例和属性，高级开发者还可以使用众多的Flask插件扩展Dash应用。

React也很赞，在Plotly，我们用React重写了全部Web平台和在线视图编辑器。React最了不起的一点是它的社区作品众多且个个优秀。React的开源社区已经公布了数以千计的高质量交互式组件，包括下拉菜单、滑块、日历，还有交互式表格等。

Dash整合了Flask与React的强大功能，使非专业Web开发的Python数据分析师也可以使用。
***
### 从React.js到Python Dash组件
Dash组件是一个编译React组件属性与值，并将之生成JSON序列的Python类。

Dash提供了一个[工具集](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fplotly%2Fdash-components-archetype)，可以轻松地将React组件 (Javascript编写) ，打包为可在Dash中使用的组件。此工具集使用动态编程，自动将注释过的React PropType转化为标准的Python类。生成后的Dash组件Python类对用户很友好，能进行自动参数验证，并生成字符串。[编写组件](https://dash.plotly.com/plugins)
```python
    >>> help(dcc.Dropdown)
    class Dropdown(dash.development.base_component.Component)
     |  A Dropdown component.
     |  Dropdown is an interactive dropdown element for selecting one or more
     |  items.
     |  The values and labels of the dropdown items are specified in the `options`
     |  property and the selected item(s) are specified with the `value` property.
     |
     |  Use a dropdown when you have many options (more than 5) or when you are
     |  constrained for space. Otherwise, you can use RadioItems or a Checklist,
     |  which have the benefit of showing the users all of the items at once.
     |
     |  Keyword arguments:
     |  - id (string; optional)
     |  - className (string; optional)
     |  - disabled (boolean; optional): If true, the option is disabled
     |  - multi (boolean; optional): If true, the user can select multiple values
     |  - options (list; optional)
     |  - placeholder (string; optional): The grey, default text shown when no option is selected
     |  - value (string | list; optional): The value of the input. If `multi` is false (the default)
     |  then value is just a string that corresponds to the values
     |  provided in the `options` property. If `multi` is true, then
     |  multiple values can be selected at once, and `value` is an
     |  array of items with values corresponding to those in the
     |  `options` prop.
     |
     |  Available events: 'change
```
***
### 并发-多用户使用
Dash应用程序的状态存储在前端(即Web浏览器)中，这允许多个用户可以使用独立的会话，同时与Dash应用程序进行交互操作。

这个也是实际应用中最方便的了，不用考虑多个用户同时使用的情况🤞

###  CSS和默认样式
核心库没有包含CSS与默认样式，这样做是为了支持模块化和独立版本控制，鼓励Dash应用的开发者，自定义其应用程序的界面外观。点此查阅由Dash核心团队维护的[核心样式指南](https://links.jianshu.com/go?to=https%3A%2F%2Fcodepen.io%2Fchriddyp%2Fpen%2FbWLwgP)。

###  数据可视化
Dash的图形组件使用plotly.js对图形进行渲染，Plotly.js与Dash配合默契，它使用声明式编程模式，开源且速度快，还支持科技计算、金融、商务类的各种视图。Plotly.js基于D3.js构建，支持导出符合出版标准的高清矢量图与优先性能的WebGL视图。

Dash的图形元素与开源的plotly.py库共享同样的语法，开发者可以轻易地在两者之间切换。Dash的图形组件从plotly.js事件系统中关联信息，允许开发者编写响应在Plotly图形中**悬停、点击、选点**等操作的应用。

![aef77db0b3429094dcef5de746bfaf0f.png](aef77db0b3429094dcef5de746bfaf0f.png)

## Dash安装
***
新建虚拟环境并激活：
```
python -m venv venv
.\venv\Scripts\activate
```
conda创建新环境：
```
conda create -n dash python=3.9.11
```
***
安装dash：
```
pip install dash -i https://mirror.baidu.com/pypi/simple
```
安装dash-bootstrap-components：
```
pip install dash-bootstrap-components -i https://mirror.baidu.com/pypi/simple
```
***

## Dash部署
在Linux系统中，dash应用可以使用gunicorn进行部署：
[Gunicorn](https://link.zhihu.com/?target=http%3A//gunicorn.org/) (独角兽)是一个高效的Python WSGI Server,通常用它来运行 wsgi application(由我们自己编写遵循WSGI application的编写规范) 或者 wsgi framework(如Django,Paster),地位相当于Java中的Tomcat。

安装gunicorn
```
pip install -i https://mirrors.aliyun.com/pypi/simple gunicorn
```
切换到文件目录，运行命令
```
gunicorn -w 4 -b 0.0.0.0:5000 app:server
```
        -w是worker 进程数；
        -b是地址和端口；
        app是文件名；
        server是创建的实例；
后台运行命令：
```
nohup gunicorn -w 4 -b 0.0.0.0:5000 app:server &
```
***
由于本人二手服务器性能堪忧，导致部署后还没有本机测试时流畅，后续尝试使用一下docker部署
***
[nginx gunicorn部署](https://zhuanlan.zhihu.com/p/141626596)
![fa7bec162de6f6ee975d775c0b8c1884.png](fa7bec162de6f6ee975d775c0b8c1884.png "fa7bec162de6f6ee975d775c0b8c1884.png")



 















 
