const fs = require('fs');

class Hl {
	static Database = (() => {
		const databaseContent = JSON.parse(fs.readFileSync('database.json', 'utf-8'));
		const { color_codes, commands, color_classes } = databaseContent;
		return { color_codes, commands, color_classes };
	})();

	static lex(func) {
		let state = {
			mode: "normal",
			history: ["normal"],
			string_type: "",
			is_macro: "",
			nbt_type: "",
		};
		let tokens = [];
		var currToken = "";

		const resetToken = (needToAppendChar = false) => {
			// needToAppendChar = needToAppendChar || false
			if (currToken !== null) {
				tokens.push(currToken)
			}
			if (needToAppendChar) {
				tokens.push(char);
			}
			currToken = "";
		};

		const switchMode = (mode) => {
			if (mode === "back") {
				state.history.pop();
				state.mode = state.history[state.history.length - 1];
			} else {
				state.mode = mode;
				state.history.push(mode);
			}
		};

		const closedBrackets = { "{": "}", "[": "]" };

		for (let idx = 0; idx < func.length; idx++) {
			var char = func[idx];
			const nextChar = func.slice(idx + 1, idx + 2);
			const prevChar = func[idx - 1];
			const prevTokens = tokens.slice().reverse();
			const nextChars = func.slice(idx + 1);

			if (state.mode === "normal") {
				if (!" \t#[]{}\"'$)\\\n".includes(char)) {
					currToken += char;
				} else {
					let needToAppendChar = true;
					let needToReset = true;
					if ("{[".includes(char)) {
						if (currToken.includes("@")) {
							switchMode("filter");
						} else {
							var openedBrackets = 1;
							switchMode("nbt");
							state.nbt_type = char;
						}
					} else if (char === "$") {
						needToReset = false;
						if (nextChar === "(") {
							switchMode("macro");
							resetToken();
						}
						currToken += char;
					} else if ("\"'".includes(char)) {
						switchMode("string");
						state.string_type = char;
						currToken += char;
						needToReset = false;
					} else if (char === "#") {
						// let isComment = [true];
						// if (!prevTokens.some(i => i === "\n")) {
						//     isComment = [...prevTokens].map(i => i !== " " && i !== "\t");
						// }
						// const nextWord = nextChars.split(" ")[0];
						// if (isComment[0] && !["define", "declare", "alias"].includes(nextWord)) {
						//     switchMode("comment");
						//     resetToken();
						//     currToken += "\u200b";
						let is_comment = prevTokens.length === 0 || prevTokens.includes("\n") ? [true] : prevTokens.filter(i => i !== " " && i !== "\t").map(i => i === '\n');
						let next_word = nextChars.split(" ")[0];
						if (is_comment[0] && !["define", "declare", "alias"].some(command => command === next_word)) {
							switchMode("comment");
							resetToken();
							currToken += "\u200b";
						}
						currToken += char;
						needToReset = false;
					}
					if (needToReset) {
						resetToken(needToAppendChar);
					}
				}
			} else if (state.mode === "filter") {
				if (!" \t{}\"']$)\\\n=,.".includes(char)) {
					currToken += char;
				} else {
					let needToAppendChar = true;
					let needToReset = true;
					if (char === "]") {
						switchMode("back");
					} else if (char === "{") {
						if (tokens[tokens.length - 2] === "nbt") {
							let openedBrackets = 1;
							switchMode("nbt");
							state.nbt_type = char;
						}
					} else if ("\"'".includes(char)) {
						switchMode("string");
						state.string_type = char;
						currToken += char;
						needToReset = false;
					} else if (char === ".") {
						if (currToken === char) {
							currToken += char;
						} else {
							if (nextChar === char) {
								resetToken();
								currToken = char;
								needToReset = false;
							} else {
								currToken += char;
								needToReset = false;
							}
						}
						needToAppendChar = false;
					} else if (char === "$") {
						needToReset = false;
						if (nextChar === "(") {
							switchMode("macro");
							resetToken();
						}
						currToken += char;
					} else if (char === ")") {
						currToken += char;
						needToAppendChar = false;
					}
					if (needToReset) {
						resetToken(needToAppendChar);
					}
				}
			} else if (state.mode == "nbt") {
				if (!" \t[]{}\"'$)\\\n;:,=".includes(char)) {
					currToken += char;
				} else {
					let needToAppendChar = true;
					let needToReset = true;
					if ("\"'".includes(char)) {
						switchMode("string");
						state.string_type = char;
						currToken += char;
						needToReset = false;
					} else if (char == "$") {
						needToReset = false;
						if (next_char == "(") {
							switchMode("macro");
							resetToken();
						}
						currToken += char;
					} else if (char == ")") {
						currToken += char;
						needToAppendChar = false;
					}
					if (needToReset) {
						resetToken(needToAppendChar);
					}
					// Exiting nbt state if it's closed
					if (char == state.nbt_type) {
						openedBrackets += 1;
					} else if (char == closedBrackets[state.nbt_type]) {
						openedBrackets -= 1;
						if (openedBrackets == 0) {
							switchMode("back");
						}
					}
				}
			} else if (state.mode == "string") {
				currToken += char;
				if (char == state.string_type && currToken.slice(-2, -1) != "\\") {
					switchMode("back");
					resetToken();
				}
			} else if (state.mode == "comment") {
				if (char != "\n") {
					currToken += char;
				} else {
					switchMode("back");
					resetToken(true);
				}
			}

		}
		return tokens;
	}

