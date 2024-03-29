from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import keyboard
import platform
import random
import time

project_name = 'HunterVerse'
version = '0.9.3.7'
version_code = sum(list(map(int, version.split('.'))))
root = Tk()
root.resizable(False, False)
root.title(f'{project_name} {version}')
root.withdraw()

with open('hunterverse\\assets\\user\\userdata.py', 'r') as userget:
    if userget.read().strip() != '':
        register_need = False
    else:
        with open('hunterverse\\assets\\user\\userdata.py', 'w') as changeUnsaved:
            changeUnsaved.write(
                f'''# .%.%.%.%.
pet = ''
equipment = ''
lootbox = ''

closed = 'None'
updated = '{time.strftime(f"%m-%d-%Y%%%T%%{int(time.time())}")}'
''')
        register_need = True

facts_tricks_string = f'''
The more valuable a lootbox is, the longer it takes to open it.
A username can only have from 3 to 10 characters!
This game is created by Hung.
This game is inspired by OwO Bot (a Discord bot).
The name of the game is "{project_name}" for anyone who forgot.
The current version of the game is: "{version}".
You are reading this.
You are breathing.
It\'s {time.strftime("%I:%M %p")} now.
Today is {time.strftime("%A")}.
{"APRIL FOOLS BABY!!!" if time.strftime("%d/%m") == "01/04" else "Today is not April Fools"}
At the initialization, there are always 4 facts.
You can\'t resist against reading this line.
'''
facts_trick = random.sample(facts_tricks_string.strip().split('\n'), k=5)

# GENERAL
operator_sys = platform.system()
isMainStarted = False
username = 'Unknown'
money = 0

# TEMPORARY VARIABLE
repeatMainProgress = '0'
moneyValue = '0'


def temp():
    pass


def savedata(closed: bool = False):
    with open('hunterverse\\assets\\user\\userdata.py', 'r') as saveData:
        linesRead = saveData.readlines()
        fileString: list = linesRead[0].replace('#', '').strip().split('%')
    fileString[4] = str(money)
    with open('hunterverse\\assets\\user\\userdata.py', 'w') as saveRegister:
        saveRegister.write(f'''# {"%".join(fileString)}
pet = '{".".join(petListAlt)}'
equipment = '{".".join(equipmentListAlt)}'
lootbox = '{".".join(lootboxListAlt)}'

closed = '{time.strftime(f"%m-%d-%Y%%%T%%{int(time.time())}") if closed else linesRead[5][:-1].replace("closed = ", "").replace("'", "")}'
updated = '{time.strftime(f"%m-%d-%Y%%%T%%{int(time.time())}")}'
''')


def register():
    registerPage = Toplevel(root)
    registerPage.title('Registration')
    registerPage.resizable(False, False)

    def registerCallback(_):
        maximumUsernameLengthLabel.configure(
            text=f'{"  " if len(usernameEntry.get()) < 10 else ""}{len(usernameEntry.get())}/10')
        if any(i not in '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM' for i in
               usernameEntry.get()) or usernameEntry.get().isdigit() or not 3 <= len(usernameEntry.get()) <= 10 or \
                usernameEntry.get().count('_') > 1 or usernameEntry.get()[-1] in ['_', '.']:
            if len(usernameEntry.get()) > 15:
                usernameEntry.delete(15, END)
                maximumUsernameLengthLabel.configure(text='15/10')
            submitregisterButton.configure(state=DISABLED)
            if len(usernameEntry.get()) == 0:
                maximumUsernameLengthLabel.configure(foreground='black')
            else:
                maximumUsernameLengthLabel.configure(foreground='#a60a0a')
        else:
            submitregisterButton.configure(state=NORMAL)
            maximumUsernameLengthLabel.configure(foreground='black')

    def submitRegister():
        usernameEntry.unbind('<KeyRelease>')
        submitregisterButton.configure(state=DISABLED)
        usernameEntry.configure(state=DISABLED)
        with open('hunterverse\\assets\\user\\userdata.py', 'w') as saveRegister:
            saveRegister.write(
                f'''# {usernameEntry.get()}%{time.strftime("%m-%d-%Y")}%{time.strftime("%T")}%{int(time.time())}%1000
pet = ''
equipment = ''
lootbox = '{".".join(["Basic Lootbox" for _ in range(3)])}'

closed = 'None'
updated = '{time.strftime(f"%m-%d-%Y%%%T%%{int(time.time())}")}'
''')

        Label(registerPage, text='Processing...', font=('Calibri', 11, 'bold')).grid(row=10, column=3, columnspan=3,
                                                                                     pady=5)
        root.after(random.randint(2500, 5000), lambda: [registerPage.destroy(), loadingProcess()])

    def quitRegister():
        if messagebox.askyesno('Quit Registration', 'Are you sure to cancel the registration progress?'):
            open('hunterverse\\assets\\user\\userdata.py', 'w').close()
            root.destroy()

    mainregisterFrame = Frame(registerPage)
    mainregisterFrame.grid(row=3, column=3)

    registerHeader = Label(mainregisterFrame, text='Register', font=('Calibri', 15, 'bold'))
    registerHeader.grid(row=3, column=3, columnspan=4, pady=3)

    Label(mainregisterFrame, text='Username:').grid(row=5, column=4, padx=2)
    usernameEntry = Entry(mainregisterFrame)
    usernameEntry.grid(row=5, column=5)

    maximumUsernameLengthLabel = Label(mainregisterFrame, text='  0/10')
    maximumUsernameLengthLabel.grid(row=5, column=6, padx=3)

    submitregisterButton = Button(mainregisterFrame, text='Register', state=DISABLED, command=submitRegister)
    submitregisterButton.grid(row=9, column=3, columnspan=4)

    registerPage.protocol("WM_DELETE_WINDOW", quitRegister)
    usernameEntry.bind('<KeyRelease>', registerCallback)


