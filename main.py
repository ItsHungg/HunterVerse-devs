from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import random
import time

project_name = 'HunterVerse'
version = '0.9.2.1'
version_code = sum(list(map(int, version.split('.'))))
root = Tk()
root.resizable(False, False)
root.title(f'{project_name} {version}')
root.withdraw()

with open('hunterverse\\assets\\user\\userdata.txt', 'r') as userget:
    if userget.read().strip() != '':
        register_need = False
    else:
        register_need = True


def register():
    registerPage = Toplevel(root)
    registerPage.title('Registration')
    registerPage.resizable(False, False)

    def registerCallback(_):
        maximunUsernameLengthLabel.configure(text=f'{len(usernameEntry.get())}/10')
        if any(i in '`-=[]\\;\',./~!@#$%^&*()_+{}|:\"<>?' for i in usernameEntry.get()) or usernameEntry.get().isdigit() or not 3 <= len(
                usernameEntry.get()) <= 10:
            submitregisterButton.configure(state=DISABLED)
            if len(usernameEntry.get()) == 0:
                maximunUsernameLengthLabel.configure(foreground='black')
            else:
                maximunUsernameLengthLabel.configure(foreground='#a60a0a')
        else:
            submitregisterButton.configure(state=NORMAL)
            maximunUsernameLengthLabel.configure(foreground='black')

    def submitRegister():
        submitregisterButton.configure(state=DISABLED)
        usernameEntry.configure(state=DISABLED)
        with open('hunterverse\\assets\\user\\userdata.txt', 'w') as saveRegister:
            saveRegister.write(
                f'{usernameEntry.get()}.{time.strftime("%m-%d-%Y")}.{time.strftime("%T")}.{int(time.time())}')

        Label(registerPage, text='Processing...', font=('Calibri', 11, 'bold')).grid(row=10, column=3, columnspan=3, pady=5)
        root.after(random.randint(2500, 5000), lambda: [registerPage.destroy(), loadingProcess()])

    def quitRegister():
        if messagebox.askyesno('Quit Registration', 'Are you sure to cancel the registration progress?'):
            root.destroy()
    
    mainregisterFrame = Frame(registerPage)
    mainregisterFrame.grid(row=3, column=3)

    registerHeader = Label(mainregisterFrame, text='Register', font=('Calibri', 15, 'bold'))
    registerHeader.grid(row=3, column=3, columnspan=4)

    Label(mainregisterFrame, text='Username: ').grid(row=5, column=4)
    usernameEntry = Entry(mainregisterFrame)
    usernameEntry.grid(row=5, column=5)

    maximunUsernameLengthLabel = Label(mainregisterFrame, text='0/10')
    maximunUsernameLengthLabel.grid(row=5, column=6)

    submitregisterButton = Button(mainregisterFrame, text='Register', state=DISABLED, command=submitRegister)
    submitregisterButton.grid(row=9, column=3, columnspan=4)

    registerPage.protocol("WM_DELETE_WINDOW", quitRegister)
    usernameEntry.bind('<KeyRelease>', registerCallback)


def temp():
    pass


def loadingProcess():
    global username

    mainProgressWindow = Toplevel(root)
    mainProgressWindow.title('Initialization')
    mainProgressValueLabel = Label(mainProgressWindow, text='Initializing... (0%)', font=('Calibri', 11, 'bold'))
    mainProgressValueLabel.grid(row=3, column=3, sticky='ew')
    mainProgressWindow.resizable(False, False)

    with open('hunterverse\\assets\\user\\userdata.txt', 'r') as setUsername:
        username = setUsername.read().strip().split('.')[0]

    def startInit():
        global repeatMainProgress
        if mainProgressbar['value'] < 100:
            mainProgressbar['value'] += 1
            mainProgressValueLabel.configure(text=f'Initializing... ({int(mainProgressbar["value"])}%)')
            repeatMainProgress = root.after(random.randint(10, 500), startInit)
        else:
            mainProgressValueLabel.configure(text=f'Successfully run: {project_name} {version}')
            root.after(random.randint(2500, 5000), lambda: [root.deiconify(), mainProgressWindow.destroy()])

    mainProgressbar = ttk.Progressbar(mainProgressWindow, orient='horizontal', mode='determinate', length=300)
    mainProgressbar.grid(row=4, column=3, sticky='ew')

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
            del repeatMainProgress

    mainProgressWindow.protocol("WM_DELETE_WINDOW", temp)


