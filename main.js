class Highlighter {
    static Database = (() => {
        const databaseContent = {
            "color_codes": {
                "comment": "\u001b[30m",
                "link-comment": "\u001b[4;34m",
                "backslash": "\u001b[30m",
        
                "macro": "\u001b[34m",
        
                "command": "\u001b[35m",
                "subcommand": "\u001b[34m",
                
                "selector": "\u001b[36m",
                "delimiter": "\u001b[34m",
                
                "argument": "\u001b[0m",
                "path": "\u001b[33m",
                "number": "\u001b[32m",
                
                "bracket0": "\u001b[33m",
                "bracket1": "\u001b[35m",
                "bracket2": "\u001b[34m",
                
                "key": "\u001b[0m",
                "value": "\u001b[32m",
                "str_value": "\u001b[33m"
            },
            "commands": {
                "advancement": {
                    "subcommands": ["grant", "revoke", "everything", "only", "from", "through"]
                },
                "attribute": {
                    "subcommands": ["get", "base", "modifier", "add", "multiply", "multiply_base"]
                },
                "ban": {
                    "subcommands": []
                },
                "ban-ip": {
                    "subcommands": []
                },
                "ban-list": {
                    "subcommands": []
                },
                "bossbar": {
                    "subcommands": ["add", "get", "max", "players", "value", "visible", "list", "set", "color", "max", "name", "players", "style", "blue", "green", "pink", "purple", "red", "white", "yellow", "notched_6", "notched_10", "notched_12", "notched_20", "progress"]
                },
                "clear": {
                    "subcommands": []
                },
                "clone": {
                    "subcommands": ["from", "to", "replace", "masked", "force", "move", "normal", "filtered"]
                },
                "damage": {
                    "subcommands": ["at", "by", "from"]
                },
                "data": {
                    "subcommands": ["get", "merge", "modify", "remove", "block", "entity", "storage", "append", "insert", "prepend", "from", "string", "value"]
                },
                "datapack": {
                    "subcommands": ["disable", "enable", "list", "first", "last", "before", "after", "avaliable", "enabled"]
                },
                "debug": {
                    "subcommands": ["start", "stop", "function"]
                },
                "defaultgamemode": {
                    "subcommands": []
                },
                "deop": {
                    "subcommands": []
                },
                "difficulty": {
                    "subcommands": ["peaceful", "easy", "normal", "hard"]
                },
                "effect": {
                    "subcommands": ["clear", "give", "infinite"]
                },
                "enchant": {
                    "subcommands": []
                },
                "execute": {
                    "subcommands": ["align", "anchored", "as", "at", "facing", "in", "on", "positioned", "rotated", "store", "summon", "if", "unless", "run", "x", "y", "z", "xy", "xz", "xyz", "xzy", "yx", "yz", "yxz", "yzx", "zx", "zy", "zxy", "zyx", "eyes", "feet", "entity", "attacker", "controller", "leasher", "origin", "owner", "passengers", "target", "vehicle", "over", "result", "succes", "biome", "block", "data", "storage", "dimension", "loaded", "predicate", "score", "matches", "<", "<=", "=", ">=", ">"]
                },
                "experience": {
                    "subcommands": ["add", "set", "query", "levels", "points"]
                },
                "fill": {
                    "subcommands": ["destroy", "hollow", "kepp", "outline", "replace"]
                },
                "fillbiome": {
                    "subcommands": ["replace"]
                },
                "forceload": {
                    "subcommands": ["add", "remove", "query", "all"]
                },
                "function": {
                    "subcommands": ["with", "storage", "block", "entity"]
                },
                "gamemode": {
                    "subcommands": []
                },
                "gamerule": {
                    "subcommands": []
                },
                "give": {
                    "subcommands": []
                },
                "help": {
                    "subcommands": []
                },
                "item": {
                    "subcommands": ["modify", "replace", "block", "entity", "with", "from"]
                },
                "jfr": {
                    "subcommands": ["start", "stop"]
                },
                "kick": {
                    "subcommands": []
                },
                "kill": {
                    "subcommands": []
                },
                "list": {
                    "subcommands": ["uuids"]
                },
                "loacte": {
                    "subcommands": ["structure", "biome", "poi"]
                },
                "loot": {
                    "subcommands": ["give", "insert", "spawn", "replace", "block", "entity", "fish", "loot", "kill", "mine"]
                },
                "me": {
                    "subcommands": []
                },
                "motion": {
                    "subcommands": ["add", "set"]
                },
                "msg": {
                    "subcommands": []
                },
                "op": {
                    "subcommands": []
                },
                "pardon": {
                    "subcommands": []
                },
                "pardon-ip": {
                    "subcommands": []
                },
                "particle": {
                    "subcommands": ["force", "normal"]
                },
                "perf": {
                    "subcommands": ["start", "stop"]
                },
                "place": {
                    "subcommands": ["feature", "jigsaw", "structure", "template"]
                },
                "playsound": {
                    "subcommands": []
                },
                "publish": {
                    "subcommands": []
                },
                "recipe": {
                    "subcommands": ["give", "take"]
                },
                "reload": {
                    "subcommands": []
                },
                "return": {
                    "subcommands": []
                },
                "ride": {
                    "subcommands": ["mount", "dismount"]
                },
                "save-all": {
                    "subcommands": []
                },
                "save-off": {
                    "subcommands": []
                },
                "save-on": {
                    "subcommands": []
                },
                "say": {
                    "subcommands": []
                },
                "schedule": {
                    "subcommands": ["function", "clear", "append", "replace"]
                },
                "scoreboard": {
                    "subcommands": ["objectives", "players", "add", "remove", "setdisplay", "modify", "list", "get", "set", "add", "reset", "enable", "operation", "displayname", "rendertype", "hearts", "integer", "=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"]
                },
                "seed": {
                    "subcommands": []
                },
                "setblock": {
                    "subcommands": []
                },
                "setidletimeout": {
                    "subcommands": []
                },
                "setworldspawn": {
                    "subcommands": []
                },
                "spawnpoint": {
                    "subcommands": []
                },
                "spectate": {
                    "subcommands": []
                },
                "spreadplayers": {
                    "subcommands": ["under"]
                },
                "stop": {
                    "subcommands": []
                },
                "stopsound": {
                    "subcommands": []
                },
                "summon": {
                    "subcommands": []
                },
                "tag": {
                    "subcommands": ["add", "list", "remove", "list"]
                },
                "team": {
                    "subcommands": ["list", "add", "remove", "empty", "join", "leave", "modify"]
                },
                "teammsg": {
                    "subcommands": []
                },
                "teleport": {
                    "subcommands": []
                },
                "tell": {
                    "subcommands": []
                },
                "tellraw": {
                    "subcommands": []
                },
                "tick": {
                    "subcommands": ["query", "rate", "freeze", "step", "stop", "unfreeze", "sprint"]
                },
                "time": {
                    "subcommands": ["add", "query", "set", "daytime", "gametime", "day", "night", "noon", "midnight"]
                },
                "title": {
                    "subcommands": ["clear", "reset", "title", "subtitle", "actionbar", "times"]
                },
                "titleraw": {
                    "subcommands": []
                },
                "tp": {
                    "subcommands": []
                },
                "trigger": {
                    "subcommands": ["add", "set"]
                },
                "w": {
                    "subcommands": []
                },
                "weather": {
                    "subcommands": ["clear", "rain", "thunder"]
                },
                "whitelist": {
                    "subcommands": ["add", "list", "off", "on", "reload", "remove"]
                },
                "worldborder": {
                    "subcommands": ["add", "center", "damage", "get", "set", "warining", "amount", "buffer", "distance", "time"]
                },
                "xp": {
                    "subcommands": ["add", "set", "query", "levels", "points"]
                }
            }
        };

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
        console.log(this.rootCommand);
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
                console.log(rawRoot);
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

