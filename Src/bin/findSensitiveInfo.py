import os
import script
import main


if __name__ == '__main__':

	if os.path.exists('Sensitive_log_01.txt'):
		os.remove('Sensitive_log_01.txt')
	if os.path.exists('Sensitive_log_02.txt'):
		os.remove('Sensitive_log_02.txt')
	main.main()