if register_need:
    register()
else:
    loadingProcess()

# DECLARATION


def average(*args):
    return sum(args) / len(args)


def keyforPetsFilter(x: str):
    return int(average(int("".join([k[1][0] for k in petsProperties if x in k])),
                       int("".join([k[1][1] for k in petsProperties if x in k]))))


def keyforWeaponsFilter(x: str):
    return int("".join([k[1] for k in equipmentsProperties if x in k])), int(
        "".join([k[1] for k in equipmentsProperties if x in k]))


def keyforLootboxFilter(x: str):
    sortedLootbox = ['Basic Lootbox', 'Silver Lootbox', 'Copper Lootbox', 'Iron Lootbox', 'Golden Lootbox',
                     'Diamond Lootbox', 'Emerald Lootbox', 'Special Lootbox']
    return sortedLootbox.index(x)


# # Pets DECLARATION
petsPropertiesString = '''
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
'''

petsProperties = [[i.split('.')[0], i.split('.')[1].split(':')] for i in petsPropertiesString.split('\n') if i != '']
petListAlt = []
petList = sorted(list(set(petListAlt.copy())), key=keyforPetsFilter, reverse=True)
# petList = sorted([x[0] for x in petsProperties], key=keyforPetsFilter, reverse=True)

# # Equipments DECLARATION
equipmentsPropertiesString = '''
Sword.10
Hammer.10
Axe.15
Knife.3
Spear.7
Crossbow.7
Bow.5
Helmet.25
Armor.30
Leggings.20
Boots.10
Strength Poison 1.10
Strength Poison 2.15
Strength Poison 3.25
'''

equipmentsProperties = [[i.split('.')[0], i.split('.')[1]] for i in equipmentsPropertiesString.split('\n') if i != '']
equipmentListAlt = []
equipmentList = sorted(list(set(equipmentListAlt.copy())), key=keyforWeaponsFilter, reverse=True)

# # Lootbox DECLARATION
lootboxPropertiesString = '''
Basic Lootbox.Knife:Bow:Spear
Silver Lootbox.Knife:Bow:Crossbow:Spear:Sword
Copper Lootbox.Knife:Bow:Crossbow:Spear:Sword:Hammer
Iron Lootbox.Knife:Bow:Crossbow:Spear:Sword:Hammer:Strength Poison 1
Golden Lootbox.Bow:Crossbow:Spear:Sword:Hammer:Axe:Boots
Diamond Lootbox.Bow:Spear:Sword:Hammer:Axe:Boots:Leggings:Strength Poison 2
Emerald Lootbox.Sword:Hammer:Axe:Boots:Leggings:Armor:Helmet:Strength Poison 3
Special Lootbox.Axe:Boots:Leggings:Armor:Helmet:Strength Poison 1:Strength Poison 2:Strength Poison 3
'''
lootboxProperties = [[i.split('.')[0], i.split('.')[1].split(':')] for i in lootboxPropertiesString.split('\n') if
                     i != '']
lootboxListAlt = [n[0] for n in random.choices(lootboxProperties, k=15)]
lootboxList = sorted(list(set(lootboxListAlt.copy())), key=keyforLootboxFilter)

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
    global petList

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

    Button(mainpetFrame, text='Close', command=lambda: petWindow.destroy(), background='red', ).grid(row=70, column=5,
                                                                                                     sticky='ew',
                                                                                                     padx=10)
    petListbox.bind('<<ListboxSelect>>', petSelect)