def loadingProcess():
    global username, money

    mainProgressWindow = Toplevel(root)
    mainProgressWindow.title('Initialization')
    mainProgressValueLabel = Label(mainProgressWindow, text='Initializing... (0%)', font=('Calibri', 13, 'bold'))
    mainProgressValueLabel.grid(row=3, column=3, sticky='ew', pady=5)
    mainProgressWindow.resizable(False, False)

    with open('hunterverse\\assets\\user\\userdata.py', 'r') as setUser:
        userString = setUser.readlines()[0].replace('#', '').strip().split('%')
        username = userString[0]
        money = int(userString[4])

    def startInit():
        global repeatMainProgress

        def endProgress():
            global isMainStarted
            mainProgressWindow.destroy()
            root.deiconify()
            isMainStarted = True

            if register_need and isMainStarted:
                root.after(250, lambda: messagebox.showinfo('Claim Confirmed',
                                                            f'You have claimed ${money} as a STARTER GIFT!'))
            keyboard.add_hotkey('ctrl+shift+a+1', pet)
            keyboard.add_hotkey('ctrl+shift+a+2', equipment)
            keyboard.add_hotkey('ctrl+shift+a+3', lootbox)
            keyboard.add_hotkey('ctrl+shift+a+4', coinflip)
            keyboard.add_hotkey('ctrl+shift+b+1', hunt)
            root.attributes("-topmost", True)
            root.attributes("-topmost", False)

        if mainProgressbar['value'] < 100:
            if mainProgressbar['value'] == 24:
                factsLabel.configure(text=f'Facts: {facts_trick[1]}')
            if mainProgressbar['value'] == 49:
                factsLabel.configure(text=f'Facts: {facts_trick[2]}')
            if mainProgressbar['value'] == 74:
                factsLabel.configure(text=f'Facts: {facts_trick[3]}')
            mainProgressbar['value'] += 1
            mainProgressValueLabel.configure(text=f'Initializing... ({int(mainProgressbar["value"])}%)')
            repeatMainProgress = root.after(random.randint(5, 450), startInit)
        else:
            mainProgressValueLabel.configure(text=f'Successfully run: {project_name} {version}')
            factsLabel.configure(text=f'Thanks for playing {project_name}. Now, enjoy your game!', foreground='#350c4f')
            root.after(random.randint(2500, 5000), endProgress)

    mainProgressbar = ttk.Progressbar(mainProgressWindow, orient='horizontal', mode='determinate', length=500)
    mainProgressbar.grid(row=4, column=3, sticky='ew', padx=7)

    factsLabel = Label(mainProgressWindow, text=f'Facts: {facts_trick[0]}', font=('Calibri', 10, 'bold'))
    factsLabel.grid(row=6, column=3)

    mainProgressWindow.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    root.after(random.randint(1000, 2500),
               lambda: [startInit(), mainProgressWindow.protocol("WM_DELETE_WINDOW", askCancelProgress)])

    def askCancelProgress():
        global repeatMainProgress
        if messagebox.askyesno(f'Cancel Initialization',
                               'Are you sure to cancel initialization?\nThis might cause damage to the assets!'):
            mainProgressWindow.protocol("WM_DELETE_WINDOW", temp)
            root.after_cancel(repeatMainProgress)
            mainProgressbar['value'] = 100
            mainProgressValueLabel.configure(text='Terminating initialization...')
            root.after(random.randint(1500, 3000), lambda: root.destroy())
            savedata()
            del repeatMainProgress

    mainProgressWindow.protocol("WM_DELETE_WINDOW", temp)


def notWindow():
    diffOP = Toplevel(root)
    diffOP.title('Warning')
    Label(diffOP,
          text=f'This game is programmed on Windows environment.\nIf you run on an another Operating System ({operator_sys}), some features might break.',
          font=('Calibri', 11, 'bold'), foreground='#80211b').grid(row=2, column=3)

    def tempCall(validator: bool = False):
        continueButton.configure(state=DISABLED)
        quitButton.configure(state=DISABLED)
        if not validator:
            root.after(random.randint(1500, 3000), lambda: exit())
        else:
            root.after(random.randint(2500, 5000),
                       lambda: [diffOP.destroy(), register() if register_need else loadingProcess()])
        return

    continueButton = Button(diffOP, text='Yes, I understand what I am doing', width=30,
                            command=lambda: tempCall(True))
    quitButton = Button(diffOP, text='No, I don\'t want to continue', width=30, command=tempCall)

    continueButton.grid(row=3, column=3)
    quitButton.grid(row=4, column=3)


if operator_sys != 'Windows':
    notWindow()
elif register_need:
    register()
else:
    loadingProcess()


# DECLARATION


def average(*args):
    return sum(args) / len(args)


def keyforPetsPropertiesFilter(x: str):
    i = x[0]
    properties = [[i.split('.')[0], i.split('.')[1].split(':')] for i in petsPropertiesString.split('\n') if i != '']
    return int(average(int("".join([k[1][0] for k in properties if i in k])),
                       int("".join([k[1][1] for k in properties if i in k]))))


def keyforPetsFilter(x: str):
    if x == '':
        return 0
    return int(average(int("".join([k[1][0] for k in petsProperties if x in k])),
                       int("".join([k[1][1] for k in petsProperties if x in k]))))


def keyforWeaponsFilter(x: str):
    return int("".join([k[1] for k in equipmentProperties if x in k])), int(
        "".join([k[1] for k in equipmentProperties if x in k]))


def keyforLootboxFilter(x: str):
    sortedLootbox = ['Basic Lootbox', 'Silver Lootbox', 'Copper Lootbox', 'Iron Lootbox', 'Golden Lootbox',
                     'Diamond Lootbox', 'Emerald Lootbox', 'Special Lootbox', 'Asian Lootbox']
    return sortedLootbox.index(x)


# # Values DECLARATION
isPetOpened = False
isEquipmentOpened = False
isLootboxOpened = False
isCoinFlipOpened = False
isBuyOpened = False
isHuntingOpened = False

