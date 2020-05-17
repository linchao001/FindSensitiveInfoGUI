
# --coding:utf-8-- #
from lxml import etree
#创建自定义解析器
parser = etree.HTMLParser(encoding="GBK")
#解析htmml,
htmlelement = etree.parse("D:\GrgBanking\eCAT\Resource\Common\HTML\SouthVoyageCard.html", parser=parser)
#print(type(htmlelement))
#输出字符串格式的html
html = etree.tostring(htmlelement, encoding ='utf-8').decode('utf-8')
#print(type(html))
#返回一个支持xPath语法的对象
page = etree.HTML(html)
#print(type(page))
#hrefs = page.xpath("/html/body/div/table/tr/td[@id='txtIDCard']")
#返回一个节点列表
hrefs = page.xpath("//*[@id='txtIDCard']")


#print(hrefs[0].tag)
#print(hrefs[0].attrib)
print(hrefs[0].text)




for a in hrefs:
	print(a.attrib)








