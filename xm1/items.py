# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Xm1Item(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field() #日期
    job_name = scrapy.Field() #职位名称
    company_name = scrapy.Field() #公司名称
    work_place = scrapy.Field() #工作地点
    edu_req = scrapy.Field() #学历要求
    viewed = scrapy.Field() #浏览次数
    hiring = scrapy.Field() #招聘人数
    work_exp = scrapy.Field() #工作经验
    wages = scrapy.Field() #薪资待遇
    pass