# # Pets DECLARATION
petsPropertiesString = f'''
Dog.58:56
Cat.52:46
Elephant.68:85
Eagle.81:52
Cow.36:42
Turtle.16:92
Rabbit.39:17
Cheetah.82:71
Crocodile.83:81
Bear.85:78
Wolf.76:52
Rat.38:27
Fox.61:50
Buffalo.80:76
{"urmom.100:100" if time.strftime("%d/%m") == "01/04" else "Penguin.28:16"}
'''

# noinspection PyTypeChecker
petsProperties = sorted(
    [[i.split('.')[0], i.split('.')[1].split(':')] for i in petsPropertiesString.split('\n') if i != ''],
    key=keyforPetsPropertiesFilter, reverse=True)
with open('hunterverse\\assets\\user\\userdata.py', 'r') as getPetList:
    petLine = getPetList.readlines()[1].replace('pet = ', '').replace('\'', '').strip().split('.')
petListAlt = petLine if petLine[0] != '' else []
petList = sorted(list(set(petListAlt.copy())), key=keyforPetsFilter, reverse=True)
# petList = sorted([x[0] for x in petsProperties], key=keyforPetsFilter, reverse=True)

# # Equipment DECLARATION
equipmentPropertiesString = f'''
Sword.10
Hammer.10
Axe.15
Knife.5
Spear.7
Crossbow.7
Bow.5
Helmet.25
Armor.30
Leggings.20
Boots.10
Shovel.5
Slippers.3
Strength Poison 1.10
Strength Poison 2.15
Strength Poison 3.25
'''

equipmentProperties = [[i.split('.')[0], i.split('.')[1]] for i in equipmentPropertiesString.split('\n') if i != '']
with open('hunterverse\\assets\\user\\userdata.py', 'r') as getEquipmentList:
    equipmentLine = getEquipmentList.readlines()[2].replace('equipment = ', '').replace('\'', '').strip().split('.')
equipmentListAlt = equipmentLine if equipmentLine[0] != '' else []
equipmentList = sorted(list(set(equipmentListAlt.copy())), key=keyforWeaponsFilter, reverse=True)

# # Lootbox DECLARATION
lootboxPropertiesString = f'''
Basic Lootbox.Knife:Bow:Spear
Silver Lootbox.Knife:Bow:Crossbow:Spear:Sword
Copper Lootbox.Knife:Bow:Crossbow:Spear:Sword:Hammer
Iron Lootbox.Knife:Bow:Crossbow:Spear:Sword:Hammer:Strength Poison 1
Golden Lootbox.Bow:Crossbow:Spear:Sword:Hammer:Axe:Boots
Diamond Lootbox.Bow:Spear:Sword:Hammer:Axe:Boots:Leggings:Strength Poison 2
Emerald Lootbox.Sword:Hammer:Axe:Boots:Leggings:Armor:Helmet:Strength Poison 3
Special Lootbox.Axe:Boots:Leggings:Armor:Helmet:Strength Poison 1:Strength Poison 2:Strength Poison 3
{"Asian Lootbox.Slippers" if time.strftime("%d/%m") == "01/04" else ""}
'''
lootboxProperties = [[i.split('.')[0], i.split('.')[1].split(':')] for i in lootboxPropertiesString.split('\n') if
                     i != '']
with open('hunterverse\\assets\\user\\userdata.py', 'r') as getLootboxList:
    lootboxLine = ['Basic Lootbox', 'Basic Lootbox', 'Basic Lootbox'] if register_need else getLootboxList.readlines()[
        3].replace('lootbox = ', '').replace('\'', '').strip().split('.')
lootboxListAlt = lootboxLine if lootboxLine[0] != '' else []
lootboxList = sorted(list(set(lootboxListAlt.copy())), key=keyforLootboxFilter)

lootboxPrices = {
    'Basic Lootbox': 100,
    'Silver Lootbox': 500,
    'Copper Lootbox': 750,
    'Iron Lootbox': 1000,
    'Golden Lootbox': 1500,
    'Diamond Lootbox': 2000,
    'Emerald Lootbox': 3000,
    'Special Lootbox': 5000,
    'Asian Lootbox': 10000
}

# HEADER FRAME
headerFrame = Frame(root)
headerFrame.grid(row=3, column=3)

headerText = Label(root, text=f'{project_name}', font=('Calibri', 22, 'bold'), foreground='#2c0a57')
headerText.grid(row=3, column=3, pady=10, padx=5)

ttk.Separator(root, orient='horizontal').grid(row=4, column=3, sticky='ew')
Label(root, text=f'Version: {version}', font=('Verdana', 8, 'bold')).grid(row=4, column=3)
# MENU FRAME
menuFrame = Frame(root)
menuFrame.grid(row=5, column=3, padx=5, pady=5)


def pet():
    global petList, isPetOpened
    if isPetOpened:
        return
    isPetOpened = True

    def petCallbackProtocol(master):
        global isPetOpened
        isPetOpened = False
        master.destroy()

    def petSelect(_):
        selected_indices = petListbox.curselection()[0]
        selected_item = petList[selected_indices]

        petNameLabel.configure(
            text=f'{selected_item} {f"(x{petListAlt.count(selected_item)})" if petListAlt.count(selected_item) > 1 else ""}')
        petInfoLabel.configure(
            text=f'Attack\t: {"".join([k[1][0] for k in petsProperties if selected_item in k])}\nDefense\t: {"".join([k[1][1] for k in petsProperties if selected_item in k])}\nTotal\t: {int(average(int("".join([k[1][0] for k in petsProperties if selected_item in k])), int("".join([k[1][1] for k in petsProperties if selected_item in k]))))}')

    petWindow = Toplevel(root)
    petWindow.title('Pets')
    petWindow.resizable(False, False)

    mainpetFrame = Frame(petWindow)
    mainpetFrame.grid(row=3, column=3, padx=5, pady=5)

    Label(mainpetFrame, text=f'{username}\'s Pets:', font=('Calibri', 18, 'bold')).grid(row=3, column=3, columnspan=3,
                                                                                        pady=5)
    petListbox = Listbox(mainpetFrame, listvariable=Variable(value=petList), border=1, selectmode=BROWSE,
                         font=('Calibri', 11, 'normal'))
    petListbox.grid(row=5, column=3, rowspan=75, sticky='nsew')

    petlistScrollbar = ttk.Scrollbar(mainpetFrame, orient=VERTICAL, command=petListbox.yview)
    petlistScrollbar.grid(row=5, column=4, rowspan=75, sticky='wns')
    petListbox.configure(yscrollcommand=petlistScrollbar.set)

    petNameLabel = Label(mainpetFrame, text='N/A', font=('Calibri', 11, 'bold'))
    petNameLabel.grid(row=5, column=5, sticky='n')
    petInfoLabel = Label(mainpetFrame, text='Attack\t: ...\nDefense\t: ...\nTotal\t: ...')
    petInfoLabel.grid(row=7, column=5, sticky='n')

    Button(mainpetFrame, text='Close', command=lambda: petCallbackProtocol(petWindow), background='red').grid(
        row=70, column=5,
        sticky='ew',
        padx=10)
    petListbox.bind('<<ListboxSelect>>', petSelect)
    petWindow.protocol("WM_DELETE_WINDOW", lambda: petCallbackProtocol(petWindow))


