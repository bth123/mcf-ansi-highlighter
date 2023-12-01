# import database
import re
from json import loads


class Highlighter:
	class Database:
		with open("database.json", "r", encoding="utf-8") as db:
			database_content = loads(db.read())
		color_codes = database_content["color_codes"]
		commands = database_content["commands"]
		regexes = {
			"nbt": r'(\$\([a-zA-Z0-9_-]*\)|"[^"]*"|\'[^\']*\'|[a-zA-Z_]\w*|[0-9]+[a-zA-Z]?|[\[\]{},:;])',
			"macro": r"\$\([a-zA-Z0-9_-]*\)"
		}

	def highlight(function):
		highlighted = ""
		function = function.split("\n")
		for command in function:
			highlighted += f"{Highlighter.command(command)}\n"
		return highlighted

	def command(command):
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
			if raw_command[1] == ">":
				return " "*tabs_count + colors["comment"] + "#>" + colors["link-comment"] + raw_command[2:]
			else:
				return f"{' '*tabs_count}{colors['comment']}{raw_command}"
		# Command highlight
		command = Highlighter.split(raw_command)
		highlighted = []
		for element in command:
			if (raw_root := element.replace("$", "")) in commands:
				highlighted.append(colors["command"]+element)
				Highlighter.root_command = raw_root
			elif element in commands[Highlighter.root_command]["subcommands"]:
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
			else:
				highlighted.append(colors["argument"]+element)
			if element[:-2] == "$(":
				highlighted.append(colors["macro"]+"$"+colors["bracket0"]+"["+colors["argument"]+element[2:-1]+colors["bracket0"]+"]")
		return f"{' ' * tabs_count}{' '.join(highlighted)}"

	def macro(element, prev_color):
		colors = Highlighter.Database.color_codes
		highlighted = ""
		for index, symbol in enumerate(element):
			if symbol == "$":
				highlighted += colors["macro"] + symbol
			elif symbol in "()":
				highlighted += colors[f"bracket{brackets_depth}"] + symbol
				if symbol == ")" and element[idnex+1:index+2] not in "$":
					highlighted += colors[prev_color]
			else:
				highlighted += symbol

	def split(command):
		command += " "
		command_elements = []
		brackets_count = 0
		current_element = ""
		for char in command:
			if char in "{[":
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
		highlighted = colors["selector"]+selector.replace("[", f"{colors['bracket1']}[{colors['key']}").replace("]", f"{colors['bracket1']}]")\
			.replace("=", f"{colors['delimiter']}={colors['value']}").replace(",", f"{colors['delimiter']},{colors['key']}")\
				.replace("!", f"{colors['bracket2']}!{colors['value']}").replace("..", f"{colors['bracket2']}..{colors['value']}")\
					.replace("#", f"{colors['selector']}#").replace("{", colors['bracket2']+"{"+colors['key'])\
					.replace("}", colors['bracket2']+"}"+colors['value'])
		if "nbts" in locals():
			for index, tag in enumerate(nbts):
				highlighted = highlighted.replace(f"%%%%nbt{index}%%%%", Highlighter.nbt(tag, brackets_depth=0))
		return highlighted

	def nbt(tag, brackets_depth=-1):
		colors = Highlighter.Database.color_codes
		def lexer(tag, brackets_depth):
			tokens = []
			regex = Highlighter.Database.regexes["nbt"]
			for match in re.finditer(regex, tag):
				token = match.group(1)
				if token.lstrip()[0] in "\"'":
					tokens.append((token, "str_value"))
				elif token[0] in "1234567890" or token in "BIL":
					tokens.append((token, "value"))
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
			if token[0] == "$":
				highlighted += colors["macro"]+"$"+colors[type]+"("+colors["argument"]+token[2:-1]+colors[type]+")"
			else:
				highlighted += colors[type] + token
				if type == "delimiter":
					highlighted += " "
		return highlighted

a = "$data $(macro_yeaah) entity @s[type=armor_stand] {Invisible: 1b, ArmorItems:[{},{},{},{id:\"emerald_block\", Count:$(another_cool-macr0)}],NoGravity:1b,NoBasePlate:1b}"
# print(Highlighter.nbt("{Invisible: 1b, ArmorItems:[{},{},{},{id:\"emerald_block\", Count:$(another_cool-macr0)}],NoGravity:1b,NoBasePlate:1b}"))
# print(Highlighter.highlight("say @a[scores={kills=5,deaths=20..}]"))
# print(Highlighter.target("@e[type=pig]"))
print(Highlighter.highlight(a))
# print(Highlighter.split(a))
