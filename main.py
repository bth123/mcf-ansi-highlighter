import re
from json import loads


class Highlighter:
	class Database:
		with open("database.json", "r", encoding="utf-8") as db:
			database_content = loads(db.read())
		color_codes = database_content["color_codes"]
		commands = database_content["commands"]
		regexes = {
			"nbt": r"""(\$\([a-zA-Z0-9_-]*\)|string[0-9]+|[a-zA-Z_]\w*|[0-9]+[a-zA-Z]?|[\[\]{},:;])""",
			"string": r"""(?<!\\)(?:"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\')""",
			"macro": r"\$\([a-zA-Z0-9_-]*\)"
		}
		root_command = ""

	def highlight(function):
		highlighted = ""
		function = function.replace("\\\n", "\\newline")
		function = function.split("\n")
		for command in function:
			highlighted += f"{Highlighter.line(command)}\n"
		return highlighted

	def line(command):
		# Shortcuts
		colors = Highlighter.Database.color_codes
		commands = Highlighter.Database.commands
		# Main
		raw_command = command.lstrip()
		tabs_count = len(command) - len(raw_command)
		# Comment check
		if raw_command == "":
			return raw_command
		elif raw_command[0] == "#":
			if raw_command[1] in "#>":
				return " "*tabs_count + colors["comment"] + "#>" + colors["link-comment"] + raw_command[2:]
			else:
				return f"{' '*tabs_count}{colors['comment']}{raw_command}"
		# Command highlight
		command = Highlighter.split(raw_command)
		highlighted = []
		for element in command:
			if (raw_root := element.replace("$", "").replace("\\newline", "")) in commands:
				highlighted.append(colors["command"]+element)
				Highlighter.root_command = raw_root
			elif Highlighter.root_command != "" and element.replace("\\", "") in commands[Highlighter.root_command]["subcommands"]:
				highlighted.append(colors["subcommand"]+element)
			elif element[0] == "@":
				highlighted.append(Highlighter.target(element))
			elif element[0] in "#%&":
				highlighted.append(colors["selector"]+element)
			elif element[0] == "{":
				highlighted.append(Highlighter.nbt(element))
			elif ":" in element:
				highlighted.append(colors["path"]+element)
			elif element.isdigit():
				highlighted.append(colors["number"]+element)
			elif element[:-2] == "$(":
				highlighted.append(colors["macro"]+"$"+colors["bracket0"]+"["+colors["argument"]+element[2:-1]+colors["bracket0"]+"]")
			else:
				highlighted.append(colors["argument"]+element)
		return f"{' ' * tabs_count}{' '.join(highlighted)}".replace("newline", f"{colors['backslash']}\\\n")

	def split(command):
		command += " "
		command_elements = []
		strings = []
		brackets_count = 0
		current_element = ""
		for index, char in enumerate(command):
			if len(strings) >= 1:
				if char == strings[-1] and command[index-1] != "\\":
					strings.pop(-1)
				current_element += char
			elif char in "\"'":
				strings.append(char)
				current_element += char
			elif char in "{[":
				brackets_count += 1
				current_element += char
			elif char in "]}":
				brackets_count -= 1
				current_element += char
			elif char == " " and brackets_count == 0:
				command_elements.append(current_element)
				current_element = ""
			else:
				current_element += char
		return command_elements

	def target(selector):
		# Shortcuts
		colors = Highlighter.Database.color_codes
		# Main
		tag = ""
		if "nbt" in selector:
			# States
			brackets_count = 0
			nbts = []
			curr_tag = ""
			for char in selector:
				if char == "{":
					brackets_count += 1
					curr_tag += char
				elif char == "}":
					brackets_count -= 1
					curr_tag += char
					if brackets_count == 0:
						selector = selector.replace(curr_tag, f"%%%%nbt{len(nbts)}%%%%")
						nbts.append(curr_tag)
						curr_tag = ""
				elif brackets_count >= 1:
					curr_tag += char
		highlighted = colors["selector"]+selector.replace("[", f"{colors['bracket0']}[{colors['key']}").replace("]", f"{colors['bracket0']}]")\
			.replace("=", f"{colors['delimiter']}={colors['value']}").replace(",", f"{colors['delimiter']},{colors['key']}")\
				.replace("!", f"{colors['delimiter']}!{colors['value']}").replace("..", f"{colors['bracket1']}..{colors['value']}")\
					.replace("#", f"{colors['selector']}#").replace("{", colors['bracket1']+"{"+colors['key'])\
					.replace("}", colors['bracket1']+"}"+colors['value'])
		if "nbts" in locals():
			for index, tag in enumerate(nbts):
				highlighted = highlighted.replace(f"%%%%nbt{index}%%%%", Highlighter.nbt(tag, brackets_depth=0))
		return highlighted

	def nbt(tag, brackets_depth=-1):
		colors = Highlighter.Database.color_codes
		# Strings are highlighted separately bc they has really hard regex and idk
		# if there a way to put it into nbt regex
		string_re = Highlighter.Database.regexes["string"]
		strings = re.findall(string_re, tag)
		for index, string in enumerate(strings):
			tag = tag.replace(string, f"string{index}")
		def lexer(tag, brackets_depth):
			tokens = []
			nbt_re = Highlighter.Database.regexes["nbt"]
			for match in re.finditer(nbt_re, tag):
				token = match.group()
				if token[0] in "1234567890" or token in "BIL":
					tokens.append((token, "value"))
				elif token[:6] == "string":
					tokens.append((token, "string"))
				elif token in "[{":
					brackets_depth += 1
					brackets_depth %= 3
					tokens.append((token, f"bracket{brackets_depth}"))
				elif token in "}]":
					tokens.append((token, f"bracket{brackets_depth}"))
					brackets_depth -= 1
					brackets_depth %= 3
				elif token in ':,;':
					tokens.append((token, "delimiter"))
				elif token[:2] == "$(":
					tokens.append((token, f"bracket{(brackets_depth + 1) % 3}"))
				else:
					tokens.append((token, "key"))
			return tokens
		lexed = lexer(tag, brackets_depth)
		highlighted = ""
		for token, type in lexed:
			if token[:2] == "$(":
				highlighted += f"{colors['macro']}${colors[type]}({colors['argument']}{token[2:-1]}{colors[type]})"
			elif type == "string":
				highlighted += f"{colors['str_value']}{strings[int(token.replace('string', ''))]}"
			else:
				highlighted += colors[type] + token
				if type == "delimiter":
					highlighted += " "
		return highlighted

