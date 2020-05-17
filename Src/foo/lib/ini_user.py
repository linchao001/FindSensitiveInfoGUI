import configparser

class GetINI:
	'提供读写ini类型文件和读取值得一些方法'
	def __init__(self):
		'实例化ConfigParser()对象'
		self.conf = configparser.ConfigParser()

	def Read(self, inifilename):
		'读取ini文件'
		self.conf.read(inifilename,encoding="utf-8-sig")

	#获取ini文件内所有的section，以列表形式返回['path', 'keyword']
	def GetSections(self):
		return self.conf.sections()

	#'获取指定section下所有options ，以列表形式返回['Keyword_1', 'Keyword_2']'
	def GetOptions(self,section):	
		return self.conf.options(section)

	#'获取指定section下所有的键值对，以元祖列表形式返回[('Keyword_1', 'F_PAN'), ('Keyword_2', 'F_VALIDDATE')]'
	def GetItems(self,section):	
		return self.conf.items(section)

	#'获取指定section中option的值，返回为string类型'
	def Get(self,section,option):
		return self.conf.get(section,option)

	#判断是否存在指定section
	def HasSection(self,section):
		return self.conf.has_section(section)


	#删除指定section
	def DelSection(self,section):
		self.conf.remove_section(section)

	#增加指定section
	def AddSection(self,section):
		self.conf.add_section(section)

	#增加指定section下的key和value
	def AddOption(self,section,key,value):
		self.conf.set(section,key,value)

	#写指令，对配置文件进行修改后，一定要执行写指令
	def Write(self,inifilename):
		with open(inifilename,'w') as configfile:
			self.conf.write(configfile)
