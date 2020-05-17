import os

path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(path, 'conf')

#以下变量为全局变量
path_Keywordini = os.path.join(path, 'Keyword.ini')
path_IdcardInfoxml = os.path.join(path, 'IdcardInfo.xml')
path_MeaningForKeywordxml = os.path.join(path, 'MeaningForKeyword.xml')

