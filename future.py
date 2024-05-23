from json import loads
from re import MULTILINE, findall, match, search, sub


# I use  btw (You can only see it if you too hehe)
# 23.05.24
class Hl:
    class Database:
        with open("database.json", "r", encoding="utf-8") as db:
            database_content = loads(db.read())
        color_codes = database_content["color_codes"]
        commands = database_content["commands"]
        color_classes = database_content["color_classes"]

    def lex(func):

        def switch_mode(mode):
            nonlocal history
            if mode == "back":
                history.pop(-1)
            else:
                history.append(mode)

        lines = func.split("\n")
        tokens = []
        clear_tokens = []
        history = ["normal"]
        string_type = ""
        bracket_count = 0
        nbt_type = ""
        curr_token = ""
        curr_type = "text"
        curr_line_idx = 0

        # Циганські фокуси
        for idx, char in enumerate(func):
            need_to_reset = True
            need_to_append_char = True
            next_char = func[idx + 1 : idx + 2]
            prev_char = func[idx - 1 : idx - 2]
            curr_line_idx += 1 if char == "\n" else 0
            #
            if history[-1] == "normal":
                # " \\\t\n#[{\"'$"
                if char in " \\\t\n":
                    curr_type = "none"
                elif char == "#":
                    if lines[curr_line_idx].lstrip()[0] == char:
                        switch_mode("comment")
                        new_type = "comment"
                elif char == "[":
                    new_type = "brakcet"
                    if tokens[-1][0][0] == "@":
                        switch_mode("filter")
                    else:
                        if "=" not in func[idx:].split("]")[0].split("\"")[0].split(",")[0]:
                            switch_mode("array")
                            new_type = "bracket"
                            nbt_type = char
                            bracket_count = 1
                        else:
                            switch_mode("component")
                elif char == "{":
                    switch_mode("compound")
                    new_type = "bracket"
                elif char in "\"'":
                    switch_mode("string")
                    new_type = "string"
                elif char == "$" and next_char == "(":
                    switch_mode("macro")
                    new_type = "macro"
            if need_to_reset:
                tokens.append((curr_token, curr_type))
                if curr_token not in " \t\n":
                   clear_tokens.append(curr_token) 
                if need_to_append_char:
                    tokens.append((char, new_type))
                    new_type = "none"

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

    def highlight(func, theme="default"):
        # Shotcuts
        colors = Hl.Database.color_codes if theme == "default" else theme
        commands = Hl.Database.commands
        # Setting up vars
        possible_subcommands = []
        bracket_index = 0
        highlighted = ""
        # Магія ✨
        lexed = Hl.lex(func)
        tokens = lexed[0]
        clear_tokens = lexed[1]
        clear_tokens.append("")
        clear_index = 0
    
    def ansi2html(function):
        color_classes = Hl.Database.color_classes
        ansi_codes_re = r"(([30][0-7]?)(;(4[0-7]))?m)"
        converted = ""
        function_elements = function.replace("\n", "<br>").split("\u001b[")[1:]
        for element in function_elements:
            matches = search(ansi_codes_re, element)
            converted += f'<span class="ansi_{color_classes[matches.group(2)]}{" "+color_classes[matches.group(4)] if matches.group(4) != None else ""}">{element.replace(matches.group(1), "")}</span>'
        return f"<pre>{converted}</pre>"


print(Hl.highlight("""execute summon shulker run summon husk ~ ~ ~"""))
