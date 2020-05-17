#将自定义包的路径加入sys.path
import sys
import os

#获取包或模块所在的路径
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
path_foo = os.path.join(path,'foo')
path_GUI = os.path.join(path_foo, 'GUI')
path_lib = os.path.join(path_foo, 'lib')
path_global = os.path.join(path_foo, 'global')

path_list = [path_foo, path_GUI, path_lib, path_global]


for a_path in path_list:
	sys.path.append(a_path)

