from json import loads
from re import MULTILINE, findall, match, search, sub


# I use  btw (You can only see it if you too hehe)
# 23.05.24



def optimize_len(func):
	optimized = ""
	ansi_codes_re = r"(\[([0-5];)?[034][0-7]?m){1,2}"
	splitted = func.split("\u001b")
	#
	prev_color = splitted[0].split("m")[0] + "m"
	for element in splitted[1:]:
		matches = search(ansi_codes_re, element)
		optimized += (
			"\u001b" + element
			if prev_color != matches.group(0)
			else element.replace(prev_color, "")
		)
		prev_color = matches.group(0)
	return optimized

def ansi2html(function):
	color_classes = Hl.Database.color_classes
	ansi_codes_re = r"(([30][0-7]?)(;(4[0-7]))?m)"
	converted = ""
	function_elements = function.replace("\n", "<br>").split("\u001b[")[1:]
	for element in function_elements:
		matches = search(ansi_codes_re, element)
		converted += f'<span class="ansi_{color_classes[matches.group(2)]}{" "+color_classes[matches.group(4)] if matches.group(4) != None else ""}">{element.replace(matches.group(1), "")}</span>'
	return f"<pre>{converted}</pre>"


