from pathlib import Path
import json, argparse

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'goto.json'
PATHFILE_PATH = Path(__file__).resolve().parent / 'data' / 'path.txt'

class InvalidUsage(Exception):
	def print(self):
		message = " ".join(self.args)
		message += "\n(Use -h for help)"
		print("\033[31m" + message + '\033[39m')

def load_settings():
	try:
		with open(str(DATA_PATH), 'r') as f:
			return json.load(f)
	except FileNotFoundError:
		return {}

def write_settings(data):
	with open(str(DATA_PATH), 'w') as f:
		json.dump(data, f)

settings = load_settings()

def goto_path(name):
	path = settings.get(name, None)
	if path is None:
		raise InvalidUsage("The path name", name, "doesn't exists")
	with open(str(PATHFILE_PATH), 'w') as f:
		f.write(path)

def list_paths():
	print("PATHS LIST:")
	for name, path in settings.items():
		print(name, "  ---->  ", path)

def add_path(name):
	path = str(Path('.').resolve())
	settings[name] = path
	write_settings(settings)
	print("Added", name, " -> ", path)

def remove_path(name):
	if not name in settings:
		path = str(Path(name).resolve())
		for name2 in settings:
			if settings[name2] == path:
				name = name2
				break
	if not name in settings:
		raise InvalidUsage("Found not path named", name)

	path = settings[name]
	del settings[name]
	write_settings(settings)
	print("Removed", name, " -> ", path)

def parse_arguments():
	parser = argparse.ArgumentParser(description='Goto to a favorite folder')
	g = parser.add_mutually_exclusive_group()
	g.add_argument('dest', metavar='DESTINATION_NAME', help='The name of the path where you want to go', default=None, nargs='?')
	g.add_argument('-a', '--add', metavar='NEW_PATH_NAME', default=None, help="Add this path to favorites with the given name")
	g.add_argument('-d', '--delete', metavar='PATH_NAME', default=None, help="Add this path to favorites with the given name")
	g.add_argument('-l', '--list', dest='list', action='store_const', const=True, default=False, help='Print the list of all favorites')
	g.add_argument('-c', dest='complete', action='store_const', const=True, default=False, help=argparse.SUPPRESS)

	return parser.parse_args()

def complete_print():
	print(*settings.keys())

def main():
	"""
	You should add this to your .bashrc / .zhrc :

	goto () {
		python3 "/path/to/scripts/goto.py" "$@"
		cd "$(cat /path/to/scripts/data/path.txt)"
	}
	_goto_completions()
	{
	  COMPREPLY=($(compgen -W "$(python3 /path/to/scripts/goto.py -c)" "${COMP_WORDS[1]}"))
	}
	complete -F _goto_completions goto
	"""
	args = parse_arguments()
	if args.complete:
		return complete_print()

	with open(str(PATHFILE_PATH), 'w') as f:
		f.write('.')

	args = parse_arguments()
	if args.dest is not None:
		goto_path(args.dest)
	elif args.list:
		list_paths()
	elif args.add is not None:
		add_path(args.add)
	elif args.delete is not None:
		remove_path(args.delete)
	else:
		raise InvalidUsage("You must give an argument to the command")
		exit(1)

if __name__ == '__main__':
	try:
		main()
	except InvalidUsage as e:
		e.print()