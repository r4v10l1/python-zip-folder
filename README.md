## Python Zip'n'Backup

Edited from https://github.com/mikkelrask/python-zip-folder. Nice work.

A simple python script to frequently backup any folder, and automaticly upload it to Mega.nz. It is however made with a minecraft world folder in mind.

It utilizes [mega.py](https://pypi.org/project/mega.py/ "mega.py on PyPi.org") and the idea is to run it on a daily basis through a basic [cron job](https://en.wikipedia.org/wiki/Cron "Cron on Wiki"), or whatever equilant your OS offers.

The script will sorta check if the game is running, and will not execute if that is the case. This is to prevent chunk curruption i.e chunks that are being saved at the same time, as the script tries to backup or similar. Simply it will not run, if Java is running.

It should be able to run on every machine that has python installed, but have not been testet thuroughly. (Tested on windows 10, minecraft 1.16.5)

(Rice not cool as original so not gonna even post it)

### Installing

`git clone https://github.com/r4v10l1/python-zip-folder PATH-TO-YOUR-SAVES-FOLDER`

`pip install -r requirements.txt` (Updated the file to add colorama)

`python3 App.py`

### Configuring

#### Editing the config.py file

`vim config.py` (You need to edit the file in order to add your login information)

While mega uploads can be anonymized and do accept anonymous uploads, the script does assume you have a Mega.nz account and will not work if no account is given. Open up config.py in any text editor and put in your account credentials in (`user` and `password`), and put in the name if your world save folder name on (`folderName`), and hit save.

#### With arguments

If you want to have more control or run multiple instances (to have more than one world backup, or back up to multiple accounts) you're also able to pass arguments through the commandline.

Ie:
`python App.py -u John@johnson.com -p Ep1cHardP4ss -w HawaiiMC -dl 1`

will download John's HawaiiMC backup from yesterday.

`-u` expects a string. This is your email for your Mega.nz account

`-p` expects a string. This is your password for your Mega.nz account

`-w` expects a string. With this one you are able to define what folder/world you want to backup.

`-dl` is of course optional and expects and integer representing how many backups/days you want to go back.

Note: If you don't want to use your password in the command because you don't want to store it in the shell history, you can add a blank space
` `
before your command.

### Help

`python App.py --help`
