# coding: utf-8
from scrapy import Spider
import json, time
from scrapy.http import FormRequest
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
from HnZnwd.items import HnznwdItem

class HnQaSpider(Spider):
	name = 'qa'
	allowed_domains = ['218.28.41.134']
	start_urls = ['http://218.28.41.134//hnww/BsfzBLH_Zdwd.do']
	url = 'http://218.28.41.134//hnww/BsfzBLH_getAnswerByCode.do#'
	def parse(self, response):
		url = 'http://218.28.41.134//hnww/BsfzBLH_Zdwd.do'
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.get(url)
		i = 0
		while True:
			problemlist = BeautifulSoup(driver.page_source, 'lxml').select('ul#ul3')[0].select('li')
			for problem in problemlist:
				zlcode = problem.a['zlcode']
				yield FormRequest(self.url, formdata={'zlcode': zlcode}, meta={"question": problem.a['title']},
								  callback=self.find_parse)
			for j in range(20):
				try:
					driver.find_elements_by_xpath('//a[@class="next"][contains(text(),"下一页")]')[0].click()
					time.sleep(0.5)
					break
				except:
					print('重新下一页...')
					time.sleep(2)
			if i > 1:
				soup = BeautifulSoup(driver.page_source, 'lxml')
				page = soup.select('span#paginationXgwt')[0]
				if int(page['currpage']) == int(page['totalpage']):
				#if int(page['currpage']) == 5:
					problemlist = BeautifulSoup(driver.page_source, 'lxml').select('ul#ul3')[0].select('li')
					for problem in problemlist:
						zlcode = problem.a['zlcode']
						yield FormRequest(self.url, formdata={'zlcode': zlcode}, meta={"question": problem.a['title']},
										  callback=self.find_parse)
					break
			i = i + 1

	def find_parse(self, response):
		zlnr = json.loads(response.body.decode('utf-8'))['zlnr']
		sel = etree.HTML(zlnr)
		answer = sel.xpath('string(.)').strip().replace('\n','').replace('\r','').replace('　','').replace(' ','')
		question = response.meta['question']
		item = HnznwdItem()
		item['q'] = question
		item['a'] = answer
		yield item