def equipment():
    global equipmentList, isEquipmentOpened
    if isEquipmentOpened:
        return
    isEquipmentOpened = True

    def equipmentCallbackProtocol(master):
        global isEquipmentOpened
        isEquipmentOpened = False
        master.destroy()

    def equipmentSelect(_):
        selected_indices = equipmentListbox.curselection()[0]
        selected_item = equipmentList[selected_indices]

        equipmentNameLabel.configure(
            text=f'{selected_item} {f"(x{equipmentListAlt.count(selected_item)})" if equipmentListAlt.count(selected_item) > 1 else ""}')
        equipmentInfoLabel.configure(
            text=f'Total: +{"".join([k[1] for k in equipmentProperties if selected_item in k])}%')

    equipmentWindow = Toplevel(root)
    equipmentWindow.title('Equipment')
    equipmentWindow.resizable(False, False)

    mainequipmentFrame = Frame(equipmentWindow)
    mainequipmentFrame.grid(row=3, column=3, padx=5, pady=5)

    Label(mainequipmentFrame, text=f'{username}\'s Equipment:', font=('Calibri', 18, 'bold')).grid(row=3, column=3,
                                                                                                   columnspan=3,
                                                                                                   pady=5)
    equipmentListbox = Listbox(mainequipmentFrame, listvariable=Variable(value=equipmentList), border=1,
                               selectmode=BROWSE,
                               font=('Calibri', 11, 'normal'))
    equipmentListbox.grid(row=5, column=3, rowspan=75, sticky='nsew')

    equipmentlistScrollbar = ttk.Scrollbar(mainequipmentFrame, orient=VERTICAL, command=equipmentListbox.yview)
    equipmentlistScrollbar.grid(row=5, column=4, rowspan=75, sticky='wns')
    equipmentListbox.configure(yscrollcommand=equipmentlistScrollbar.set)

    equipmentNameLabel = Label(mainequipmentFrame, text='N/A', font=('Calibri', 11, 'bold'))
    equipmentNameLabel.grid(row=5, column=5, sticky='n')
    equipmentInfoLabel = Label(mainequipmentFrame, text='Total: +...%')
    equipmentInfoLabel.grid(row=7, column=5, sticky='n')

    Button(mainequipmentFrame, text='Close', command=lambda: equipmentCallbackProtocol(equipmentWindow),
           background='red').grid(row=70,
                                  column=5,
                                  sticky='ew',
                                  padx=10)
    equipmentListbox.bind('<<ListboxSelect>>', equipmentSelect)
    equipmentWindow.protocol("WM_DELETE_WINDOW", lambda: equipmentCallbackProtocol(equipmentWindow))


