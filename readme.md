- Scrapy抓取天气网中全国地区历史天气数据

- 首先新建Scrapy爬虫项目

  ```python
  scrapy startproject TianQi
  ```

- 需要抓取的数据：

  - 通过对页面的分析，需要抓取和保存的数据包括：地区名、日期、最高气温、最低气温、天气、风向、风力、抓取时间、抓取数据的url

  - 要保存items的字段

    --------items截图----

- 分析抓取的过程

  - 打开网站http://lishi.tianqi.com/
  - 点击具体的一个区域，进去该区域的详情页面
  - 页面上查看之后发现历史的天气数据还在下一级的页面中，点击进入
  - 最终我们看到了我们想要抓取的具体的数据
  - 因为要保存地区的信息，但是该地区的详细历史天气在最终的目录，我们可以通过meta传参将地区的信息传到最终要获取数据的页面

- 分析完毕，创建爬虫

  ```python
  scrapy genspider weather "http://lishi.tianqi.com/"
  ```

- 首先在http://lishi.tianqi.com/起始页我们需要获取到所有地区的列表和所有地区的链接，这里我们使用xpath。然后对地区列表和地区链接进行遍历，还有一点需要注意的就是，起始页的地区列表是根据A-Z字母排序的，前面有A-Z也是有链接的，我们在遍历的时候需要判断一下url是否是# 如果是，我们就continue，否则的话我们就创建新的请求并发送，在发送请求时将地区名通过meta传到下一级页面中。

  ```python
      def parse(self, response):

          # 获取所有地区的列表
          area_list = response.xpath("//div[@id='tool_site']/div[2]/ul/li/a/text()").extract()

          # 获取所有地区的链接
          url_list = response.xpath("//div[@id='tool_site']/div[2]/ul/li/a/@href").extract()

          # 遍历地区列表和url列表
          for area, url in zip(area_list, url_list):
              # 对url进行判断 看是否为 #
              print area,"------",url
              if url == '#':
                  continue

              # 创建请求并发送
              yield scrapy.Request(url, callback=self.parse_area, meta={'area_name': area})
  ```

- 上面在起始页提起出地区的url并发送请求，在parse_area方法中提取出我们想要的数据，通过观察，在地区的url详情页面我们需要提取的数据就是该地区每年每月天气数据的url，首先我们接受meta传来的地区名，然后获取到每一个月份的url列表，在对url列表进行遍历，发送请求，去得到每个月的具体的天气数据。

  ```python
      def parse_area(self, response):
          # 接收meta传来的地区名
          area = response.meta['area_name']
          # print area

          # 获取每一个月份url列表
          url_list = response.xpath("//*[@id='tool_site']/div[2]/ul/li/a/@href").extract()
          # 遍历url列表
          for url in url_list:
              # 创建请求并发送
              print url
              yield scrapy.Request(url, callback=self.parse_data, meta={'area_name': area})
  ```

