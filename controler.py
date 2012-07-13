import sys, os,  tty, termios

class controler:
	def __init__(self, lambda_map):
		pass
		
class kcontroler(controler):
	def __init__(self, lambda_map):
		controler.__init__(self, lambda_map)
	
	def get_next(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		tty.setraw(fd)
		key = sys.stdin.read(1)
		termios.tcsetattr(fd, termios.TCSANOW, old_settings)
	# in raw terminal mode CTRL+C is ASCII code 0x03
	# We exit upon CTRL+C
		if key == ' ':
			termios.tcsetattr(fd, termios.TCSANOW, old_settings)
			os.system("reset")
			sys.exit(0)
		
		if key == "z":
			return "U"
		if key == "s":
			return "D"
		if key == "q":
			return "L"
		if key == "d":
			return "R"
		if key == "a":
			return "A"
		if key == "w":
			return "W"
			
		
