import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import PeoplesItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class PeoplesSpider(scrapy.Spider):
	name = 'peoples'
	start_urls = ['https://www.peoples.com/press']

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn btn-primary  pubui-button pubui-btn-clear dtm-custom-linktracking pubui-btn-icon      "]/@href').getall() + response.xpath('//div[@class="richtexteditor"]//a/@href[not (ancestor::span[@class="pubui-rte-dark-color"])]').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="pubui-rte-base"]/text() | //span[@class="pubui-rte-light-color"]/text()').get().strip('Posted ')
		title = response.xpath('//span[@class="pubui-rte-h2"]//text()').get()
		content = response.xpath('(//div[@class="richtexteditor util-comp-padding-sm util-comp-margin util-comp-margin-bottom util-fix-content-width-desktop"])[2]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=PeoplesItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
