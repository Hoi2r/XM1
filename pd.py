import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar,Map,Funnel,Line,Tab
sf1 = pd.read_csv("results.csv")

def map():
    # 工作地点分布地图：
    d = []
    sf1['work_place'] = sf1['work_place'].str[0:2]
    a = sf1['work_place'].value_counts()
    b = a.index.tolist()
    c = a.values.tolist()
    for j,k in zip(b,c):
        d.append([j,k])
    c = (
        Map(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add("数量",[list(sf) for sf in d], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="统计所有招聘信息工作地点的分布",subtitle="仅显示全国地图分布"),
            visualmap_opts=opts.VisualMapOpts(max_=20),
        )
    )
    return c
def bar():
    # 岗位受关注排行柱状图：
    sf1["viewed"] = sf1["viewed"].str[8:-1:].astype("int")
    sf1.sort_values(by="viewed",ascending=False,inplace=True)
    a = sf1.loc[sf1['viewed']>20000,:]
    b = a["job_name"].head(30).values.tolist()
    d = a["viewed"].head(30).values.tolist()

    c = (
        Bar(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add_xaxis(b)
        .add_yaxis("浏览次数",d)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="岗位受关注排行", subtitle="统计近期各岗位岗位受关注排行，仅统计浏览次数大于20000的前30条"),
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)),
        )
    )
    return c
def funnel():
    # 学历要求统计分布漏斗图
    data = sf1["edu_req"].value_counts()
    list1 = data.values.tolist()
    list2 = data.index.tolist()
    d = list2.index("不限")
    list1.pop(d)
    list2.remove("不限")
    data = [[list2[i], list1[i]] for i in range(len(list2))]
    c = (
        Funnel(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add(
            series_name="学历要求/岗位数",
            data_pair=data,
            gap=4,
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="学历要求排行", subtitle="统计近期各岗位的学历要求"))
    )
    return c
def line():
    # 工作经验招聘需求折线图
    data = sf1["work_exp"].value_counts()
    data.sort_values(ascending=False, inplace=True)
    data = data.head(8)
    x2 = data.index.tolist()
    y2 = data.values.tolist()

    c = (
        Line(init_opts=opts.InitOpts(width="1200px", height="600px"))
            .add_xaxis(x2)
            .add_yaxis("招聘需求", y2, is_connect_nones=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="工作经验招聘需求排行",subtitle="统计近期各岗位的工作经验要求，仅显示排名前部分"))
    )
    return c


tab = Tab()
tab.add(bar(), "岗位受关注排行柱状图")
tab.add(line(), "工作经验招聘需求折线图")
tab.add(funnel(), "学历要求统计分布漏斗图")
tab.add(map(), "工作地点分布地图")
tab.render("数据展示.html")