def lootbox():
    global lootboxList, isLootboxOpened
    if isLootboxOpened:
        return
    isLootboxOpened = True

    def lootboxCallbackProtocol(master):
        global isLootboxOpened
        isLootboxOpened = False
        master.destroy()

    def openLootbox():
        global lootboxList
        selected_index = lootboxListbox.curselection()[0]
        selected_item = lootboxList[selected_index]

        if messagebox.askyesno('Lootbox Open',
                               f'Do you want to open a{"n" if selected_item[0] in "UEOAI" else ""} {selected_item}?'):
            def progress():
                global lootboxList

                def opened():
                    global equipmentList, lootboxList, isLootboxOpened
                    itemOpened = random.choice([k[1] for k in lootboxProperties if selected_item in k][0])
                    lootboxListAlt.remove(selected_item)
                    lootboxList = sorted(list(set(lootboxListAlt.copy())), key=keyforLootboxFilter)
                    equipmentListAlt.append(itemOpened)
                    equipmentList = sorted(list(set(equipmentListAlt.copy())), key=keyforWeaponsFilter, reverse=True)

                    showOpenResultWindow = Toplevel(root)
                    showOpenResultWindow.title('Open Result')
                    showOpenResultWindow.resizable(False, False)

                    rollingWindow.destroy()

                    showResultLabel1 = Label(showOpenResultWindow,
                                             text=f'You\'ve just discovered{"" if itemOpened in ["Leggings"] else " a"}{" pair of" if itemOpened in ["Boots"] else ""}{"n" if itemOpened[0] in "UEOAI" and itemOpened not in ["Boots", "Slippers"] else ""}...')
                    showResultLabel1.grid(row=3, column=3)

                    showResultLabel2 = Label(showOpenResultWindow, text=itemOpened, font=('Calibri', 16, 'bold'),
                                             foreground='#7609b5')
                    showResultLabel2.grid(row=4, column=3)

                    isLootboxOpened = False
                    savedata()
                    root.after(5000, lambda: showOpenResultWindow.destroy())

                if openProgressBar['value'] < 100:
                    openProgressBar['value'] += 1
                    openPercentShow.configure(text=f'Opening... ({int(openProgressBar["value"])}%)')
                    root.after(random.randint(10 * (lootboxList.index(selected_item) + 1),
                                              100 * (lootboxList.index(selected_item) + 1)), progress)
                else:
                    openPercentShow.configure(text=f'Processing...')
                    root.after(random.randint(1000, 2500), opened)

            lootboxWindow.destroy()
            rollingWindow = Toplevel(root)
            rollingWindow.title('Lootbox Opening')
            rollingWindow.resizable(False, False)

            mainRollingFrame = Frame(rollingWindow)
            mainRollingFrame.grid(row=3, column=3)

            openHeaderText = Label(mainRollingFrame, text=f'{selected_item}', font=('Calibri', 15, 'bold'))
            openHeaderText.grid(row=3, column=3)

            openPercentShow = Label(mainRollingFrame, text='Opening... (0%)')
            openPercentShow.grid(row=4, column=3)

            openProgressBar = ttk.Progressbar(mainRollingFrame, orient='horizontal', mode='determinate', length=250)
            openProgressBar.grid(row=5, column=3, sticky='ew', padx=3)

            root.after(1500, progress)
            rollingWindow.protocol("WM_DELETE_WINDOW", lambda: lootboxCallbackProtocol(rollingWindow))
        else:
            lootboxWindow.lift()

    def lootboxSelect(_):
        selected_indices = lootboxListbox.curselection()[0]
        selected_item = lootboxList[selected_indices]

        lootboxNameLabel.configure(
            text=f'{lootboxList[selected_indices]} {f"(x{lootboxListAlt.count(selected_item)})" if lootboxListAlt.count(selected_item) > 1 else ""}')
        lootboxOpenButton.configure(state=NORMAL)

    lootboxWindow = Toplevel(root)
    lootboxWindow.title('Lootbox')
    lootboxWindow.resizable(False, False)

    mainlootboxFrame = Frame(lootboxWindow)
    mainlootboxFrame.grid(row=3, column=3, padx=5, pady=5)

    Label(mainlootboxFrame, text=f'{username}\'s Lootboxes:', font=('Calibri', 18, 'bold')).grid(row=3, column=3,
                                                                                                 columnspan=3,
                                                                                                 pady=5)
    lootboxListbox = Listbox(mainlootboxFrame, listvariable=Variable(value=lootboxList), border=1,
                             selectmode=BROWSE,
                             font=('Calibri', 11, 'normal'))
    lootboxListbox.grid(row=5, column=3, rowspan=75, sticky='nsew')

    lootboxlistScrollbar = ttk.Scrollbar(mainlootboxFrame, orient=VERTICAL, command=lootboxListbox.yview)
    lootboxlistScrollbar.grid(row=5, column=4, rowspan=75, sticky='wns')
    lootboxListbox.configure(yscrollcommand=lootboxlistScrollbar.set)

    lootboxNameLabel = Label(mainlootboxFrame, text='N/A', font=('Calibri', 11, 'bold'))
    lootboxNameLabel.grid(row=5, column=5, sticky='n')
    lootboxOpenButton = Button(mainlootboxFrame, text='Open', state=DISABLED, command=openLootbox)
    lootboxOpenButton.grid(row=7, column=5, sticky='n')

    Button(mainlootboxFrame, text='Close', command=lambda: lootboxCallbackProtocol(lootboxWindow),
           background='red').grid(row=70,
                                  column=5,
                                  sticky='ew',
                                  padx=10)
    lootboxListbox.bind('<<ListboxSelect>>', lootboxSelect)
    lootboxWindow.protocol("WM_DELETE_WINDOW", lambda: lootboxCallbackProtocol(lootboxWindow))


def coinflip():
    global money, isCoinFlipOpened
    if isCoinFlipOpened or isHuntingOpened:
        return
    isCoinFlipOpened = True

    coinflipWindow = Toplevel(root)
    coinflipWindow.title('Coinflip')
    coinflipWindow.resizable(False, False)

    def cfCallbackProtocol(master):
        global isCoinFlipOpened
        isCoinFlipOpened = False
        master.destroy()

    def moneyInputBind(_):
        global moneyValue
        moneyValue = betMoneyInput.get()
        # moneyStripValue = moneyValue.replace('$', '')
        if moneyValue == '':
            betMoneyInput.insert(0, '$0')
        elif moneyValue == '$':
            betMoneyInput.insert(1, '0')
        elif '$' not in moneyValue:
            betMoneyInput.insert(0, '$')
        elif not moneyValue.isdigit():
            betMoneyInput.delete(0, END)
            betMoneyInput.insert(0,
                                 f'${"0" if moneyValue == "$" else str(int("".join([i for i in moneyValue if i.isdigit()])))}')

        if betMoneyInput.get().replace('$', '').isdigit() and int(
                betMoneyInput.get().replace('$', '')) <= money and 0 < int(betMoneyInput.get().replace('$', '')) <= 50000:
            flipcoinButton.configure(state=NORMAL)
        else:
            flipcoinButton.configure(state=DISABLED)

    def chooseFace():
        faceChoice = Toplevel(root)
        faceChoice.title('Head/Tail')
        faceChoice.resizable(False, False)

        coinflipWindow.destroy()

        def flipcoin():
            global money

            flipWindow = Toplevel(root)
            flipWindow.title('...')
            flipWindow.resizable(False, False)

            faceChosen = faceChoiceCombobox.get()
            faceChoice.destroy()

            def flipResult():
                global money, isCoinFlipOpened
                result = random.choice(['Head', 'Tail'])
                flipLabel.configure(
                    text=f'The coin spins... \"{result}\" and you {"won" if result == faceChosen else "lost"}')
                Label(flipWindow, text=f'${betValue}',
                      font=('Calibri', 16, 'bold'), foreground='#9c4051').grid(row=6, column=3)
                if result == faceChosen:
                    money += betValue * 2
                isCoinFlipOpened = False
                savedata()
                root.after(10000, lambda: flipWindow.destroy())

            betValue = int(moneyValue.replace('$', ''))
            money -= betValue

            flipLabel = Label(flipWindow, text=f'{username} has spent ${betValue} and chose {faceChosen}...')
            flipLabel.grid(row=3, column=3, pady=3, padx=5)
            root.after(2500, flipResult)

            flipWindow.protocol("WM_DELETE_WINDOW", lambda: cfCallbackProtocol(flipWindow))

        Label(faceChoice, text='Please select a face:').grid(row=3, column=3)

        faceChoiceCombobox = ttk.Combobox(faceChoice, values=['Head', 'Tail'], state='readonly')
        faceChoiceCombobox.grid(row=5, column=3, sticky='ew', padx=3)

        flipButton = Button(faceChoice, text='FLIP', command=flipcoin, state=DISABLED)
        flipButton.grid(row=7, column=3)

        def flipfaceValidator(_):
            if faceChoiceCombobox.get() == '':
                flipButton.configure(state=DISABLED)
            else:
                flipButton.configure(state=NORMAL)

        faceChoiceCombobox.bind('<<ComboboxSelected>>', flipfaceValidator)
        faceChoice.protocol("WM_DELETE_WINDOW", lambda: cfCallbackProtocol(faceChoice))

    mainCoinflipFrame = Frame(coinflipWindow)
    mainCoinflipFrame.grid(row=3, column=3)

    Label(mainCoinflipFrame, text=f'Coinflip', font=('Calibri', 18, 'bold')).grid(row=3, column=3, padx=35, pady=5)

    moneyShowLabel = Label(mainCoinflipFrame, text=f'Cash: ${money}')
    moneyShowLabel.grid(row=5, column=3)

    betMoneyInput = Entry(mainCoinflipFrame, justify=CENTER)
    betMoneyInput.insert(0, '$0')
    betMoneyInput.grid(row=7, column=3)

    flipcoinButton = Button(mainCoinflipFrame, text='Next', state=DISABLED, command=chooseFace)
    flipcoinButton.grid(row=10, column=3, pady=(0, 10))

    betMoneyInput.bind('<KeyRelease>', moneyInputBind)
    coinflipWindow.protocol("WM_DELETE_WINDOW", lambda: cfCallbackProtocol(coinflipWindow))


