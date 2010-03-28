def max(a, b):
	if a > b:
		return a
	return b

def min(a, b):
	if a < b:
		return a
	return b

def ensure_range(x, lower, upper):
	return max(lower, min(upper, x))

def trim(string):
	if string == None or string == '':
		return ''
	
	whitespace = ' \n\r\t'
	index = 0
	while index < len(string):
		if string[index] in whitespace:
			index += 1
		else:
			break
	string = string[index:]
	
	index = len(string) - 1
	while index > 0:
		if string[index] in whitespace:
			index -= 1
		else:
			break
	
	string = string[:index + 1]
	return string
