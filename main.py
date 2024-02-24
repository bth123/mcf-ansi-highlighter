from re import match, findall
from json import loads
from string import ascii_letters

class Hl:
	class Database:
		with open("database.json", "r", encoding="utf-8") as db:
			database_content = loads(db.read())
		color_codes = database_content["color_codes"]
		commands = database_content["commands"]

	def lex(func):
		state = {
			"mode": "normal",
			"history": ["normal"],
			"string_type": "",
			"is_macro": "",
			"nbt_type": "",
		}
		def reset_token(need_to_append_char=False):
			nonlocal tokens, curr_token
			tokens.append(curr_token) if curr_token != "" else None
			if need_to_append_char:
				tokens.append(char)
			curr_token = ""
		def switch_mode(mode):
			if mode == "back":
				state["history"].pop(-1)
				state["mode"] = state["history"][-1]
			else:
				state["mode"] = mode
				state["history"].append(mode)
		# Setting up vars
		closed_bracktes = {"{":"}", "[":"]"}
		tokens = []
		curr_token = ""
		# Magec
		for idx, char in enumerate(func):
			next_char = func[idx+1:idx+2]
			prev_char = func[idx-1]
			if state["mode"] == "normal":
				if char not in " \t#[]{}\"'$)\\\n":
					curr_token += char
				else:
					need_to_append_char = True
					need_to_reset = True
					if char in "{[":
						if "@" in curr_token:
							switch_mode("filter")
						else:
							opened_brackets = 1
							switch_mode("nbt")
							state["nbt_type"] = char
					elif char == "$":
						need_to_reset = False
						if next_char == "(":
							switch_mode("macro")
							reset_token()
						curr_token += char
					elif char in "\"'":
						switch_mode("string")
						state["string_type"] = char
						curr_token += char
						need_to_reset = False
					elif char == "#" and prev_char == "\n" or idx == 0:
						switch_mode("comment")
						reset_token()
						curr_token = char
						need_to_reset = False
					if need_to_reset:
						reset_token(need_to_append_char)
			elif state["mode"] == "filter":
				if char not in " \t{}\"']$)\\\n=,.":
					curr_token += char
				else:
					need_to_append_char = True
					need_to_reset = True
					if char == "]":
						switch_mode("back")
					elif char == "{":
						if tokens[-2] == "nbt":
							opened_brackets = 1
							switch_mode("nbt")
							state["nbt_type"] = char
					elif char in "\"'":
						switch_mode("string")
						state["string_type"] = char
						curr_token += char
						need_to_reset = False
					elif char == ".":
						if curr_token == char:
							curr_token += char
						else:
							if next_char == char:
								reset_token()
								curr_token = char
								need_to_reset = False
							else:
								curr_token += char
								need_to_reset = False
						need_to_append_char = False
					elif char == "$":
						need_to_reset = False
						if next_char == "(":
							switch_mode("macro")
							reset_token()
						curr_token += char
					elif char == ")":
						curr_token += char
						need_to_append_char = False
					if need_to_reset:
						reset_token(need_to_append_char)
			elif state["mode"] == "macro":
				curr_token += char
				if char == ")":
					switch_mode("back")
					reset_token()
			elif state["mode"] == "nbt":
				if char not in " \t[]{}\"'$)\\\n;:,=":
					curr_token += char
				else:
					need_to_append_char = True
					need_to_reset = True
					if char in "\"'":
						switch_mode("string")
						state["string_type"] = char
						curr_token += char
						need_to_append_char = False; need_to_reset = False
					elif char == "$":
						need_to_reset = False
						if next_char == "(":
							switch_mode("macro")
							reset_token()
						curr_token += char
					elif char == ")":
						curr_token += char
						need_to_append_char = False
					if need_to_reset:
						reset_token(need_to_append_char)
				# Exiting nbt stte if it closed
				if char == state["nbt_type"]:
					opened_brackets += 1
				elif char == closed_bracktes[state["nbt_type"]]:
					opened_brackets -= 1
					if opened_brackets == 0:
						switch_mode("back")
			elif state["mode"] == "string":
				curr_token += char
				if char == state["string_type"] and curr_token[-1] != "\\":
					switch_mode("back")
					reset_token()
			elif state["mode"] == "comment":
				curr_token += char
				if char == "\n":
					switch_mode("back")
					reset_token()
			if idx+1 == len(func) and curr_token != "":
				tokens.append(curr_token)
				break
		return tokens

	def highlight(func):
		# Shotcuts
		colors = Hl.Database.color_codes
		commands = Hl.Database.commands
		# Setting up vars
		commands_count = 0
		possible_subcommands = []
		bracket_index = 0
		highlighted = ""
		# Магія ✨
		tokens = Hl.lex(func)
		for index, token in enumerate(tokens):
			prev_tokens = tokens[index-1::-1]
			fut_tokens = tokens[index+1:]
			if token.startswith("#"):
				if (comment_content:=token.lstrip(" \t#>")) != token.lstrip(" \t#"):
					highlighted += colors["link-comment"] + token.replace(comment_content, "") + colors["comment"] + comment_content
				else:
					highlighted += colors["comment"] + token
			elif (raw_command:=token.replace("$", "")) in commands and bracket_index <= 0:
				if raw_command != "execute":
					possible_subcommands = []
				highlighted += (colors["macro"]+"$" if "$" in token else "") + colors["command"] + raw_command
				possible_subcommands += commands[raw_command]["subcommands"]
			elif token in possible_subcommands and bracket_index <= 0:
				highlighted += colors["subcommand"] + token
			elif token == "..":
				highlighted += colors["command"] + token
			elif token[0] in "@#$%." and token[1] != "(":
				highlighted += colors["selector"] + token
			elif ":" in token and token != ":":
				highlighted += colors["path"] + token
			elif token in "[{(":
				highlighted += colors[f"bracket{bracket_index%3}"] + token
				bracket_index += 1
			elif token in ")}]":
				bracket_index -= 1
				highlighted += colors[f"bracket{bracket_index%3}"] + token
			elif token[0] in "\"'":
				# Cehcking if this string in json
				is_json = []
				for pt in prev_tokens:
					if pt in " \\\t\n": pass
					elif pt == ":" and is_json == []:
						is_json.append(pt)
					elif pt[0] in "\"'":
						is_json = True
						break
					else:
						is_json = False
						break
				is_json2 = []
				for ft in fut_tokens:
					if ft in " \\\t\n": pass
					elif ft == ":" and is_json2 == []:
						is_json2.append(ft)
					elif ft[0] in "\"'":
						is_json2 = True
						break
					else:
						is_json2 = False
						break
				if is_json or is_json2:
					string_type = "json-string"
				else:
					string_type = "string"
				# Highlighting macros
				macros = findall(r"\$\([0-9A-z-_\.]+\)", token)
				for macro in macros:
					token = token.replace(macro, macro.replace("$", colors["macro"]+"$")\
					.replace("(", colors[f"bracket{bracket_index}"]+"("+colors["text"])\
					.replace(")", colors[f"bracket{bracket_index}"]+")"+colors[string_type]))
				#
				highlighted += colors[string_type] + token
			elif token in ":;=,":
				highlighted += colors["separator"] + token
			elif match(r"~[0-9]*\.?[0-9]*|\^[0-9]*\.?[0-9]*|[0-9]+\.?[0-9]*[bsdf]?|\.?[0-9]+[bsdf]?", token):
				highlighted += colors["number"] + token
			elif match(r"\$\([0-9A-z-_\.]+\)", token):
				highlighted += f"{colors['macro']}${colors[f'bracket{bracket_index}']}({colors['text']}{token[2:-1]}{colors[f'bracket{bracket_index}']})"
			elif token == "\\":
				highlighted += colors["backslash"] + token
			elif token in " \t\n":
				highlighted += token
			else:
				highlighted += colors["text" if bracket_index <= 0 else "key"] + token
		return highlighted


print(Hl.highlight("""summon text_display ~ ~ ~ {text:'{"score":{"name":"$dmg","objective":"var"},"color":"red"}',background:0,billboard:"center",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.25f,1.25f,1.25f]},Tags:["damage","temp"]}

execute as @e[type=text_display,tag=damage,tag=temp] run {
   tag @s remove temp

   data merge entity @s {start_interpolation:0,interpolation_duration:40,transformation:{translation:[0.0f,1.0f,0.0f]}}

   scoreboard players set @s life.time 20
}"""))