def buy():
    global isBuyOpened
    if isBuyOpened:
        return
    isBuyOpened = True

    def buyCallbackProtocol(master):
        global isBuyOpened
        isBuyOpened = False
        master.destroy()

    def buySelect(_):
        selected_indices = buyListbox.curselection()[0]
        selected_item = buyList[selected_indices]

        buyNameLabel.configure(text=f'{selected_item}')
        costLabel.configure(text=f'Cost: ${lootboxPrices[selected_item]}')
        lootboxPropertiesButton.configure(state=NORMAL)
        buyLootboxButton.configure(state=NORMAL)

    def buyLootboxProperties():

        def viewBuyLootboxPropertiesSelect(_):
            equipment_selected_indices = viewBuyLootboxPropertiesListbox.curselection()[0]
            equipment_selected_item = equipmentBuyList[equipment_selected_indices]

            viewBuyLootboxPropertiesNameLabel.configure(
                text=f'{equipment_selected_item}')
            viewBuyLootboxPropertiesInfoLabel.configure(
                text=f'Total: +{[k[1] for k in equipmentProperties if equipment_selected_item in k][0]}%')

        viewBuyLootboxPropertiesWindow = Toplevel(root)
        viewBuyLootboxPropertiesWindow.title('Properties')
        viewBuyLootboxPropertiesWindow.resizable(False, False)

        mainviewBuyLootboxPropertiesFrame = Frame(viewBuyLootboxPropertiesWindow)
        mainviewBuyLootboxPropertiesFrame.grid(row=3, column=3, padx=5, pady=5)

        Label(mainviewBuyLootboxPropertiesFrame, text=f'{buyList[buyListbox.curselection()[0]]} Properties:',
              font=('Calibri', 18, 'bold')).grid(row=3, column=3,
                                                 columnspan=3,
                                                 pady=5)
        equipmentBuyList = sorted([k[1] for k in lootboxProperties if buyList[buyListbox.curselection()[0]] in k][0],
                                  key=keyforWeaponsFilter)
        viewBuyLootboxPropertiesListbox = Listbox(mainviewBuyLootboxPropertiesFrame,
                                                  listvariable=Variable(value=equipmentBuyList), border=1,
                                                  selectmode=BROWSE,
                                                  font=('Calibri', 11, 'normal'))
        viewBuyLootboxPropertiesListbox.grid(row=5, column=3, rowspan=75, sticky='nsew')

        viewBuyLootboxPropertieslistScrollbar = ttk.Scrollbar(mainviewBuyLootboxPropertiesFrame, orient=VERTICAL,
                                                              command=viewBuyLootboxPropertiesListbox.yview)
        viewBuyLootboxPropertieslistScrollbar.grid(row=5, column=4, rowspan=75, sticky='wns')
        viewBuyLootboxPropertiesListbox.configure(yscrollcommand=viewBuyLootboxPropertieslistScrollbar.set)

        viewBuyLootboxPropertiesNameLabel = Label(mainviewBuyLootboxPropertiesFrame, text='N/A',
                                                  font=('Calibri', 11, 'bold'))
        viewBuyLootboxPropertiesNameLabel.grid(row=5, column=5, sticky='n')
        viewBuyLootboxPropertiesInfoLabel = Label(mainviewBuyLootboxPropertiesFrame, text='Total: +...%')
        viewBuyLootboxPropertiesInfoLabel.grid(row=7, column=5, sticky='n')

        Button(mainviewBuyLootboxPropertiesFrame, text='Close',
               command=lambda: viewBuyLootboxPropertiesWindow.destroy(),
               background='red').grid(row=70,
                                      column=5,
                                      sticky='ew',
                                      padx=10)
        viewBuyLootboxPropertiesListbox.bind('<<ListboxSelect>>', viewBuyLootboxPropertiesSelect)
        root.after(30000, lambda: viewBuyLootboxPropertiesWindow.destroy())

    def buyLootbox():
        lootboxName = buyList[buyListbox.curselection()[0]]

        buyLootboxWindow = Toplevel()
        buyLootboxWindow.title(f'Purchase {lootboxName} (1)')
        buyLootboxWindow.resizable(False, False)

        def amountValidator(item):
            if item == '' or item.isdigit() and 0 < int(item) < 100:
                return True
            else:
                return False

        def checkValue(event):
            buyLootboxWindow.focus()
            item = amountGet.get().strip()
            print('Ok?', item)
            if item == '':
                amountGet.insert(0, '1')
            elif item.isdigit() and int(item) > 1:
                buyLootboxWindow.title(f'Purchase {lootboxName}es ({item})')
            else:
                buyLootboxWindow.title(f'Purchase {lootboxName} (1)')

            if event:
                amountGet.focus()

        amountValidReg = buyLootboxWindow.register(amountValidator)

        Label(buyLootboxWindow, text=f'Lootbox Purchase ', font=('Calibri', 28, 'bold')).grid(row=3, column=3, padx=10)
        Label(buyLootboxWindow, text=f'({lootboxName})', font=('Calibri', 15, 'bold')).grid(row=4, column=3)
        amountGet = ttk.Spinbox(buyLootboxWindow, from_=1, to=99, command=lambda: checkValue(0), width=4,
                                validate='key',
                                validatecommand=(amountValidReg,
                                                 '%P'))  # validate='key', validatecommand=(amountValidReg, '%P'), command=checkValue)
        amountGet.set(1)
        amountGet.grid(row=5, column=3)

        amountGet.bind('<KeyRelease>', checkValue)

    buyWindow = Toplevel(root)
    buyWindow.title('Buy')
    buyWindow.resizable(False, False)

    mainbuyFrame = Frame(buyWindow)
    mainbuyFrame.grid(row=3, column=3, padx=5, pady=5)

    Label(mainbuyFrame, text=f'Buy Lootboxes', font=('Calibri', 18, 'bold')).grid(row=3, column=3, columnspan=3, pady=5)
    buyList = [k[0] for k in lootboxProperties]
    buyListbox = Listbox(mainbuyFrame, listvariable=Variable(value=buyList), border=1, selectmode=BROWSE,
                         font=('Calibri', 11, 'normal'))
    buyListbox.grid(row=5, column=3, rowspan=75, sticky='nsew')

    buylistScrollbar = ttk.Scrollbar(mainbuyFrame, orient=VERTICAL, command=buyListbox.yview)
    buylistScrollbar.grid(row=5, column=4, rowspan=75, sticky='wns')
    buyListbox.configure(yscrollcommand=buylistScrollbar.set)

    buyNameLabel = Label(mainbuyFrame, text=f'N/A', font=('Calibri', 11, 'bold'))
    buyNameLabel.grid(row=5, column=5, sticky='n')
    costLabel = Label(mainbuyFrame, text=f'Cost: $0')
    costLabel.grid(row=7, column=5, sticky='n')
    lootboxPropertiesButton = Button(mainbuyFrame, text='Properties', state=DISABLED, width=9,
                                     command=buyLootboxProperties)
    lootboxPropertiesButton.grid(row=9, column=5, pady=(3, 0))
    buyLootboxButton = Button(mainbuyFrame, text='Buy', state=DISABLED, width=9, command=buyLootbox)
    buyLootboxButton.grid(row=11, column=5)

    Button(mainbuyFrame, text='Close', command=lambda: buyCallbackProtocol(buyWindow), background='red').grid(
        row=70, column=5,
        sticky='ew',
        padx=10)
    buyListbox.bind('<<ListboxSelect>>', buySelect)
    buyWindow.protocol("WM_DELETE_WINDOW", lambda: buyCallbackProtocol(buyWindow))