	static highlight(func) {
	// Shortcuts
	const colors = Hl.Database.color_codes;
	const commands = Hl.Database.commands;

	// Setting up variables
	let commands_count = 0;
	let possible_subcommands = [];
	let bracket_index = 0;
	let highlighted = "";

	// Magic ✨
	const tokens = Hl.lex(func);
			console.log(tokens)

		for (let index = 0; index < tokens.length; index++) {
			let token = tokens[index];
			const prev_tokens = tokens.slice(0, index).reverse();
			const fut_tokens = tokens.slice(index + 1);
			
			// Handle token highlighting based on token type and context
			if (token == null) {
				1;
			} else if (token[0] == "\u200b") {
				// Handle comments
				const comment_content = token.replace(/(^\u200b#(#|>)?)/gm, "");
				let edited_content = comment_content;
				let comment_type = "comment";
	
				if (token[2] == "#" || token[2] == ">") {
					comment_type = "link-comment";
				}
	
				const pathes = comment_content.match(/#[a-zA-z_\-/:]+/g) || [];
				const decorators = comment_content.match(/@\w+/g) || [];
	
				pathes.forEach(path => {
					edited_content = edited_content.replace(path, `${colors["path"]}${path}${colors[comment_type]}`);
				});
	
				decorators.forEach(decorator => {
					edited_content = edited_content.replace(decorator, `${colors["subcommand"]}${decorator}${colors[comment_type]}`);
				});
	
				highlighted += colors["comment"] + token.replace(comment_content, "") + (comment_type == "link-comment" ? colors[comment_type] : "") + edited_content;
			} else if (" \t\n".includes(token)) {
				// Handle whitespaces
				highlighted += token;
			} else if (possible_subcommands.includes(token) && bracket_index <= 0) {
				// Handle possible subcommands
				highlighted += colors["subcommand"] + token;
			} else if (token.replace("$", "") in commands && bracket_index <= 0) {
				// Handle commands
				const raw_command = token.replace("$", "");
				if (raw_command != "execute") {
					possible_subcommands = [];
				}
				highlighted += (colors["macro"] + (token.includes("$") ? "$" : "") + colors["command"] + raw_command);
				possible_subcommands += commands[raw_command]["subcommands"];
			} else if (token[0] === "\"" || token[0] === "'") {
				// Highlighting macros in strings
				let highlightedString = colors["string"] + token;
				const macros = token.match(/\$\([0-9A-z-_\.]+\)/g) || [];
			
				macros.forEach(macro => {
					const macroName = macro.substring(2, macro.length - 1);
					const coloredMacro = macro.replace("$", colors["macro"] + "$")
												.replace("(", colors["bracket" + bracket_index] + "(" + colors["text"])
												.replace(")", colors["bracket" + bracket_index] + ")" + colors["string"]);
					highlightedString = highlightedString.replace(macro, coloredMacro);
				});
			
				highlighted += highlightedString;
			} else if (token == "..") {
				// Handle double dots
				highlighted += colors["command"] + token;
			} else if ("@#$%.".includes(token[0]) && token[1] != "(" && prev_tokens[0] != "]") {
				// Handle selectors
				highlighted += colors["selector"] + token;
			} else if (token.includes(":") && token != ":") {
				// Handle paths
				highlighted += colors["path"] + token;
			} else if ("[{(".includes(token)) {
				// Handle opening brackets
				highlighted += colors["bracket" + (bracket_index % 3)] + token;
				bracket_index++;
			} else if ("]})".includes(token)) {
				// Handle closing brackets
				bracket_index--;
				highlighted += colors["bracket" + (bracket_index % 3)] + token;
			} else if (":;=,".includes(token)) {
				// Handle separators
				highlighted += colors["separator"] + token;
			} else if (/[~\^]?[0-9]+(\.[0-9]+)?[bsdf]?/.test(token)) {
				// Handle numbers
				highlighted += colors["number"] + token;
			} else if (/\$\([0-9A-z-_\.]+\)/.test(token)) {
				// Handle macros
				const macroName = token.substring(2, token.length - 1);
				highlighted += `${colors["macro"]}$${colors["bracket" + bracket_index]}(${colors["text"]}${macroName}${colors["bracket" + bracket_index]})`;
			} else if (token == "\\") {
				// Handle backslashes
				highlighted += colors["backslash"] + token;
			} else {
				// Handle text
				highlighted += (bracket_index <= 0 ? colors["text"] : colors["key"]) + token;
			}
		}
		return highlighted;
	}
}

console.log(Hl.highlight(`# comment
#> comment
# @brbr #foo:bar/foojk
  execute as @a \\
	if score #x var <= #y var \\
	unless data entity @s foo.bar["baz"].test \\
	  run say hello world`));
