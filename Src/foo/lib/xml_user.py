import xml.etree.ElementTree as ET
from lxml import etree

class GetXML:
	'提供读取XML文件和读取值得一些方法'
	def __init__(self):
		pass

	def Read(self,xmlfilename):
		'将XML文件解析为树,并且得到根节点'
		#tree = ET.ElementTree(file=xmlfilename)
		tree = etree.parse(xmlfilename)
		self.root = tree.getroot()
		return self.root

	def Iter(self):
		'递归迭代xml文件中所有节点（包含子节点，以及子节点的子节点）'
		return self.root.iter()

	def FindAll(self,tag):
		'查找节点为tag的所有直接子元素'
		#直接子元素的意思：只会查找当前节点的子节点那一级目录
		return self.root.findall(tag)

	def Find(self,tag):
		'查找第一个节点为tag的直接子元素'
		return self.root.find(tag)

	def ReadHtml(self,htmlfilename):
		'解析html文件，返回一个支持xPath语法解析html的对象'
		#创建自定义解析器
		parser = etree.HTMLParser(encoding='GBK')
		#解析html文件,返回一个<class 'lxml.etree._ElementTree'>对象
		htmlelement = etree.parse(htmlfilename, parser = parser)
		#返回一个一个字符串，包含html中的所有内容
		html = etree.tostring(htmlelement, encoding='utf-8').decode('utf-8')
		#生成一个支持xpath解析的对象
		html = etree.HTML(html)
		return html