def hunt():
    global isHuntingOpened, money
    if isHuntingOpened or isCoinFlipOpened:
        return
    isHuntingOpened = True

    def huntingCallbackProtocol(master):
        global isHuntingOpened
        isHuntingOpened = False
        master.destroy()

    huntWindow = Toplevel(root)
    huntWindow.title('Hunt')
    huntWindow.resizable(False, False)

    def huntPet():
        petHuntingProgressWindow = Toplevel()
        petHuntingProgressWindow.title('Hunting...')
        petHuntingProgressWindow.resizable(False, False)
        huntWindow.destroy()

        def showHuntResult():
            global money, petListAlt, petList, isHuntingOpened
            huntResultWindow = Toplevel()
            huntResultWindow.title('Hunting Result')
            huntResultWindow.resizable(False, False)
            petHuntingProgressWindow.destroy()

            money -= 5
            huntingResult = \
                random.choices([x[0] for x in petsProperties], weights=list(range(1, len(petsProperties) + 1)))[0]
            petListAlt.append(huntingResult)
            petList = sorted(list(set(petListAlt.copy())), key=keyforPetsFilter, reverse=True)

            showResultLabel1 = Label(huntResultWindow,
                                     text=f'You spent $5 and caught a{"n" if huntingResult[0] in "UEOAI" else ""}...')
            showResultLabel1.grid(row=3, column=3)

            showResultLabel2 = Label(huntResultWindow, text=huntingResult, font=('Calibri', 16, 'bold'),
                                     foreground='#2b5580')
            showResultLabel2.grid(row=4, column=3)

            isHuntingOpened = False
            savedata()
            root.after(5000, lambda: huntResultWindow.destroy())

        def huntingProgress():
            if huntingProgressbar['value'] < 100:
                showHuntingProgression.configure(text=f'Hunting for it... ({int(huntingProgressbar["value"])}%)')
                huntingProgressbar['value'] += random.randint(1, 3)
                root.after(random.randint(10, 250), huntingProgress)
            else:
                showHuntingProgression.configure(text=f'Processing... (100%)')
                root.after(random.randint(1000, 2500), showHuntResult)

        showHuntingProgression = Label(petHuntingProgressWindow, text='Looking for a good pet... (0%)')
        huntingProgressbar = ttk.Progressbar(petHuntingProgressWindow, orient='horizontal', length=250)
        showHuntingProgression.grid(row=3, column=3, pady=(3, 0))
        huntingProgressbar.grid(row=5, column=3, padx=10, pady=5)

        root.after(random.randint(500, 1500), huntingProgress)
        petHuntingProgressWindow.protocol("WM_DELETE_WINDOW", lambda: huntingCallbackProtocol(petHuntingProgressWindow))

    Label(huntWindow, text='Hunting', font=('Calibri', 25, 'bold')).grid(row=3, column=3, sticky='nsew', pady=10)
    Label(huntWindow,
          text=f'{"Start hunting by pressing on the below button:" if money >= 5 else "Not enough money. You need to go and get a real job:"}',
          font=('Calibri', 10, 'normal')).grid(row=5, column=3, sticky='nsew', padx=10)
    # noinspection PyTypeChecker
    huntButton = Button(huntWindow, text=f'{"Hunt (-$5)" if money >= 5 else "Go get a job"}', width=15, command=huntPet,
                        state=f'{"disable" if money < 5 else "normal"}')
    huntButton.grid(row=7, column=3, pady=(10, 15))

    huntWindow.protocol("WM_DELETE_WINDOW", lambda: huntingCallbackProtocol(huntWindow))


