from scrapy import Spider
from scrapy import Request
from xm1.items import Xm1Item
import time
class Pc1Spider(Spider):
    name = 'pc1'
    pagen = 0
    start_urls = ['http://www.gzrc.com.cn/SearchResult.php?page=0&sums=&&parentName=&key=&region_1=&region_2=&region_3=&keytypes=&jtzw=&data=&dqdh_gzdd=&jobtypes=&edus=&titleAction=&provinceName=&sexs=&postidstr=&postname=&searchzwtrade=&gznum=&salary=&showtype=list&sorttype=score&tradeid=1000&totalid=0#searching']

    def parse(self, response):
        list = response.xpath("//tr[@style='color:#a9a9a9']/following-sibling::tr[position()<=40]")
        for one in list:
            date = one.xpath("td[1]/text()").extract_first()
            job_name = one.xpath("td[2]/a/@title").extract_first()
            company_name = one.xpath("td[3]/a/@title").extract_first()
            work_place = one.xpath("td[4]/text()").extract_first()

            item = Xm1Item()
            item['date'] = date
            item['job_name'] = job_name
            item['company_name'] = company_name
            item['work_place'] = work_place

            url = one.xpath("td[2]/a/@href").extract_first()
            url1 = "http://www.gzrc.com.cn" + url
            yield Request(url1,meta={"item":item},callback=self.parsexx)
    def parsexx(self,response): #爬详细页 + 多页
        item = response.meta['item']
        item['viewed'] = response.xpath("//span[@class='fr']/text()").extract()
        item['edu_req'] = response.xpath("//*[@class='top-content fl']/p[2]/text()").extract()
        item['work_exp'] = response.xpath("//*[@class='top-content fl']/p[3]/text()").extract()
        item['hiring'] = response.xpath("//*[@class='top-content fl']/p[5]/text()").extract()
        item['wages'] = response.xpath("normalize-space(//*[@class='top-content fl']/p[4]/text())").extract()
        yield item
        # time.sleep(2)
        self.pagen += 1
        if self.pagen < 90:
            next_url = "http://www.gzrc.com.cn/SearchResult.php?page={}&sums=&&parentName=&key=&region_1=&region_2=&region_3=&keytypes=&jtzw=&data=&dqdh_gzdd=&jobtypes=&edus=&titleAction=&provinceName=&sexs=&postidstr=&postname=&searchzwtrade=&gznum=&salary=&showtype=list&sorttype=score&tradeid=1000&totalid=0#searching".format(
                self.pagen)
            yield Request(next_url, callback=self.parse)