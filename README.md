# MCF ansi highlighter

## Website problems
As of right now, I am encountering difficulties with updating the site. If you want to use the latest highligter version you can [install](https://github.com/bth123/mcf-ansi-highlighter?tab=readme-ov-file#python) it on your pc.

## The Highlighter compared to Syntax mcfunction
1.
![highlighter](illustrations/highlighter1.png)
![vsc](illustrations/vsc1.png)

2.
![highlighter](illustrations/highlighter2.png)
![vsc](illustrations/vsc2.png)

## Use in your projects
If you want to use the highlighter in your project, please leave credit to the original github repo.
1. Downlaod `database.json` and put it in your project folder.
### Python 
2. Download `highlighter.py` and put it in your project folder.
3. From `highlighter` import class `Highlighter` in your code.
4. Use `Highlighter.highlight("<Your function here>")` to get the ansi highlighted function.
### JavaScript [outdated]
2. Download `highlighter.js` and put it in your project folder.
3. Import `Highlighter` class from `highlighter` in your code.
4. Use `Highlighter.highlight("<Your function here>")` to get the ansi highlighted function.

Note: `database.json` must be at the folder where code executing. If for some reason you can't place it in that way, edit it's path in the module file.