def equipment():
    global equipmentList

    def equipmentSelect(_):
        selected_indices = equipmentListbox.curselection()[0]
        selected_item = equipmentList[selected_indices]

        equipmentNameLabel.configure(
            text=f'{selected_item} {f"(x{equipmentListAlt.count(selected_item)})" if equipmentListAlt.count(selected_item) > 1 else ""}')
        equipmentInfoLabel.configure(
            text=f'Total: +{"".join([k[1] for k in equipmentsProperties if selected_item in k])}%')

    equipmentWindow = Toplevel(root)
    equipmentWindow.title('Equipments')
    equipmentWindow.resizable(False, False)

    mainequipmentFrame = Frame(equipmentWindow)
    mainequipmentFrame.grid(row=3, column=3, padx=5, pady=5)

    Label(mainequipmentFrame, text=f'{username}\'s Equipments:', font=('Calibri', 18, 'bold')).grid(row=3, column=3,
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

    Button(mainequipmentFrame, text='Close', command=lambda: equipmentWindow.destroy(), background='red', ).grid(row=70,
                                                                                                                 column=5,
                                                                                                                 sticky='ew',
                                                                                                                 padx=10)
    equipmentListbox.bind('<<ListboxSelect>>', equipmentSelect)


def lootbox():
    global lootboxList

    def openLootbox():
        selected_index = lootboxListbox.curselection()[0]
        selected_item = lootboxList[selected_index]

        if messagebox.askyesno('Lootbox Open', f'Do you want to open {selected_item} (1)?'):
            def progress():
                def opened():
                    global equipmentList, lootboxList
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
                                             text=f'You\'ve just discovered a{" pair of" if itemOpened in ["Boots"] else ""}{"n" if itemOpened[0] in "UEOAI" and itemOpened not in ["Boots"] else ""}...')
                    showResultLabel1.grid(row=3, column=3)

                    showResultLabel2 = Label(showOpenResultWindow, text=itemOpened, font=('Calibri', 16, 'bold'),
                                             foreground='#7609b5')
                    showResultLabel2.grid(row=4, column=3)

                if openProgressBar['value'] < 100:
                    openProgressBar['value'] += 1
                    openPercentShow.configure(text=f'Opening... ({int(openProgressBar["value"])}%)')
                    root.after(random.randint(10, 100), progress)
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

            openProgressBar = ttk.Progressbar(mainRollingFrame, orient='horizontal', mode='determinate')
            openProgressBar.grid(row=5, column=3, sticky='ew')

            root.after(1500, progress)
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

    Button(mainlootboxFrame, text='Close', command=lambda: lootboxWindow.destroy(), background='red', ).grid(row=70,
                                                                                                             column=5,
                                                                                                             sticky='ew',
                                                                                                             padx=10)
    lootboxListbox.bind('<<ListboxSelect>>', lootboxSelect)


# # MANAGEMENT
manageFrame = Frame(menuFrame)
manageFrame.grid(row=3, column=3)

manageText = Label(manageFrame, text='Management', font=('Calibri', 15, 'bold'))
manageText.grid(row=3, column=3, pady=5)

# # # Pets
petButton = Button(manageFrame, text='Pets', width=10, command=pet)
petButton.grid(row=4, column=2, padx=10)

# # # Equipments
equipmentButton = Button(manageFrame, text='Equipments', width=10, command=equipment)
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
coinflipButton = Button(gamblingFrame, text='Coinflip', width=10)
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

# # # Buy/Shop
buyButton = Button(economyFrame, text='Shop', width=10)
buyButton.grid(row=4, column=2, padx=14)

# # # Currency
cashButton = Button(economyFrame, text='Currency', width=10)
cashButton.grid(row=4, column=3, padx=14)

# # # Daily
dailyButton = Button(economyFrame, text='Daily', width=10)
dailyButton.grid(row=4, column=4, padx=14)

# # ACTION
actionFrame = Frame(root)
actionFrame.grid(row=10, column=3)

actionText = Label(actionFrame, text='Action', font=('Calibri', 15, 'bold'))
actionText.grid(row=3, column=3, pady=5)

# # # Hunting
huntingButton = Button(actionFrame, text='Hunt', width=10)
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

# # # Statistics
statButton = Button(userFrame, text='Statistics', width=10)
statButton.grid(row=4, column=2, padx=14)

# # # Profile
profileButton = Button(userFrame, text='Profile', width=10)
profileButton.grid(row=4, column=3, padx=14)

Label(root, font=('Verdana', 2, 'normal')).grid(row=99, columnspan=100)
ttk.Separator(root, orient='horizontal').grid(row=100, columnspan=100, sticky='ew')
Label(root, text=f'~ Phan Thanh Hung ~', font=('Verdana', 7, 'bold')).grid(row=100, columnspan=100)
Label(root, text=f'{project_name}', font=('Verdana', 10, 'bold'), foreground='#0b103d').grid(row=101, columnspan=100)


def askExit():
    if messagebox.askyesno(f'{project_name} {version}', f'Are you sure to exit {project_name} {version} ?',
                           icon='warning'):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", askExit)
mainloop()
