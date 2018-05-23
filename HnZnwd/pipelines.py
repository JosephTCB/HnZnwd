# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class HnznwdPipeline(object):
	def process_item(self, item, spider):
		return item

	def __init__(self):
		self.f = open("hnznwd.json", "w+",encoding='utf-8')

		  # 所有的item使用共同的管道
	def process_item(self, item, spider):
		content = json.dumps(dict(item), ensure_ascii = False) + ",\n"
		self.f.write(content)
		return item

	def close_spider(self, spider):
		self.f.close()
		f = open('hnznwd.json', 'r', encoding='utf-8')
		result = ""
		for line in open('hnznwd.json', encoding='utf-8'):
			line = f.readline()
			result = result + line
		f.close()
		result = result[:-2]
		result = "[" + result + "]"
		load_dict = json.loads(result)
		qalist = self.MergeHost(load_dict)
		file = open('hnznwd.txt', 'w', encoding='utf-8')
		for q_a in qalist:
			content = json.dumps(q_a, ensure_ascii=False) + ',\n'
			file.write(content)
		file.close()

	def MergeHost(self, resource_list):
		allResource = []
		allResource.append(resource_list[0])
		for dict in resource_list:
			k = 0
			for item in allResource:
				if dict['q'] != item['q']:
					k = k + 1
				else:
					break
				if k == len(allResource):
					allResource.append(dict)
		return allResource
