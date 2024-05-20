from json import loads
from re import MULTILINE, findall, match, search, sub


# I use  btw (You can only see it if you too hehe)
# 19.05.24
class Hl:
    class Database:
        with open("database.json", "r", encoding="utf-8") as db:
            database_content = loads(db.read())
        color_codes = database_content["color_codes"]
        commands = database_content["commands"]
        color_classes = database_content["color_classes"]

    def lex(func):
        def reset_token():
            nonlocal curr_token, curr_type, tokens, clear_tokens
            tokens.append((curr_token, curr_type))
            if curr_token not in " \\\t\n":
                clear_tokens.append(curr_token)

        def switch_mode(mode):
            nonlocal history
            if mode == "back":
                history.pop(-1)
            else:
                history.append(mode)

        tokens = []
        clear_tokens = []
        history = ["normal"]
        string_type = ""
        nbt_type = ""
        curr_token = ""
        curr_type = "text"

        # Циганські фокуси
        for idx, char in enumerate(func):
            next_char = func[idx + 1 : idx + 2]
            prev_char = func[idx - 1 : idx - 2]
            if history[-1] == "normal":
                # " \\\t\n#[{\"'$"
                if char in " \\\t\n":
                    reset_token()
                    curr_type = "none"
                elif char == "#":
                    pass
                elif char == "[":
                    if tokens[-1][0][0] == "@":
                        switch_mode("filter")
                        curr_type = "bracket"
                    else:
                        switch_mode(
                            ""
                        )  # I have no clue how to separate nbt array from cmponent

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
        #
        for index, token in enumerate(tokens):
            prev_tokens = tokens[index::-1]
            fut_tokens = tokens[index + 1 :]
            clear_index += 1 if token not in " \\\n\t" else 0
            prev_clear_tokens = clear_tokens[clear_index - 2 :: -1]
            if token[0] == "\u200b":
                token = token[1:]
                comment_content = sub(r"^\s*#(#|>)?", "", token, flags=MULTILINE)
                edited_content = comment_content[:]
                if token[1] in "#>":
                    comment_type = "link-comment"
                else:
                    comment_type = "comment"
                # path and @this stuff
                pathes = findall(r"#[a-zA-z_\-]+:[a-zA-z_\-/]", comment_content)
                decaorator_maybe_idkhonestly = findall(r"@\w+", comment_content)
                for path in pathes:
                    edited_content = comment_content.replace(
                        path, colors["path"] + path + colors[comment_type]
                    )
                for i in decaorator_maybe_idkhonestly:
                    edited_content = edited_content.replace(
                        i, colors["subcommand"] + i + colors[comment_type]
                    )
                #
                highlighted += (
                    colors["comment"]
                    + token.replace(comment_content, "")
                    + (colors[comment_type] if comment_type == "link-comment" else "")
                    + edited_content
                )
            elif (
                token in possible_subcommands
                and bracket_index <= 0
                and prev_clear_tokens[0] != "run"
            ):
                highlighted += colors["subcommand"] + token
            elif (
                raw_command := token.replace("$", "")
            ) in commands and bracket_index <= 0:
                highlighted += (
                    (colors["macro_bf_command"] + "$" if "$" in token else "")
                    + colors["command"]
                    + raw_command
                )
                possible_subcommands = commands[raw_command]["subcommands"]
            elif token[0] in "\"'":
                # Highlighting macros
                macros = findall(r"\$\([0-9A-z-_\.]+\)", token)
                for macro in macros:
                    token = token.replace(
                        macro,
                        macro.replace("$", colors["macro"] + "$")
                        .replace(
                            "(",
                            colors[f"bracket{bracket_index}"] + "(" + colors["text"],
                        )
                        .replace(
                            ")",
                            colors[f"bracket{bracket_index}"] + ")" + colors["string"],
                        ),
                    )
                #
                highlighted += colors["string"] + token
            elif token == "..":
                highlighted += colors["range"] + token
            elif ":" in token and token != ":" and prev_clear_tokens[0] not in "[,":
                highlighted += colors["path"] + token
            elif (
                token[0] in "@#$%."
                and len(token) > 1
                and token[1] != "("
                and prev_tokens[0] != "]"
            ):
                highlighted += colors["selector"] + token
            elif token in ":;=,":
                highlighted += colors["separator"] + token
            elif token == "/" and fut_tokens[0] in commands:
                highlighted += colors["macro_bf_command"] + token
            elif token in "[{(":
                highlighted += colors[f"bracket{bracket_index%3}"] + token
                bracket_index += 1
            elif token in ")}]":
                bracket_index -= 1
                highlighted += colors[f"bracket{bracket_index%3}"] + token
            elif match(
                r"^(~-?[0-9]*\.?[0-9]*|\^-?[0-9]*\.?[0-9]*|-?[0-9]+\.?[0-9]*[bsdf]?|-?\.?[0-9]+[bsdf]?)$",
                token,
            ):
                highlighted += colors["number"] + token
            elif match(r"\$\([0-9A-z-_\.]+\)", token):
                highlighted += f"{colors['macro']}${colors[f'bracket{bracket_index}']}({colors['text']}{token[2:-1]}{colors[f'bracket{bracket_index}']})"
            elif token == "\\":
                highlighted += colors["backslash"] + token
            elif token in " \t\n":
                highlighted += token
            else:
                text_type = "text"
                if bracket_index > 0:
                    text_type = "key"
                    if prev_clear_tokens[0] in ":=":
                        text_type = "value"
                highlighted += colors[text_type] + token
        return Hl.optimize_len(highlighted)

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
