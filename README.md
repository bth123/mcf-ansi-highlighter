# MCF ansi highlighter

## The Highlighter compared to Syntax mcfunction
1.
![highlighter](illustrations/highlighter1.png)
![vsc](illustrations/vsc1.png)

2.
![highlighter](illustrations/highlighter2.png)
![vsc](illustrations/vsc2.png)

## Use as module
### Python
1. Download `highlighter.py` and `database.json` and put it in your project folder.
2. Write `import path.to.highlighter` in your code.
3. Use `highlighter.highlight("<Your function here>")` to get the ansi highlighted function.
### JavaScript
1. Download `highlighter.js` and `database.json` and put it in your project folder.
2. Write `import "path.to.highlighter"` in your code.
3. Use `highlighter.highlight("<Your function here>")` to get the ansi highlighted function.
### C++
1. Download `highlighter.h` and `database.json` and put it in your project folder.
2. Write `#include <path/to/highlighter.h>` in your code.
3. Use `highlighter::highlight("<Your function here>")` to get the ansi highlighted function.

Note: `database.json` must be at the same folder as `highlighter`

## Other features
Also, highlighter has a few more functions that might be useful:
- `split("<command>")` - splits command to elements: `"execute as @e[type=pig, nbt={CustomName:'{"text":"Ruben"}'}] run say gex"` -> `["execute", "as", "@e[type=pig, nbt={CustomName:'{"text":"Ruben"}'}]", "run", "say", "gex"]`
- `target("<selector>")` highlights selector: `"@e[type=pig]"` -> `"[36m@e[33m[[32mtype[34m=[37mpig[33m]"`
- `nbt("<tag>")` highlights nbt tag: `"{NoAI:1b}"` -> `"[33m{[32mNoAI[34m: [37m1b[33m}"`

## Contribution
Right now I'm only one contributor, but you feel free to contact me at discord with your ideas or developments (bth123).
![contributors](illustrations/contributors.png)