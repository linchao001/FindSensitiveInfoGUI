import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import os
import re
import time
import win32api

from ini_user import GetINI
from xml_user import GetXML

import global_variable

class StrFindGUI:

	def __init__(self):
		'类的构造函数 主要用于绘制应用程序的界面'
		self.root = Tk()
		self.root.title(u"敏感信息查找")
		self.root.geometry('800x600')
		self.root.resizable(FALSE,FALSE)

		#top
		self.top_frame = Frame(self.root)
		self.top_frame.grid(row=0,column=0,columnspan=200)

		#top_label_logPath
		self.path_label = Label(self.top_frame,text=u"日志路径：", padx=1, pady=1)
		self.path_label.grid(row=0,column=0)

		#top_entry_logPath
		self.path = StringVar()
		self.path_entry = Entry(self.top_frame, textvariable=self.path, highlightthickness=2, width=94)
		self.getini = GetINI()																				#实例化一个GetINI对象，用来读取ini文件
		self.getini.Read(global_variable.path_Keywordini)
		self.path_name = self.getini.Get('path','PathName')
		self.path.set(self.path_name)																	#设置默认搜索路径
		self.path_entry.grid(row=0,column=1,columnspan=4)
		
		#top_button
		self.path_button = Button(self.top_frame, text=u"打开", padx=1, pady=1,width=6, cursor='hand2', command=self.SelectPath)
		self.path_button.grid(row=0,column=5)


		#top_label_configurepath
		self.configure_path_label = Label(self.top_frame, text=u"配置路径：",padx=1,pady=1)
		self.configure_path_label.grid(row=1,column=0)

		#top_entry_configurepath
		self.configure_path_name = StringVar()
		self.configure_path_entry = Entry(self.top_frame, textvariable=self.configure_path_name,highlightthickness=2,width=94)
		self.configure_path_entry.grid(row=1,column=1,columnspan=4)


		#top_button_configurepath
		self.configurepath_button = Button(self.top_frame, text=u"打开", padx=1, pady=1, width=6, cursor="hand2", command=self.SelectConfigurePath)
		self.configurepath_button.grid(row=1,column=5)

		
		#top_label
		self.configure_path_label = Label(self.top_frame, text=u"搜索结果：",padx=1,pady=1)
		self.configure_path_label.grid(row=2,column=0)

		#top_entry
		self.related_file_name = StringVar()
		self.search_display =Entry(self.top_frame, textvariable=self.related_file_name,highlightthickness=2, width=94, state=DISABLED)
		self.search_display.grid(row=2,column=1,columnspan=4)

		#top_button
		self.search_button = Button(self.top_frame, text=u"搜索",padx=1, pady=1,width=6,cursor='hand2',command=self.SearchSensitiveInfo)
		self.search_button.grid(row=2,column=5)

		
		#top_button
		self.search_button = Button(self.top_frame, text=u"选择", padx=3, pady=6,width=7,cursor='hand2',command=self.SelectKeyword)
		self.search_button.grid(row=3,column=0,padx=10,rowspan=2)

		#top_checkbutton
		#标记com.txt或者ecat.txt日志是否加密
		self.tk_var_com = IntVar()
		self.isEncriptComtxt_checkbutton = Checkbutton(self.top_frame,text="com日志是否加密", variable=self.tk_var_com, command=self.isEncryptLog)
		self.isEncriptComtxt_checkbutton.grid(row=3,column=1)

		self.tk_var_log = IntVar()
		self.isEncriptComtxt_checkbutton = Checkbutton(self.top_frame,text="ecat日志是否加密", variable=self.tk_var_log, command=self.isEncryptLog)
		self.isEncriptComtxt_checkbutton.grid(row=4,column=1)

		#top_button
		self.search_button = Button(self.top_frame, text=u"检查Resources", padx=3, pady=6,width=13,cursor='hand2',command=self.SearchInHtml)
		self.search_button.grid(row=3,column=2,padx=10,rowspan=2)

		#top_button
		self.search_button = Button(self.top_frame, text=u"检查账密配置", padx=3, pady=6,width=13,cursor='hand2',command=self.SearchPassword)
		self.search_button.grid(row=3,column=3,padx=10,rowspan=2)

		

		#mid
		#list keyword 
		self.keyword_list_01 = ScrolledText(self.root,width=15,height=20)
		self.keyword_list_01.grid(row=1,column=0,rowspan=2,sticky=W)
		self.keyword_list_01.insert(END,"报文域\n支持自定义输入 \n")
		self.keyword_list_01.tag_add('tag_01','1.0','2.100')
		self.keyword_list_01.tag_config('tag_01', background='yellow', foreground='red')
		self.keyword_list_01.tag_bind('tag_01',"<Enter>",self.ShowDetails)
		self.keyword_list_01.tag_bind('tag_01',"<Leave>",self.HideDetails)

		
		self.keyword_list_02 = ScrolledText(self.root,width=15,height=10)
		self.keyword_list_02.grid(row=1,column=1)
		self.keyword_list_02.insert(END,"敏感文件路径\n支持自定义输入 \n")
		self.keyword_list_02.tag_add('tag_01','1.0','2.100')
		self.keyword_list_02.tag_config('tag_01', background='yellow', foreground='red')
		self.keyword_list_02.tag_bind('tag_01',"<Enter>",self.ShowDetails)
		self.keyword_list_02.tag_bind('tag_01',"<Leave>",self.HideDetails)


		self.keyword_list_03 = ScrolledText(self.root,width=15,height=9)
		self.keyword_list_03.grid(row=2,column=1)
		self.keyword_list_03.insert(END,"以身份证信息命名的文件\n支持自定义输入 \n")
		self.keyword_list_03.tag_add('tag_01','1.0','2.100')
		self.keyword_list_03.tag_config('tag_01', background='yellow', foreground='red')
		self.keyword_list_03.tag_bind('tag_01',"<Enter>",self.ShowDetails)
		self.keyword_list_03.tag_bind('tag_01',"<Leave>",self.HideDetails)

		self.keyword_list_04 = ScrolledText(self.root,width=15,height=15)
		self.keyword_list_04.grid(row=3,column=0,sticky=W)
		self.keyword_list_04.insert(END,"个人隐私信息\n支持自定义输入 \n")
		self.keyword_list_04.tag_add('tag_01','1.0','2.100')
		self.keyword_list_04.tag_config('tag_01', background='yellow', foreground='red')
		self.keyword_list_04.tag_bind('tag_01',"<Enter>",self.ShowDetails)
		self.keyword_list_04.tag_bind('tag_01',"<Leave>",self.HideDetails)


		self.keyword_list_05 = ScrolledText(self.root,width=15,height=15)
		self.keyword_list_05.grid(row=3,column=1,sticky=W)
		self.keyword_list_05.insert(END,"密钥信息、其他安全信息\n支持自定义输入 \n")
		self.keyword_list_05.tag_add('tag_01','1.0','2.100')
		self.keyword_list_05.tag_config('tag_01', background='yellow', foreground='red')
		self.keyword_list_05.tag_bind('tag_01',"<Enter>",self.ShowDetails)
		self.keyword_list_05.tag_bind('tag_01',"<Leave>",self.HideDetails)


		self.sensitive_info_listbox = ScrolledText(self.root,width=74,height=29,spacing1=3)
		self.sensitive_info_listbox.grid(row=1,column=6,rowspan=10,columnspan=100)
		'''
		#test&debug
		for item in range(1, 300):
       		 self.sensitive_info_listbox.insert(END, item)
		
		'''
		self.ModifyKeywordini()	
		self.CreateChildWindow()

		#读取keyword.ini中的sensitive_documents，并将其值插入到界面上的self.keyword_list_02文本框中
		sensitive_documents = self.getini.GetItems('sensitive_documents')
		line = 2
		for a_sensitve_document in sensitive_documents:
			self.keyword_list_02.insert(END, a_sensitve_document[1]+'\n')
			#为插入的关键字增加Tag
			tag_name = 'position_tag_' + str(line)
			#self.keyword_list_02.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
			self.keyword_list_02.tag_add(tag_name,'{line}.0'.format(line=line),'{line}.end'.format(line=line))
			self.keyword_list_02.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.Locate_Keyword_In_Result, tag_name=tag_name, keyword_listbox=self.keyword_list_02))
			line = line + 1

		#读取keyword.ini中的idcardfiles_path，并将其值插入到界面上的self.keyword_list_03文本框中
		idcardfiles_paths = self.getini.GetItems('idcardfiles_path')
		line = 2
		for a_idcardfiles_path in idcardfiles_paths:
			self.keyword_list_03.insert(END, a_idcardfiles_path[1]+'\n')
			#为插入的关键字增加Tag
			tag_name = 'position_tag_' + str(line)
			#self.keyword_list_04.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
			self.keyword_list_03.tag_add(tag_name,'{line}.0'.format(line=line),'{line}.end'.format(line=line))
			self.keyword_list_03.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.Locate_Keyword_In_Result, tag_name=tag_name, keyword_listbox=self.keyword_list_03))
			line = line + 1

		#读取keyword.ini中的personal_privacy，并将其值插入到界面上的self.keyword_list_04文本框中
		personal_privacy = self.getini.GetItems('personal_privacy')
		line = 2
		for a_personal_privacy in personal_privacy:
			self.keyword_list_04.insert(END, a_personal_privacy[1]+'\n')
			#为插入的关键字增加Tag
			tag_name = 'position_tag_' + str(line)
			#self.keyword_list_04.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
			self.keyword_list_04.tag_add(tag_name,'{line}.0'.format(line=line),'{line}.end'.format(line=line))
			self.keyword_list_04.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.Locate_Keyword_In_Result, tag_name=tag_name, keyword_listbox=self.keyword_list_04))
			line = line + 1

		#读取keyword.ini中的keyinfo，并将其值插入到界面上的self.keyword_list_04文本框中
		keyinfo = self.getini.GetItems('keyinfo')
		line = 2
		for a_keyinfo in keyinfo:
			self.keyword_list_05.insert(END, a_keyinfo[1]+'\n')
			#为插入的关键字增加Tag
			tag_name = 'position_tag_' + str(line)
			#self.keyword_list_05.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
			self.keyword_list_05.tag_add(tag_name,'{line}.0'.format(line=line),'{line}.end'.format(line=line))
			self.keyword_list_05.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.Locate_Keyword_In_Result, tag_name=tag_name, keyword_listbox=self.keyword_list_05))
			line = line + 1

		#读取keyword.ini中的special_paths并保存在全局变量self.special_paths里，将在这些路径里搜索不包含子文件夹的文件
		#self.special_paths变量中保存的路径，意味着不会查找该路径中子文件夹中的文件
		self.special_paths = []
		paths = self.getini.GetItems('special_paths')
		for a_paths in paths:
			self.special_paths.append(a_paths[1])
		
		#self.menubar = Menu(self.child_window, tearoff=False)
		self.root.mainloop()



	def CreateChildWindow(self):
		self.child_window=Toplevel()
		self.child_window.title('请选择')
		self.child_window.geometry('800x600')
		self.child_window.resizable(TRUE,TRUE)
		#self.child_window.attributes('-topmost',True)
		#self.child_window.overrideredirect(boolean=True)
		self.child_window.protocol("WM_DELETE_WINDOW", self.callback)

		
		#top_button
		self.button_01 = Button(self.child_window, text=u"选择所有",padx=10, pady=6,width=7,cursor='hand2',command=self.SelectAllKeyword)
		self.button_01.grid(row=0,column=0,padx=50)

		self.button_02 = Button(self.child_window, text=u"全不选择",padx=10, pady=6,width=7,cursor='hand2',command=self.DelAllSelect)
		self.button_02.grid(row=0,column=1,padx=50)

		self.button_03 = Button(self.child_window, text=u"不选择屏蔽域",padx=10, pady=6,width=7,cursor='hand2',command=self.DelMaskField)
		self.button_03.grid(row=0,column=2,padx=50)

		self.button_04 = Button(self.child_window, text=u"选择敏感域",padx=10, pady=6,width=7,cursor='hand2',command=self.SelectSensitiveField)
		self.button_04.grid(row=0,column=3,padx=50)

		self.button_05 = Button(self.child_window, text=u"确认",padx=10, pady=6,width=7,cursor='hand2',command=self.Confirm_button)
		self.button_05.grid(row=1,column=0,padx=50)

		self.child_window.withdraw()
	

	def callback(self):
		tkinter.messagebox.showinfo("提醒","该操作将不会使用本次选中的报文域参与搜索")
		self.child_window.withdraw()

	def SelectPath(self):
		'与第一个“打开”按钮绑定，将选中文件路径设置为搜索路径'
		path_name = filedialog.askdirectory(initialdir="D:/")
		self.path.set(path_name)


	def SelectConfigurePath(self):
		'与第二个“打开”按钮绑定，将选中文件路径置为通讯报文配置文件所在路径'
		path_name = filedialog.askopenfilename(initialdir="D:/",title=u"选择8583配置文件",filetypes=[('xml','*.xml'),('All Files','*')])
		self.configure_path_name.set(path_name)
		#重新指定报文配置文件后，需要重新抓取报文域并更新到Keyword.ini
		self.ModifyKeywordini()

	def SelectKeyword(self):
		'与"选择"按钮绑定'
		self.child_window.deiconify()

		i=2
		j=0
		z=0
		try:
			for a_Keyword_FieldName in self.Keyword_FieldNames:
				keyword_checkbutton = Checkbutton(self.child_window, text=a_Keyword_FieldName, variable=self.tk_int_var[z],cursor='hand2')
				keyword_checkbutton.bind("<Button-3>",self.HandlerAdaptor(self.pop_menu,a_Keyword_FieldName=a_Keyword_FieldName))
				keyword_checkbutton.grid(row=i, column=j, sticky=W)
				
				i = i + 1
				z = z + 1
				if i == 20:
					j = j + 1
					i = 2
			self.SelectSensitiveField()
		except	AttributeError:
			self.child_window.attributes('-topmost',False)
			tkinter.messagebox.showinfo('提示','没有找到报文配置文件,请手动指定')
			self.child_window.withdraw()
			self.child_window.attributes('-topmost',True)
			return


	def pop_menu(self,event,a_Keyword_FieldName):
		self.menubar = Menu(self.child_window, tearoff=False)
		ID = a_Keyword_FieldName.partition(":")[0]
		self.menubar.add_command(label = self.Field_Description[ID])
		self.menubar.post(event.x_root, event.y_root)

	def ShowDetails(self,event):
		self.details = Menu(self.root, tearoff=False,font = "黑体")
		self.details.add_command(label = "支持自定义输入，每个关键字以回车键分隔")
		self.details.post(event.x_root, event.y_root)

	def HideDetails(self,event):

		self.details.unpost()
		self.details.delete(0)

	def isEncryptLog(self):
		path_name = self.path.get()
		try:
			self.all_files=''																	#初始化一个保存所有文件的变量
			self.all_files = self.TraversalFiles(path_name)										#遍历指定路径下的所有文件
		except FileNotFoundError:
			tkinter.messagebox.showinfo('提示','搜索路径为空或者该路径不存在')
		else:
			self.all_files = self.all_files.strip('\n')												#字符串首尾去换行符处理
			files = self.all_files.split('\n')													#以\n为分割符，返回分割后的列表

		#若勾选com\eCat日志是否加密复选框，则将com\eCat日志后缀修改为.Encrypted
		#若取消勾选com\eCat日志是否加密复选框,则将com\eCat日志后缀修改为.txt
		if self.tk_var_com.get() == 1:
			for a_file in files:
				a_file_name = a_file.rpartition("\\")
				if a_file_name[2][0:3] == "COM" and a_file_name[2][3:11].isdigit():
					portion = os.path.splitext(a_file)
					newname = portion[0] + '.Encrypted'
					os.rename(a_file,newname)			
		else:
			for a_file in files:
				a_file_name = a_file.rpartition("\\")
				if a_file_name[2][0:3] == "COM" and a_file_name[2][3:11].isdigit():
					portion = os.path.splitext(a_file)
					newname = portion[0] + '.txt'
					os.rename(a_file,newname)

		if self.tk_var_log.get() == 1:
			for a_file in files:
				a_file_name = a_file.rpartition("\\")
				if a_file_name[2][0:4] == "eCAT" and a_file_name[2][4:12].isdigit():
					portion = os.path.splitext(a_file)
					newname = portion[0] + '.Encrypted'
					os.rename(a_file,newname)
		else:
			for a_file in files:
				a_file_name = a_file.rpartition("\\")
				if a_file_name[2][0:4] == "eCAT" and a_file_name[2][4:12].isdigit():
					portion = os.path.splitext(a_file)
					newname = portion[0] + '.txt'
					os.rename(a_file,newname)
		
	
	def SelectAllKeyword(self):
		'与“选择所有”按钮绑定，选择所有关键字'
		i = 0
		for var in self.tk_int_var:
			self.tk_int_var[i].set(1)
			i = i + 1
			

	def DelAllSelect(self):
		'与“全不选择”按钮绑定，所有关键字都不选择'
		i = 0
		for var in self.tk_int_var:
			self.tk_int_var[i].set(0)
			i = i + 1

	def DelMaskField(self):
		'与“不选择屏蔽域”按钮绑定，打解包配置文件中已经配置屏蔽的报文域取消选择'
		#获取打解包配置文件的路径，并读取其中的MaskFieldName
		atmp_conf_path = self.configure_path_name.get()
		getxml = GetXML()
		root = getxml.Read(atmp_conf_path)
		try:
			MaskFieldName = root.find('TransactionFieldConfig').attrib['MaskFieldName']
		except:
			tkinter.messagebox.showinfo('提示','没有在打解包配置文件中找到MaskFieldName')
			return
		MaskFieldName = MaskFieldName.strip().split('|')
		#轮询self.Keyword_FieldNames，判断报文域是否在MaskFieldName列表里，如果在，则将这个报文域的复选框取消打勾
		i = 0
		for a_Keyword_FieldName in self.Keyword_FieldNames:
			a_Keyword_FieldName = a_Keyword_FieldName.partition(":")[2]
			if a_Keyword_FieldName in MaskFieldName:
				self.tk_int_var[i].set(0)
			i = i + 1


	def SelectSensitiveField(self):
		'与“选择敏感域”按钮绑定，将安全技术规范中指定的敏感域默认勾选'
		#根据《软件安全技术规范》，下列序号报文域属于敏感报文域
		sensitiveFieldBitID = [2,14,22,25,26,35,36,45,48,52,53,55,57,58,60,61,64,96,102,103,128]
		#轮询self.Keyword_FieldNames,判断域序号是否在sensitiveFieldBitID列表里，如果在，则将这个报文域的复选框打勾
		i = 0
		for a_Keyword_FieldName in self.Keyword_FieldNames:
			a_Keyword_FieldName = int(a_Keyword_FieldName.partition(":")[0])
			if a_Keyword_FieldName in sensitiveFieldBitID:
				self.tk_int_var[i].set(1)
			i = i + 1

			
	def Confirm_button(self):
		'与“确认”按钮绑定，隐藏子窗口，将选中的关键字保存在一个列表，并插入到应用界面上，用来参与搜索'
		self.child_window.withdraw()
		i = 0
		tkIntVar_value_list = []
		for var in self.tk_int_var:
			tkIntVar_value_list.append(self.tk_int_var[i].get())
			i = i + 1
		selected_result_dict = dict(zip(self.Keyword_FieldNames,tkIntVar_value_list))
		selected_keywords = []                                                         #初始化一个列表用来保存被选中的报文域关键字
		for var in selected_result_dict.items():
			if var[1] == 1:
				selected_keywords.append(var[0])
		#向keyword_list_01中插入关键字前，需要清空该文本框
		self.keyword_list_01.delete(3.0,END)
		line = 2
		for var in selected_keywords:
			self.keyword_list_01.insert(END,'\n'+var)
			#为插入的关键字增加Tag
			tag_name = 'position_tag_' + str(line)
			#self.keyword_list_05.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
			self.keyword_list_01.tag_add(tag_name,'{line}.0'.format(line=line),'{line}.end'.format(line=line))
			self.keyword_list_01.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.Locate_Keyword_In_Result, tag_name=tag_name, keyword_listbox=self.keyword_list_01))
			line = line + 1


	#debug&test temporarily
	#Get Keyword real time	
	def GetKeyword_realtime(self):
		self.T=self.keyword_list.get(0.0,END)
		messagebox.showinfo('提示',self.T)

	
	def TraversalFiles(self,path):
		'递归遍历指定文件夹下所有的文件（包含子文件夹中的文件）'
		#将该文件夹（包含子文件夹）中的所有文件，以字符串形式保存到self.all_files变量中，各文件之间以'\n'作分隔符
		list = os.listdir(path)
		for i in range(0,len(list)):
			temp_file = os.path.join(path, list[i])
			#messagebox.showinfo('提示',temp_file)
			if not os.path.isdir(temp_file):
				self.all_files = self.all_files + temp_file+'\n'
			else:
				self.TraversalFiles(temp_file)

		return self.all_files

					
	def ScanATMP8583(self):
		'查找程序使用的是什么报文配置文件，并返回其绝对路径'

		getxml = GetXML()

		#获取MessageConfig.xml的根节点
		try:
			root = getxml.Read("D:\GrgBanking\eCAT\Config\MessageConfig.xml")
		except FileNotFoundError:
			tmp = '-----------------------------------------------------------------'
			self.sensitive_info_listbox.insert(END, tmp)
			tmp = '没有找到报文配置文件,请手动指定'
			self.sensitive_info_listbox.insert(END, tmp)
			tmp = '-----------------------------------------------------------------'
			self.sensitive_info_listbox.insert(END, tmp)
			tkinter.messagebox.showinfo('提示','没有找到报文配置文件,请手动指定')
			return


		for DataFormatterService in root.iter(tag='DataFormatterService'):
			#先判断DataFormatterService alias="Default"才继续判断是否包含ATMP
			if (DataFormatterService.attrib['alias'] == 'Default') and (DataFormatterService.attrib['cfg'].find('ATMP') != -1):
				atmp_conf_path = "D:\GrgBanking\eCAT" + DataFormatterService.attrib['cfg'][2:]

		self.configure_path_name.set(atmp_conf_path)

		#获取ATMP_8583.xml或者ATMP_FixedLen.xml的根节点
		if atmp_conf_path.find('8583') == -1:
			tmp = '-----------------------------------------------------------------'
			self.sensitive_info_listbox.insert(END, tmp)
			tmp = '该版本的报文格式非8583，可能是定长报文格式'
			self.sensitive_info_listbox.insert(END, tmp)
			tmp = '-----------------------------------------------------------------'
			self.sensitive_info_listbox.insert(END, tmp)
		return atmp_conf_path

	def ModifyKeywordini(self):
		'将FieldName遍历抓取出来，保存在Keyword.ini中'

		atmp_conf_path = self.configure_path_name.get()
		print(atmp_conf_path)
		if len(atmp_conf_path) == 0:
			atmp_conf_path = self.ScanATMP8583()

		getxml = GetXML()
		root = getxml.Read(atmp_conf_path)

		getini = GetINI()
		getini.Read(global_variable.path_Keywordini)
		getini.DelSection('FieldName')
		getini.Write(global_variable.path_Keywordini)
		getini.AddSection('FieldName')
		
		try:
			Fields = root.find("TransactionFieldConfig").find("BitmapFields").findall("Field")
		except AttributeError:
			tkinter.messagebox.showinfo('提示','从报文配置文件里抓取关键字发生异常')
			return
		
		n = 1
		#初始化一个字典，BitID:Description形式。用来通过BitID找到该域的域描述
		self.Field_Description = dict()
		for a_Field in Fields:
			key = 'FieldName' + '_' + str(n)
			FieldName = a_Field.find("Data").attrib['FieldName']
			BitID = a_Field.attrib['BitID']
			Description = a_Field.attrib['Description']
			self.Field_Description[BitID] = Description
			#FieldName = FieldName + ":" + BitID
			FieldName = BitID + ":" + FieldName
			getini.AddOption('FieldName', key, FieldName)
			n = n + 1
			getini.Write(global_variable.path_Keywordini)	

		self.Keyword_FieldNames = []									#初始化一个全局列表用来保存从报文配置文件中获取的报文域

		try:
			self.getini = GetINI()										#实例化一个GetINI对象，用来读取ini文件
			self.getini.Read(global_variable.path_Keywordini)
			FieldNames = self.getini.GetItems('FieldName')				#从keyword.ini中获取FieldName节点下的键值对，返回元祖列表
			for a_FieldName in FieldNames:
				self.Keyword_FieldNames.append(a_FieldName[1])

			self.tk_int_var = []										#初始化一个列表，用来保存tk整形变量。
			for a_Keyword_FieldName in self.Keyword_FieldNames:
				self.tk_int_var.append(IntVar()) 
		except configparser.NoSectionError:
			pass
	
	
	#依次对每个文件中的每一行，进行遍历关键字搜索
	def Process(self,a_file_name,line):
		'处理字符串文本行，如果有敏感信息，分别打印到日志和应用界面的列表里，如果没有，不做任何处理' 
		line = line.strip()

		#将报文域关键字、个人隐私关键字、密钥等安全信息关键字统一保存在all_keywords列表里
		fieldnamesandID_keywords = self.keyword_list_01.get(3.0,END)										#初始化一个变量用来保存当前被选中的报文域关键字
		#目前Field_names_keyword为BitID：FieldName格式，需要去除BitID
		field_names_keywords = []
		fieldnamesndID_keywords = fieldnamesandID_keywords.strip().split('\n')
		try:
			for a_fieldnamesndID_keyword in fieldnamesndID_keywords:
				field_names_keywords.append((a_fieldnamesndID_keyword.split(":"))[1])
		except:
			pass
		#初始化一个变量用来保存个人隐私信息关键字
		personal_privacy_keywords = []
		personal_privacy_keywords = (self.keyword_list_04.get(3.0,END)).strip().split('\n')
		#初始化一个变量用来保存密钥等信息关键字	
		keyinfo_keywords = []							
		keyinfo_keywords = (self.keyword_list_05.get(3.0,END)).strip().split('\n')

		self.all_keywords = field_names_keywords + personal_privacy_keywords + keyinfo_keywords

		for a_keyword in self.all_keywords:
			self.root.update()
			if re.search(a_keyword, line, re.I):
				print(line,file=open("Sensitive_log_01.txt", 'a', encoding='utf-8'))
				'''
				if line.count('*') <= 2:

					#no_repeat为重复标志，对于当前字符串文本，将和缓存列表sensitive_lines里的文本行比较，若相同，则将重复标志位置0
					no_repeat = 1
					if line[0:2].isdigit():
						for a_sensitive_line in self.sensitive_lines:
							if line[12:] == a_sensitive_line[12:]:								#日志中时间为12个字符
								no_repeat = 0
					else:
						for a_sensitive_line in self.sensitive_lines:
							if line == a_sensitive_line:
								no_repeat = 0
					
					#判断重复标志位，仅当重复标志位为1时，才将该行插入到应用界面的列表框里
					if no_repeat:
						self.sensitive_info_listbox.insert(END, line)							#插入文本行到应用界面列表框里
						self.sensitive_line_source[line] = a_file_name							#以字典形式保存该行所在的文件信息,即{line:源文件路径}
						self.keyword_in_sensitive_line[line] = a_keyword						#以字典形式保存改行包含的关键字，即{line:a_keyword}
						self.root.update()														#实时更新界面信息

					self.sensitive_lines.append(line)											#将文本行插入缓存列表里
					'''
	def SearchKeywordInfo(self):
		tmp = '-----------------------------------------------------------------\n'
		self.sensitive_info_listbox.insert(END, tmp)
		tmp = '操作正在进行中，请稍后……\n'
		self.sensitive_info_listbox.insert(END, tmp)
		tmp = '-----------------------------------------------------------------\n'
		self.sensitive_info_listbox.insert(END, tmp)

		path_name = self.path.get()																#初始化一个保存当前搜索路径的变量
		
		try:
			self.all_files=''																	#初始化一个保存所有文件的变量
			self.all_files = self.TraversalFiles(path_name)										#遍历指定路径下的所有文件
		except FileNotFoundError:
			tkinter.messagebox.showinfo('提示','搜索路径为空或者该路径不存在')
		else:
			self.all_files = self.all_files.strip('\n')												#字符串首尾去换行符处理
			files = self.all_files.split('\n')														#以\n为分割符，返回分割后的列表

			self.sensitive_lines = []																#该列表是一个临时缓存，对敏感信息行进一步处理时需要用到
			self.sensitive_line_source = dict()														#创建一个字典，{line:filename}形式，用来定位该行敏感信息所在文件路径
			self.keyword_in_sensitive_line = dict()													#创建一个字典，{line:keyword}形式，用来定位该行包含哪个关键字
			#初始化一个列表，用来保存(filepath,index,line)元组
			self.all_line_details = []
			#初始化一个元素，用来保存行信息，包含文件路径，行索引，行内容
			a_line_detail = ()
			#先创建一个Sensitive_log_01.txt，防止第一次搜索结果为空时，导致第二次搜索报错
			print('Hello~~\n',file=open("Sensitive_log_01.txt", 'a', encoding='utf-8'))

			#处理txt和log文件，检查是否包含敏感信息
			for a_file in files:					
				#判断文件是否是txt或者log类型的，如果是就搜索敏感信息，如果不是就进入下一次循环判断下一个文件的类型
				#下面逻辑语句代替：
				#if a_file.endswith('txt') or a_file.endswith('log'):
				if a_file.rfind('.') != -1 and (a_file[a_file.rfind('.')+1:] == 'txt' or a_file[a_file.rfind('.')+1:] == 'log'):

					'''
					#打印文件路径信息到日志里，方便定位敏感信息
					print('\n\n---------------------------',file=open("Sensitive_log.txt", 'a', encoding='utf-8'),end='')
					print(a_file,file=open("Sensitive_log.txt", 'a', encoding='utf-8'),end='')
					print('---------------------------\n\n',file=open("Sensitive_log.txt", 'a', encoding='utf-8'),end='')
					'''

					#打印查找状态到界面上
					tmp = '正在查找：'+a_file
					self.related_file_name.set(tmp)


					#处理文件内容
					with open(a_file,'rb') as f:
						#每打开一个文件，索引从1开始计数
						index = 1
						for line in f.readlines():							
							a_line_detail = (a_file, index, str(line,'utf-8','ignore'))
							index = index + 1
							self.all_line_details.append(a_line_detail)
							try:
								self.Process(a_file,str(line,'utf-8','ignore'))
							except re.error:
								tkinter.messagebox.showinfo('提示','关键字不符合正则表达式规则，如[,需要转义才符合规则，转义后为\[')
								tmp = '注意关键字格式，请更新关键字！！！'
								self.related_file_name.set(tmp)
								return
								

	
	def SearchSensitiveFile(self):
		'处理敏感路径，打印路径里所有文件'
		#因为插入了下面三行字符串，所以行索引需要+3
		self.line_index = self.line_index + 3
		#打印提示信息到界面
		tmp = '-----------------------------------------------------\n'
		self.sensitive_info_listbox.insert(END, tmp)
		tmp = '请注意，下面的文件可能为敏感文件，双击可查看\n'
		self.sensitive_info_listbox.insert(END, tmp)
		tmp = '-----------------------------------------------------\n'
		self.sensitive_info_listbox.insert(END, tmp)
	
		#打印信息到日志
		tmp = '请注意，下面的文件可能为敏感文件\n'
		print('\n\n-----------------------------\n',file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'),end='')
		print(tmp,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'),end='')
		print('-------------------------------\n\n',file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'),end='')
		
		#获取keyword_list_02中所有敏感文件可能存在的路径
		all_sensitive_paths = self.keyword_list_02.get(2.0,END)
		all_sensitive_paths = all_sensitive_paths.strip()
		all_sensitive_paths = all_sensitive_paths.split()


		for a_sensitive_path in all_sensitive_paths:
			if os.path.exists(a_sensitive_path):													#判断该路径是否存在
				self.all_files=''
				#判断该路径是否只需要寻找根路径下的文件，而不需要寻找子文件夹中的文件
				#如果该路径在self.special_paths里能找到，则self.all_files不保存该路径下的子文件夹中的文件
				#反之，则需要保存该路径下包含所有子文件夹中所有文件
				if a_sensitive_path in self.special_paths:
					fileandfolder = os.listdir(a_sensitive_path)
					for onlyfile in fileandfolder:
						onlyfile = os.path.join(a_sensitive_path,onlyfile)
						if not os.path.isdir(onlyfile):
							self.all_files = self.all_files + onlyfile +'\n'
				else:
					#判断该路径下是否有文件，即遍历该路径（包含子路径）下所有文件，保存在self.all_files中
					self.TraversalFiles(a_sensitive_path)
				#如果有文件就处理	
				if self.all_files.strip():												
					files = self.all_files.split('\n')
					for a_file in files:
						self.sensitive_info_listbox.insert(END, '{a_file}\n'.format(a_file=a_file))		#将疑似敏感文件打印至应用程序界面
						#为记录增加Tag
						tag_name = 'position_tag_' + str(self.line_index)
						#self.keyword_list_04.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
						self.sensitive_info_listbox.tag_add(tag_name,'{line_index}.0'.format(line_index=self.line_index),'{line_index}.end'.format(line_index=self.line_index))
						self.sensitive_info_listbox.tag_bind(tag_name,'<Double-Button-1>',self.HandlerAdaptor(self.OpenThisFile, tag_name=tag_name, keyword_listbox=self.sensitive_info_listbox))
						self.line_index = self.line_index + 1
						self.sensitive_line_source[a_file] = a_file 									#以字典形式保存该文件，用来定位源文件
						print(a_file,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'))			#将疑似敏感文件打印至日志

	def SearchIdcardFile(self):
		'搜索配置文件中配置的路径中以身份证号和姓名命名的文件，并打印出来'
		#因为插入了下面三行字符串，所以行索引需要+3
		self.line_index = self.line_index + 3
		#打印提示信息到界面
		tmp = '------------------------------------------------------\n'
		self.sensitive_info_listbox.insert(END, tmp)
		tmp = '请注意，下面的文件可能为身份证文件，双击可查看\n'
		self.sensitive_info_listbox.insert(END, tmp)
		tmp = '------------------------------------------------------\n'
		self.sensitive_info_listbox.insert(END, tmp)
	
		#打印信息到日志
		tmp = '请注意，下面的文件可能为身份证文件'
		print('\n\n---------------------------',file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'),end='')
		print(tmp,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'),end='')
		print('---------------------------\n\n',file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'),end='')

		#获取
		all_idcardfiles_paths = self.keyword_list_03.get(2.0,END)
		all_idcardfiles_paths = all_idcardfiles_paths.strip()
		all_idcardfiles_paths = all_idcardfiles_paths.split()

		#实例化一个getxml对象，读取IdcardInfo.xml配置文件
		getxml = GetXML()																			#实例化一个GetXML对象，用来处理XML文件
		root = getxml.Read(global_variable.path_IdcardInfoxml)
		
		for a_idcardfiles_path in all_idcardfiles_paths:
			if os.path.exists(a_idcardfiles_path):													#判断该路径是否存在
				self.all_files=''	
				self.TraversalFiles(a_idcardfiles_path)												#判断该路径下是否有文件，即遍历该路径（包含子路径）下所有文件，保存在self.all_files中
				if self.all_files.strip():																#如果有文件就处理													
					files = self.all_files.split('\n')
					for a_file in files:
						for idcard in root.iter('idcard'):
							if re.search(idcard.find('id').text, a_file, re.I):
								self.sensitive_info_listbox.insert(END, a_file)								#将身份证文件打印至应用程序界面
								#为记录增加Tag
								tag_name = 'position_tag_' + str(self.line_index)
								#self.keyword_list_04.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
								self.sensitive_info_listbox.tag_add(tag_name,'{line_index}.0'.format(line_index=self.line_index),'{line_index}.end'.format(line_index=self.line_index))
								self.sensitive_info_listbox.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.OpenThisFile, tag_name=tag_name, keyword_listbox=self.sensitive_info_listbox))
								self.line_index = self.line_index + 1
								self.sensitive_line_source[a_file] = a_file 								#以字典形式保存该文件，用来定位源文件
								print(a_file,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'))			#将疑似身份证文件打印至日志

							if re.search(idcard.find('name').text, a_file, re.I):
								self.sensitive_info_listbox.insert(END, a_file)								#将身份证文件打印至应用程序界面
								#为记录增加Tag
								tag_name = 'position_tag_' + str(self.line_index)
								#self.keyword_list_04.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
								self.sensitive_info_listbox.tag_add(tag_name,'{line_index}.0'.format(line_index=self.line_index),'{line_index}.end'.format(line_index=self.line_index))
								self.sensitive_info_listbox.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.OpenThisFile, tag_name=tag_name, keyword_listbox=self.sensitive_info_listbox))
								self.line_index = self.line_index + 1
								self.sensitive_line_source[a_file] = a_file 								#以字典形式保存该文件，用来定位源文件
								print(a_file,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'))			#将疑似身份证文件打印至日志
							


	def SearchSensitiveInfo(self):
		'在.txt或者.log文件里查找敏感信息,在可配置的指定路径下搜索敏感文件'

		self.sensitive_info_listbox.delete(0.0,END)

		#已取消该功能，按照波哥的建议，增加功能：将敏感域期望值与MaskFieldName的值比较，如果一个报文域名字在期望值里有，而在MaskFieldName里没有，就将该值打印出来，提醒检查

		
		#在界面指定路径中的txt和log文件搜索查找界面上的关键字
		self.SearchKeywordInfo()
		#self.SearchInLog()
		self.SearchInSennsitiveLog()


		#将配置文件中的配置的敏感路径里所有文件打印出来
		self.SearchSensitiveFile()

		#按照均林建议，增加功能：检查配置文件中配置的路径中以身份证号和姓名命名的文件
		self.SearchIdcardFile()
		
			
	def SearchInSennsitiveLog(self):
		#刷新界面，插入结果之前先清空界面
		self.sensitive_info_listbox.delete(0.0,END)
		#初始化一个字典，用来保存关键字-首个包含关键字行索引的键值对，用来在结果中定位关键字所在记录的首行
		self.keyword_line_dict = {}
		#num用来记录首个包含关键字的行索引
		num = 1
		#line_index用来记录插入的日志行的在Text中索引
		self.line_index = 1
		#进行第二次搜索，并对搜索结果排序后再显示到界面上
		for a_keyword in self.all_keywords:
			self.lines = []                                                                #初始化一个列表保存符合搜索结果的行内容，用来排序。
			with open('Sensitive_log_01.txt', 'rb') as f:
				for line in f.readlines():
					try:
						self.SearchFieldNameInLine(a_keyword,str(line,'utf-8','ignore'))
					except re.error:
						tkinter.messagebox.showinfo('提示','关键字不符合正则表达式规则，如[,需要转义才符合规则，转义后为\[')
						tmp = '注意关键字格式，请更新关键字！！！'
						self.related_file_name.set(tmp)
						return
				#修改字典，记录关键字-首个包含关键字行索引的键值对
				if not len(self.lines):
					self.keyword_line_dict[a_keyword] = None
				else:
					self.keyword_line_dict[a_keyword] = num 
				#行索引根据一个关键字含有的行记录数量联动
				num = len(self.lines) + num + 1
				#对符合含有a_keyword关键字记录的行进行排序，然后将排序后的结果插入到界面上
				self.lines.sort()
				for var in self.lines:
					self.sensitive_info_listbox.insert(END,var)
					print(var,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'))
					#为界面上的行记录增加Tag
					tag_name = 'position_tag_' + str(self.line_index)
					#self.keyword_list_04.tag_add(tag_name,"%d.%d" % (line, column),"%d.end" % (line))
					self.sensitive_info_listbox.tag_add(tag_name,'{line_index}.0'.format(line_index=self.line_index),'{line_index}.end'.format(line_index=self.line_index))
					self.sensitive_info_listbox.tag_bind(tag_name,' <Double-Button-1>',self.HandlerAdaptor(self.Locate_Line_In_log, tag_name=tag_name, keyword_listbox=self.sensitive_info_listbox))
					self.line_index = self.line_index + 1
				self.sensitive_info_listbox.insert(END,'\n')
				self.line_index = self.line_index + 1
		tmp = '查找完毕！！！'
		self.related_file_name.set(tmp)		


	def SearchPassword(self):
		self.sensitive_line_source = dict()
		self.sensitive_info_listbox.delete(0.0,END)
		#获取配置文件中的[xml_path]搜索路径
		getini = GetINI()
		getini.Read(global_variable.path_Keywordini)
		path_name = getini.Get('xml_path','pathname')

		#遍历搜索路径中所有文件，最终保存在一个叫做files的列表里
		try:
			self.all_files = ""
			self.all_files = self.TraversalFiles(path_name)
		except:
			tkinter.messagebox.showinfo("提示","搜索路径为空或者该路径不存在")
		else:
			self.all_files = self.all_files.strip()
			files = self.all_files.split('\n')

		index = 1 #创建索引
		#筛选非./TransactionFlow/路径下xml文件，并在其中寻找账号密码配置
		getxml = GetXML()
		for a_file in files:
			#排除掉./TransactionFlow/路径和./TwinScreen/中的文件
			if a_file.find('TransactionFlow') == -1 and a_file.find('TwinScreen') == -1:
				#如果是xml文件就进行帐号密码查找
				if a_file.endswith('xml'):
					try:
						root = getxml.Read(a_file)
					except:
						tkinter.messagebox.showinfo("警告","解析某个xml时出问题了")
					for a_node in getxml.Iter():
						#声明一个新字典，用来保存将原字典key值转为小写后的字典
						new_dict = {}
						for key,value in a_node.attrib.items():
							new_dict[key.lower()] = value
						flag = 0
						for usename in getini.GetItems('username'):
							if new_dict.get(usename[1]):
								flag = 1
								self.sensitive_info_listbox.insert(END,a_file+'\n')
								self.sensitive_line_source[a_file] = a_file
								tag_name = 'position_tag_' + str(index)
								self.sensitive_info_listbox.tag_add(tag_name, '{line_index}.0'.format(line_index=index),'{line_index}.end'.format(line_index=index))
								self.sensitive_info_listbox.tag_bind(tag_name, '<Double-Button-1>', self.HandlerAdaptor(self.OpenThisFile,tag_name=tag_name,keyword_listbox=self.sensitive_info_listbox))
								index = index + 1
								var = "username="+new_dict.get(usename[1])
								self.sensitive_info_listbox.insert(END,var+'\n')
								index = index + 1
								print(a_file,file=open("Sensitive_log_02.txt",'a',encoding='utf-8'))
								print("username={}".format(new_dict.get(usename[1])),file=open("Sensitive_log_02.txt",'a',encoding='utf-8'))
						for password in getini.GetItems('password'):
							if new_dict.get(password[1]):
								if flag == 0:
									print(a_file, file=open("Sensitive_log_02.txt",'a',encoding='utf-8'))
									self.sensitive_info_listbox.insert(END,a_file+'\n')
									self.sensitive_line_source[a_file] = a_file
									tag_name = 'position_tag_' + str(index)
									self.sensitive_info_listbox.tag_add(tag_name, '{line_index}.0'.format(line_index=index),'{line_index}.end'.format(line_index=index))
									self.sensitive_info_listbox.tag_bind(tag_name, '<Double-Button-1>', self.HandlerAdaptor(self.OpenThisFile,tag_name=tag_name,keyword_listbox=self.sensitive_info_listbox))
									index = index + 1
								var = "password="+new_dict.get(password[1])
								self.sensitive_info_listbox.insert(END,var+'\n')
								index = index + 1
								print("password={}".format(new_dict.get(password[1])),file=open("Sensitive_log_02.txt",'a',encoding='utf-8'))
								self.sensitive_info_listbox.insert(END,'\n')
								index = index + 1
			

	def SearchInHtml(self):
		self.sensitive_line_source = dict()
		self.sensitive_info_listbox.delete(0.0,END)
		#获取配置文件中的[html_path]搜索路径
		getini = GetINI()
		getini.Read(global_variable.path_Keywordini)
		path_name = getini.Get('html_path','pathname')
		all_html_attribute = getini.GetItems('html_attribute')
		html_attribute = []
		for a_html_attribute in all_html_attribute:
			html_attribute.append(a_html_attribute[1])

		#创建索引
		index = 1

		#遍历搜索路径中所有文件，最终保存在一个叫做files的列表里
		try:
			self.all_files = ""
			self.all_files = self.TraversalFiles(path_name)
		except:
			tkinter.messagebox.showinfo("提示","搜索路径为空或者该路径不存在")
		else:
			self.all_files = self.all_files.strip()
			files = self.all_files.split('\n')

		getxml = GetXML()
		for a_file in files:
			if a_file.endswith('html'):
				html = getxml.ReadHtml(a_file)
				hrefs_01 = html.xpath("//*[@id = 'txtIDCard']")
				hrefs_02 = html.xpath("//*[@id = 'txtMobilePhone']")
				hrefs_03 = html.xpath("//*[@id = 'txtName']")
				if hrefs_01 or hrefs_02 or hrefs_03:
					self.sensitive_info_listbox.insert(END, a_file + '\n')
					self.sensitive_line_source[a_file] = a_file
					tag_name = 'position_tag_' + str(index)
					self.sensitive_info_listbox.tag_add(tag_name, '{line_index}.0'.format(line_index=index),'{line_index}.end'.format(line_index=index))
					self.sensitive_info_listbox.tag_bind(tag_name, '<Double-Button-1>', self.HandlerAdaptor(self.OpenThisFile, tag_name=tag_name, keyword_listbox=self.sensitive_info_listbox))
					index = index + 1
				if hrefs_03:
					if hrefs_03[0].text and (len(hrefs_03[0].text.strip()) != 0) :
						var = hrefs_03[0].text.strip()
						self.sensitive_info_listbox.insert(END, 'Name = ' + var + '\n')
						index = index + 1
				if hrefs_01:
					if hrefs_01[0].text and (len(hrefs_01[0].text.strip()) != 0) :
						var = hrefs_01[0].text.strip()
						self.sensitive_info_listbox.insert(END, 'IDCard = ' + var + '\n')
						index = index + 1
				if hrefs_02:
					if hrefs_02[0].text and (len(hrefs_02[0].text.strip()) != 0) :
						var = hrefs_02[0].text.strip()
						self.sensitive_info_listbox.insert(END, 'MobilePhon = ' + var + '\n')
						index = index + 1

	def MeaningForKeyword(self,event):
		'listbox控件绑定的回调函数，以消息框的形式展示该行中的关键字具体信息'
		#按照均林建议，增加该功能。
		matching_flag = False
		#获取选中行中的关键字																			#初始化一个标志位，用来标志该关键字是否是敏感报文域，默认不是。
		try:
			keyword = self.keyword_in_sensitive_line[self.sensitive_info_listbox.get(self.sensitive_info_listbox.curselection())]
		except (KeyError,AttributeError,UnboundLocalError):
			tkinter.messagebox.showinfo(r'提示','该行没有敏感域关键字。')
			return
		getxml = GetXML()																			#实例化一个GetXML对象，用来处理XML文件
		root = getxml.Read(global_variable.ath_MeaningForKeywordxml)
		for field in root.iter('Field'):
			if keyword == field.attrib['name']:
				tkinter.messagebox.showinfo(r'说明','域命名：' +field.attrib['name'] + '\n' + '域序号：' +field.find('id').text + '\n' + '域描述：' +field.find('description').text)
				matching_flag = True
		if not matching_flag:
			tkinter.messagebox.showinfo(r'提示','该行的关键字是：['+ keyword + '],不属于敏感报文域')

	def SearchInLog(self):
		all_FieldNames = self.keyword_list.get(0.0,END)									#初始化一个变量用来保存当前所有待检查的域命
		all_FieldNames = all_FieldNames.split()

		path_name = self.path.get()																#初始化一个保存当前搜索路径的变量

		try:
			self.all_files=''																	#初始化一个保存所有文件的变量
			self.all_files = self.TraversalFiles(path_name)										#遍历指定路径下的所有文件
		except FileNotFoundError:
			tkinter.messagebox.showinfo('提示','搜索路径为空或者该路径不存在')
		else:
			self.all_files = self.all_files.strip('\n')												#字符串首尾去换行符处理
			files = self.all_files.split('\n')														#以\n为分割符，返回分割后的列表

		
		for a_FieldName in all_FieldNames:
			for a_file in files:
				self.SearchFieldName(a_FieldName,a_file)

		#打印查找状态到界面上
		tmp = '查找完毕！！！'
		self.related_file_name.set(tmp)

	def SearchFieldName(self, a_FieldName, a_file):
		#判断文件是否是txt或者log类型的，如果是就搜索敏感信息，如果不是就进入下一次循环判断下一个文件的类型
		#下面逻辑语句代替：
		#if a_file.endswith('txt') or a_file.endswith('log'):
		if a_file.rfind('.') != -1 and (a_file[a_file.rfind('.')+1:] == 'txt' or a_file[a_file.rfind('.')+1:] == 'log'):

			'''
			#打印文件路径信息到日志里，方便定位敏感信息
			print('\n\n---------------------------',file=open("Sensitive_log.txt", 'a', encoding='utf-8'),end='')
			print(a_file,file=open("Sensitive_log.txt", 'a', encoding='utf-8'),end='')
			print('---------------------------\n\n',file=open("Sensitive_log.txt", 'a', encoding='utf-8'),end='')
			'''

			#打印查找状态到界面上
			tmp = '正在查找：'+a_file
			self.related_file_name.set(tmp)

			#处理文件内容
			with open(a_file,'rb') as f:
				for line in f.readlines():
					try:
						self.SearchFieldNameInLine(a_FieldName,str(line,'utf-8','ignore'))
					except re.error:
						tkinter.messagebox.showinfo('提示','关键字不符合正则表达式规则，如[,需要转义才符合规则，转义后为\[')
						tmp = '注意关键字格式，请更新关键字！！！'
						self.related_file_name.set(tmp)
						return

	def SearchFieldNameInLine(self,a_FieldName,line):
		if re.search(a_FieldName, line, re.I):
				#print(line,file=open("Sensitive_log_02.txt", 'a', encoding='utf-8'))
				#self.sensitive_info_listbox.insert(END, line)									#插入文本行到应用界面列表框里
				self.lines.append(line)
				self.root.update()																#实时更新界面信息

	def HandlerAdaptor(self,fun, **kwds):
		'用于给事件绑定函数传参的中间适配函数'
		return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)

	def Locate_Keyword_In_Result(self, event, tag_name, keyword_listbox):
		#将选中的关键字在Text里Index保存在coordinate中
		coordinate = keyword_listbox.tag_ranges(tag_name)
		#获取选定的关键字值
		keyword_value = keyword_listbox.get(coordinate[0],coordinate[1])
		if keyword_value.find(':') != -1:
			keyword_value = keyword_value.partition(':')[2]
		line_index = self.keyword_line_dict[keyword_value]
		if line_index == None:
			tkinter.messagebox.showinfo('提示','没有包含该关键字的日志记录')
		else:
			self.sensitive_info_listbox.see('{line_index}.0'.format(line_index = line_index))
		
	def Locate_Line_In_log(self, event, tag_name, keyword_listbox):
		#将选中的关键字在Text里Index保存在coordinate中
		coordinate = keyword_listbox.tag_ranges(tag_name)
		#获取选定的关键字值
		line_value = keyword_listbox.get(coordinate[0],coordinate[1])

		for a_line_detail in self.all_line_details:
			if line_value.strip() == a_line_detail[2].strip():
				try:
					win32api.ShellExecute(0,'open','notepad++.exe','{file} -n{index}'.format(file=a_line_detail[0],index=a_line_detail[1]),'',1)
				except:
					tkinter.messagebox.showinfo('提示','请先安装notepad++')
				return
	
	def OpenThisFile(self, event, tag_name, keyword_listbox):
		'listbox控件绑定的回调函数，默认参数event不可少,功能是打开改行信息所在的源文件'
		#将选中的关键字在Text里Index保存在coordinate中
		coordinate = keyword_listbox.tag_ranges(tag_name)
		#获取选定的关键字值
		line_value = keyword_listbox.get(coordinate[0],coordinate[1])
		try:
			file = self.sensitive_line_source[line_value]
			os.startfile(file)
		except (KeyError,UnboundLocalError):
			tkinter.messagebox.showinfo('提示','该行无源文件')	