# # MANAGEMENT
manageFrame = Frame(menuFrame)
manageFrame.grid(row=3, column=3)

manageText = Label(manageFrame, text='Management', font=('Calibri', 15, 'bold'))
manageText.grid(row=3, column=3, pady=5)

# # # Pets
petButton = Button(manageFrame, text='Pets', width=10, command=pet)
petButton.grid(row=4, column=2, padx=10)

# # # Equipment
equipmentButton = Button(manageFrame, text='Equipment', width=10, command=equipment)
equipmentButton.grid(row=4, column=3, padx=10)

# # # Lootbox
lootboxButton = Button(manageFrame, text='Lootbox', width=10, command=lootbox)
lootboxButton.grid(row=4, column=4, padx=10)

# ttk.Separator(menuFrame, orient='horizontal').grid(row=5, column=3, sticky='ew', pady=15, padx=10)
# # GAMBLING
gamblingFrame = Frame(menuFrame)
gamblingFrame.grid(row=6, column=3)

gamblingText = Label(gamblingFrame, text='Gambling', font=('Calibri', 15, 'bold'))
gamblingText.grid(row=3, column=3, pady=5)

# # # Coinflip
coinflipButton = Button(gamblingFrame, text='Coinflip', width=10, command=coinflip)
coinflipButton.grid(row=4, column=2, padx=14)

# # # Slots
slotButton = Button(gamblingFrame, text='Slots', width=10)
slotButton.grid(row=4, column=3, padx=14)

# # # Lottery
lotteryButton = Button(gamblingFrame, text='Lottery', width=10)
lotteryButton.grid(row=4, column=4, padx=14)

# ttk.Separator(menuFrame, orient='horizontal').grid(row=7, column=3, sticky='ew', pady=15, padx=10)
# # ECONOMY
economyFrame = Frame(menuFrame)
economyFrame.grid(row=8, column=3)

economyText = Label(economyFrame, text='Economy', font=('Calibri', 15, 'bold'))
economyText.grid(row=3, column=3, pady=5)

# # # Shop
buyButton = Button(economyFrame, text='Shop', width=10)
buyButton.grid(row=4, column=2, padx=14)

# # # Currency
cashButton = Button(economyFrame, text='Currency', width=10)
cashButton.grid(row=4, column=3, padx=14)

# # # Buy
dailyButton = Button(economyFrame, text='Buy', width=10, command=buy)
dailyButton.grid(row=4, column=4, padx=14)

# # ACTION
actionFrame = Frame(root)
actionFrame.grid(row=10, column=3)

actionText = Label(actionFrame, text='Action', font=('Calibri', 15, 'bold'))
actionText.grid(row=3, column=3, pady=5)

# # # Hunting
huntingButton = Button(actionFrame, text='Hunt', width=10, command=hunt)
huntingButton.grid(row=4, column=2, padx=14)

# # # Battle
battleButton = Button(actionFrame, text='Battle', width=10)
battleButton.grid(row=4, column=3, padx=14)

# # # Giveaway
giveawayButton = Button(actionFrame, text='Giveaway', width=10)
giveawayButton.grid(row=4, column=4, padx=14)

Label(actionFrame, font=('Verdana', 7, 'normal')).grid(row=10, columnspan=100)
ttk.Separator(actionFrame, orient='horizontal').grid(row=11, columnspan=100, sticky='new')
# # USER
userFrame = Frame(root)
userFrame.grid(row=12, column=3)

userText = Label(userFrame, text='User', font=('Calibri', 16, 'bold'), foreground='#440f63')
userText.grid(row=3, column=2, pady=5, columnspan=2)

# # # Profile
profileButton = Button(userFrame, text='Profile', width=10)
profileButton.grid(row=4, column=2, padx=14)

# # # Profile
settingButton = Button(userFrame, text='Setting', width=10)
settingButton.grid(row=4, column=3, padx=14)

Label(root, font=('Verdana', 2, 'normal')).grid(row=99, columnspan=100)
ttk.Separator(root, orient='horizontal').grid(row=100, columnspan=100, sticky='ew')
Label(root, text=f'~ Phan Thanh Hung ~', font=('Verdana', 7, 'bold')).grid(row=100, columnspan=100)
Label(root, text=f'{project_name}', font=('Verdana', 10, 'bold'), foreground='#0b103d').grid(row=101, columnspan=100)


def askExit():
    if messagebox.askyesno(f'{project_name} {version}', f'Are you sure to quit {project_name} {version} ?',
                           icon='warning'):
        savedata(True)
        root.destroy()


root.protocol("WM_DELETE_WINDOW", askExit)
mainloop()
