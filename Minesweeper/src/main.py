import sys
from cli import start_cli

if __name__ == "__main__":
	if "-cli" in sys.argv:
		start_cli()
	else:
		pass
