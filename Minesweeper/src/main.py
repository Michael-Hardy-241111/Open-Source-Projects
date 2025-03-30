import sys
from cli import start_cli
from gui import start_gui

if __name__ == "__main__":
	if "-cli" in sys.argv:
		start_cli()
	else:
		#start_gui()
		pass
