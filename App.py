try:
	import os, zipfile, datetime, argparse, config, psutil, platform
	from colorama import Fore, Style
	from mega import Mega
except Exception:
	print("[!] A library error ocurred. Make sure you ran: python3 -m pip install -r requirements.txt")

if platform.system() == 'Linux':
    runningFile = 'java'
    def input_inf(text):
    	input("%s%s%s[%s%si%s]%s %s%s%s" % (Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Style.RESET_ALL, Fore.BLUE, text, Style.RESET_ALL))
    def input_error(text):
    	input("%s%s%s[%s%s!%s]%s %s%s%s" % (Style.RESET_ALL, Fore.RED, Style.BRIGHT, Style.RESET_ALL, Fore.RED, Style.BRIGHT, Style.RESET_ALL, Fore.RED, text, Style.RESET_ALL))
    def success_text(text):
    	print("%s%s%s[%s%s+%s]%s %s%s%s" % (Style.RESET_ALL, Fore.GREEN, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, Style.BRIGHT, Style.RESET_ALL, Fore.GREEN, text, Style.RESET_ALL))
    def informative_text(text):
    	print("%s%s%s[%s%si%s]%s %s%s%s" % (Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Style.RESET_ALL, Fore.BLUE, text, Style.RESET_ALL))
    def error_text(text):
    	print("%s%s%s[%s%s!%s]%s %s%s%s" % (Style.RESET_ALL, Fore.RED, Style.BRIGHT, Style.RESET_ALL, Fore.RED, Style.BRIGHT, Style.RESET_ALL, Fore.RED, text, Style.RESET_ALL))
    def warning_text(text):
    	print("%s%s%s[%s%s!%s]%s %s%s%s" % (Style.RESET_ALL, Fore.YELLOW, Style.BRIGHT, Style.RESET_ALL, Fore.YELLOW, Style.BRIGHT, Style.RESET_ALL, Fore.YELLOW, text, Style.RESET_ALL))
elif platform.system() == 'Darwin':
    runningFile = 'javaw.app'
elif platform.system() == 'Windows':
    runningFile = 'javaw'
    def input_inf(text):
    	input("[i] %s" % text)
    def input_error(text):
    	input("[!] %s" % text)
    def success_text(text):
    	print("[+] %s" % text)
    def informative_text(text):
    	print("[i] %s" % text)
    def error_text(text):
    	print("[!] %s" % text)
    def warning_text(text):
    	print("[!] %s" % text)

def help_reminder():
    	informative_text("Run python App.py --help for more info.")

parser = argparse.ArgumentParser('python App.py')  # The --help section
parser.add_argument('-u', '--user', type=str,
                    help='Your Mega.nz username (overrules user set in config.py).\nUsage: python App.py -u youremail@megaaccount.nz')
parser.add_argument('-p', '--password', type=str,
                    help='Mega.nz password (overrules password set in config.py)')
parser.add_argument('-w', '--world', type=str,
                    help='Name of the folder/world\
                    to back up (overrules folderName set in config.py')
parser.add_argument('-dl', '--download', type=int,
                    help='Download and unpack\
                    backups. Usage: python App.py -dl 1 where 1 indicates how many\
                    days/backups you want to go.')
args = parser.parse_args()

passed_user = args.user
passed_password = args.password
passed_worldname = args.world
dl = args.download

mega = Mega()  # Initiate Mega lib

# Check if user and pass is set or passed
if passed_user is not None:
    if passed_password is None:
        passed_password = input('Type the Mega.nz password for user '
                                + passed_user + ': ')
    m = mega.login(passed_user, passed_password)
elif config.megaCreds['user'] and config.megaCreds['password'] != '':
    m = mega.login(config.megaCreds['user'], config.megaCreds['password'])
else:
    error_text("No account settings found for Mega.nz")
    help_reminder()
    exit()


if str(args.world) != 'None':
    world = str(args.world)
else:
    world = config.world['folderName']


if world == '':
    error_text("No world folder set.")
    help_reminder()
    exit()


# The download backup functionality
def download_backup():
    days_back = dl - 1
    linklist = []
    filenamelist = []
    files = m.get_files()

    for node in files:  # cycle through what we are getting back from Mega
        newnode = files.get(node)
        name = newnode['a']
        filename = name['n']
        if world in filename:
            link = m.export(filename)
            filenamelist.append(filename)
            linklist.append(link)

    location = os.getcwd()
    informative_text(f"Mining duped world from {str(dl)} days ago.. Please wait.")
    filenamelist.sort(reverse=True)
    linklist.sort(reverse=True)
    dllink = (str(linklist[days_back]))
    dlfile = str(filenamelist[days_back])
    m.download_url(dllink, location)
    success_text("Mining complete.")
    informative_text("Crafting world from dupe - this will just take a game-tick or two, almost there...")
    with zipfile.ZipFile(dlfile, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall()
    success_text("Success! Grab your pickaxe and go mine!")


if args.download is not None:
    download_backup()
    exit()


def retrieve_file_paths(dirName):  # figure out what we are backing up
    filePaths = []

    for root, directories, files in os.walk(dirName):
        for filename in files:
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)

    return filePaths


def checkIfProcessRunning(processName):
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def main():
    now = str(datetime.datetime.today().date())
    ziparchive = world + now + '.zip'
    filePaths = retrieve_file_paths(world)

    informative_text(f"Duping {world}. Items being duped:")
    for fileName in filePaths:
        print(fileName)

    print('')
    informative_text("Crafting a shulker box with your world inside. This may have the Slowness effect depending on your world size, computers specs and such.")
    zip_file = zipfile.ZipFile(ziparchive, 'w')
    with zip_file:
        for file in filePaths:
            zip_file.write(file)

    success_text(f"The shulker {ziparchive} was crafted successfully!")
    folder = m.find('mcbackup')
    informative_text("Uploading... Please wait...")
    backup = m.upload(ziparchive, folder)
    success_text(f"{world} has been duped and sent to the following ender chest: ")
    link = m.get_upload_link(backup)
    print()
    print(link)
    quota = m.get_storage_space(giga=True)
    print('')
    informative_text("Tidying up - throwing local shulker in lava...")
    os.remove(ziparchive)
    warning_text(f"You have now used {str(round(quota['used'], 2))} GB of your {str(quota['total'])} GB total in your ender chest inventory.")

# Let's do this
if __name__ == '__main__':
    if checkIfProcessRunning(runningFile):
        input_error('Minecraft is running. Please close the game, and press any key to continue...')
        exec(open('App.py').read())
    else:
        main()
