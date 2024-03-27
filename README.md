# MCF ansi highlighter

## User-application for discord
With new user-app feature you can now have mcfunction highlight everywhere in discord. To obtain it just click \[[Authorize](https://discord.com/oauth2/authorize?client_id=1221838702016331847)\]. The app also [open source](https://github.com/bth123/mcf-ansi-highlighter/tree/user-bot) btw

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
2. Download `main.py` and put it in your project folder.
3. From highlighter import class `Hl` in your code.
4. Use `Hl.highlight("<Your function here>")` to get the ansi highlighted function.
### JavaScript [outdated]
2. Download `main.js` and put it in your project folder.
3. Import `Hl` class from highlighter in your code.
4. Use `Hl.highlight("<Your function here>")` to get the ansi highlighted function.

Note: `database.json` must be at the folder where code executing. If for some reason you can't place it in that way, edit it's path in the module file.
