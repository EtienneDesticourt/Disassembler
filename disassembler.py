from portable_executable import PortableExecutable

if __name__ == '__main__':
	with open("main.exe", "rb") as f:
	    data = f.read()

	parser = PortableExecutable()
	parser.parse(data)
