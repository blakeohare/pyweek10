import os


root = 'source'
main = root + os.sep + 'main.py'
imports = root + os.sep + 'imports.py'
functions = root + os.sep + 'functions.py'

exclude = [main, imports]

def read_file(path):
	c = open(path, 'rt')
	t = c.read()
	c.close()
	return t

def get_files(folder):
	text = ''
	static = ''
	for file in os.listdir(folder):
		path = folder + os.sep + file
		header = "\n\n########################\n## " + path + "\n" + "########################\n"
		static_header = "\n\n########################\n## " + path + " (static)\n" + "########################\n"
		if not (path in exclude):
			if os.path.isdir(path):
				folder_code = get_files(path)
				text += folder_code[0]
				static += folder_code[1]
			elif path.endswith('.py'):
				t = read_file(path)
				parts = t.split('#STATIC')
				text += header + parts[0] + "\n"
				if len(parts) > 1:
					static += static_header + parts[1]
		
	return (text, static)

code = get_files(root)

code = code[0] + "\n" + code[1]



code = read_file(imports) + "\n" + code
code += "\n# handy functions\n" + read_file(functions) + "\n"
code += ("#" * 20) + "\n# main.py\n" + ("#" * 20) + read_file(main)

c = open('run.py', 'wt')
c.write(code)
c.close()
