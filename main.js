class Highlighter {
    static Database = (() => {
        const fs = require("fs");
        const databaseContent = JSON.parse(fs.readFileSync("database.json"));

        return {
            color_codes: databaseContent.color_codes,
            commands: databaseContent.commands,
            regexes: {
                nbt: /(\$\([a-zA-Z0-9_-]*\)|string[0-9]+|[a-zA-Z_]\w*|[0-9]+[a-zA-Z]?|[\[\]{},:;])/,
                string: /(?<!\\)(?:"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\')/,
                macro: /\$\([a-zA-Z0-9_-]*\)/
            }
        };
    })();
    static rootCommand = "";

    static highlight(functionString) {
        let highlighted = "";
        functionString = functionString.replace("\\\n", "\\newline");
        const commands = functionString.split("\n");

        commands.forEach((command) => {
            highlighted += `${Highlighter.line(command)}\n`;
        });

        return highlighted;
    };

    static line(command) {
        // Shortcuts
        const colors = Highlighter.Database.color_codes;
        const commands = Highlighter.Database.commands;
        // Main
        const rawCommand = command.trimLeft();
        const tabsCount = command.length - rawCommand.length;
        // Comment check
        if (rawCommand === "") {
            return rawCommand;
        } else if (rawCommand[0] === "#") {
            if (rawCommand[1] === "#" || rawCommand[1] === ">") {
                return " ".repeat(tabsCount) + colors["comment"] + "#>" + colors["link-comment"] + rawCommand.substring(2);
            } else {
                return `${' '.repeat(tabsCount)}${colors['comment']}${rawCommand}`;
            }
        }
        // Command highlight
        const commandParts = Highlighter.split(rawCommand);
        const highlighted = [];
        for (const element of commandParts) {
            let rawRoot = element.replace("$", "").replace("\\newline", "");
            if (rawRoot in commands) {
                highlighted.push(colors["command"] + element);
                Highlighter.rootCommand = rawRoot;
            } else if (
                Highlighter.rootCommand !== "" &&
                commands[Highlighter.rootCommand]["subcommands"].includes(element.replace("\\newline", ""))
            ) {
                highlighted.push(colors["subcommand"] + element);
            } else if (element[0] === "@") {
                highlighted.push(Highlighter.target(element));
            } else if (["#", "%", "&"].includes(element[0])) {
                highlighted.push(colors["selector"] + element);
            } else if (element[0] === "{") {
                highlighted.push(Highlighter.nbt(element));
            } else if (element.includes(":")) {
                highlighted.push(colors["path"] + element);
            } else if (!isNaN(element)) {
                highlighted.push(colors["number"] + element);
            } else if (element.slice(0, -2) === "$(") {
                highlighted.push(
                    colors["macro"] +
                    "$" +
                    colors["bracket0"] +
                    "[" +
                    colors["argument"] +
                    element.slice(2, -1) +
                    colors["bracket0"] +
                    "]"
                );
            } else {
                highlighted.push(colors["argument"] + element);
            }
        }
        return `${' '.repeat(tabsCount)}${highlighted.join(' ')}`.replace("\\newline", `${colors['backslash']}\\\n`);
    };

    static split(command) {
        command += " ";
        const commandElements = [];
        const strings = [];
        let bracketsCount = 0;
        let currentElement = "";

        for (let index = 0; index < command.length; index++) {
            const char = command[index];

            if (strings.length >= 1) {
                if (char === strings[strings.length - 1] && command[index - 1] !== "\\") {
                    strings.pop();
                }
                currentElement += char;
            } else if (char === "\"" || char === "'") {
                strings.push(char);
                currentElement += char;
            } else if (char === "{" || char === "[") {
                bracketsCount += 1;
                currentElement += char;
            } else if (char === "}" || char === "]") {
                bracketsCount -= 1;
                currentElement += char;
            } else if (char === " " && bracketsCount === 0) {
                commandElements.push(currentElement);
                currentElement = "";
            } else {
                currentElement += char;
            }
        }

        return commandElements;
    };

    static target(selector) {
        // Shortcuts
        const colors = Highlighter.Database.color_codes;
        // Main
        let tag = "";
        let nbts = [];
        if (selector.includes("nbt")) {
            // States
            let bracketsCount = 0;
            let currTag = "";
            for (const char of selector) {
                if (char === "{") {
                    bracketsCount += 1;
                    currTag += char;
                } else if (char === "}") {
                    bracketsCount -= 1;
                    currTag += char;
                    if (bracketsCount === 0) {
                        selector = selector.replace(currTag, `%%%%nbt${nbts.length}%%%%`);
                        nbts.push(currTag);
                        currTag = "";
                    }
                } else if (bracketsCount >= 1) {
                    currTag += char;
                }
            }
        }
        let highlighted = colors["selector"] + selector
            .replace("[", `${colors['bracket0']}[${colors['key']}`)
            .replace("]", `${colors['bracket0']}]`)
            .replace("=", `${colors['delimiter']}=${colors['value']}`)
            .replace(",", `${colors['delimiter']},${colors['key']}`)
            .replace("!", `${colors['delimiter']}!${colors['value']}`)
            .replace("..", `${colors['bracket1']}..${colors['value']}`)
            .replace("#", `${colors['selector']}#`)
            .replace("{", `${colors['bracket1']}{$${colors['key']}`)
            .replace("}", `${colors['bracket1']}}${colors['value']}`);

        if (nbts.length >= 1) {
            for (let index = 0; index < nbts.length; index++) {
                highlighted = highlighted.replace(`%%%%nbt${index}%%%%`, Highlighter.nbt(nbts[index], 0));
            }
        }
        return highlighted;
    };

    static nbt(tag, bracketsDepth = -1) {
        const colors = Highlighter.Database.color_codes;
        const stringRe = Highlighter.Database.regexes.string;
        const strings = tag.match(new RegExp(stringRe, "g")) || [];

        strings.forEach((string, index) => {
            tag = tag.replace(string, `string${index}`);
        });

        function lexer(tag, bracketsDepth) {
            const tokens = [];
            const nbtRe = Highlighter.Database.regexes.nbt;

            tag.replace(new RegExp(nbtRe, "g"), (match) => {
                const token = match;

                if ("1234567890".includes(token[0]) || "BIL".includes(token)) {
                    tokens.push([token, "value"]);
                } else if (token.slice(0, 6) === "string") {
                    tokens.push([token, "string"]);
                } else if ("[{".includes(token)) {
                    bracketsDepth += 1;
                    bracketsDepth %= 3;
                    tokens.push([token, `bracket${bracketsDepth}`]);
                } else if ("}]".includes(token)) {
                    tokens.push([token, `bracket${bracketsDepth}`]);
                    bracketsDepth -= 1;
                    bracketsDepth %= 3;
                } else if (":,;".includes(token)) {
                    tokens.push([token, "delimiter"]);
                } else if (token.slice(0, 2) === "$(") {
                    tokens.push([token, `bracket${(bracketsDepth + 1) % 3}`]);
                } else {
                    tokens.push([token, "key"]);
                }

                return '';
            });

            return tokens;
        }

        const lexed = lexer(tag, bracketsDepth);
        let highlighted = "";

        lexed.forEach(([token, type]) => {
            if (token.slice(0, 2) === "$(") {
                highlighted += `${colors['macro']}$${colors[type]}(${colors['argument']}${token.slice(2, -1)}${colors[type]})`;
            } else if (type === "string") {
                highlighted += `${colors['str_value']}${strings[parseInt(token.replace('string', ''))]}`;
            } else {
                highlighted += colors[type] + token;
                if (type === "delimiter") {
                    highlighted += " ";
                }
            }
        });

        return highlighted;
    };
}

var a = Highlighter.highlight("say gex");
console.log(a);
