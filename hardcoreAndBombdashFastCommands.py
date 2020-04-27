# -*- coding: utf-8 -*-
import bs
import bsUI
import bsInternal
import weakref

# writed by drov.drov

v = '0.0.03'

gPopupWindowColor = (0.45, 0.4, 0.55)

commands_bd = {'Russian': {'/kick': 'Кикнуть', '/ban': 'Забанить', 'account': 'Аккаунт', \
    '/thaw': 'Разморозить','/remove': 'Выгнать из игры','/box': 'Превратить в динамит',
    '/heal': 'Вылечить','/rainbow': 'Радужная подсветка','/sleep': 'Усыпить',\
    '/freeze': 'Заморозить','/rise': 'Возродить','/inv': 'Невидимость','/fly': 'Полет',\
    '/fly3d': 'Трехмерный полет','/kill': 'Убить','/curse': 'Проклятие',\
    '/gm': 'Режим бога','/sm': 'Замедленный режим игры','/nv': 'Ночь',
    '/ac r 30 40': 'Ac r','/frev': 'fref','/ref 3 5': 'ref','/io': 'io'}, \
    'English': {'/kick': 'Kick player', '/ban': 'Ban player', 'account': 'Player account', \
    '/thaw': 'Thaw','/remove': 'Remove from game','/box': 'Change skin to tnt',
    '/heal': 'Heal','/rainbow': 'Rainbow skin','/sleep': 'Sleep player',\
    '/freeze': 'Freeze player','/rise': 'Rise player','/inv': 'Invisibility',
     '/fly': 'Fly','/fly3d': '3D - Fly','/kill': 'Kill player','/curse': 'Curse player',\
    '/gm': 'God mode','/sm': 'Slow motion','/nv': 'Night', \
    '/ac r 30 40': 'Ac r','/frev': 'fref','/ref 3 5': 'ref','/io': 'io'}}

commands_bd = commands_bd.get(bs.getLanguage(), commands_bd.get("English", {}))
commands_bd_device_needed = []
commands_bd_nothing_needed = ['/ac r 30 40','/sm','/io','/ref 3 5','/nv']

data = {'skins': ['delete', 'bunny','bear','pixie','santa','tnt',\
    'shard','inv','bones','pirate','frosty','agent',\
    'taobao','wizard','penguin','ninja','cyborg','zoe',\
    'spaz','kronk','mel','warrior','lee','zola','butch',\
    'oldlady','middleman','gladiator','alien','wrestler',\
    'gretel','robot','witch','mcburton'], 'times': ['normal',\
    'sunrise','day','noon','sunset','night','cycle'], 'chunks': ['delete', \
    'ice', 'spark','metal','rock','slime','splinter','smoke'], \
    'emitters': ['stickers', 'distortion','tendrils','none']}

commands = ['/time','/sleep','/ph','/hp']
commands_account_needed = ['/kick','/ban','/admin','/vip','/df','/skin','/prefix','/mute','/unmute']
commands_number_needed = ['/kick','/ban','/frozen','/flex', \
    '/dance','/dance2','/admin','/vip','/df','/rise','/curse','/head','/skin']
commands_all = sorted(list(set(commands + commands_account_needed + commands_number_needed)))

popupMenuOld = bsUI.PopupMenuWindow
class PopupMenuWindow(popupMenuOld):
    def __init__(self, position, choices, currentChoice, delegate=None, width=230,
        maxWidth=None, scale=1.0, choicesDisabled=[],
        choicesDisplay=[], autoSelect=None, color = (0.35,0.55,0.15)):
        choicesDisplayNew = []
        for choice in choicesDisplay:
            if type(choice) is bs.Lstr:
                choicesDisplayNew.append(choice.evaluate())
            else:
                bs.printErrorOnce(
                    'PopupMenuWindow got a raw string in \'choicesDisplay\';'
                    ' please pass bs.Lstr values only')
                choicesDisplayNew.append(choice)
        choicesDisplay = choicesDisplayNew
        parent = None
        if maxWidth is None: maxWidth = width * 1.5
        self._transitioningOut = False
        self._choices = list(choices)
        self._choicesDisplay = list(choicesDisplay)
        self._currentChoice = currentChoice
        self._choicesDisabled = list(choicesDisabled)
        self._doneBuilding = False
        if len(choices) < 1:
            raise Exception("Must pass at least one choice")
        self._width = width
        self._scale = scale
        if len(choices) > 8:
            self._height = 280
            self._useScroll = True
        else:
            self._height = 20+len(choices)*33
            self._useScroll = False
        self._delegate = None  # dont want this stuff called just yet..

        # extend width to fit our longest string (or our max-width)
        for index, choice in enumerate(choices):
            if len(choicesDisplay) == len(choices):
                choiceDisplayName = choicesDisplay[index]
            else:
                choiceDisplayName = choice
            if self._useScroll:
                self._width = max(self._width, min(
                    maxWidth, bsInternal._getStringWidth(
                        choiceDisplayName, suppressWarning=True))+75)
            else:
                self._width = max(self._width, min(
                    maxWidth, bsInternal._getStringWidth(
                        choiceDisplayName, suppressWarning=True))+60)

        bsUI.PopupWindow.__init__(self, position, size=(self._width, self._height), scale=self._scale, bgColor = color)

        if self._useScroll:
            self._scrollWidget = bs.scrollWidget(
                parent=self._rootWidget, position=(20, 20),
                highlight=False, color=(0.35, 0.55, 0.15),
                size=(self._width - 40, self._height - 40))
            self._columnWidget = bs.columnWidget(parent=self._scrollWidget)
        else:
            self._offsetWidget = bs.containerWidget(
                parent=self._rootWidget, position=(30, 15),
                size=(self._width - 40, self._height),
                background=False)
            self._columnWidget = bs.columnWidget(parent=self._offsetWidget)
        for index, choice in enumerate(choices):
            if len(choicesDisplay) == len(choices):
                choiceDisplayName = choicesDisplay[index]
            else:
                choiceDisplayName = choice
            inactive = (choice in self._choicesDisabled)
            w = bs.textWidget(
                parent=self._columnWidget, size=(self._width - 40, 28),
                onSelectCall=bs.Call(self._select, index),
                clickActivate=True, color=(0.5, 0.5, 0.5, 0.5)
                if inactive
                else(
                    (0.5, 1, 0.5, 1)
                    if choice == self._currentChoice else(0.8, 0.8, 0.8, 1.0)),
                padding=0, maxWidth=maxWidth, text=choiceDisplayName,
                onActivateCall=self._activate, vAlign='center',
                selectable=False if inactive else True)
            if choice == self._currentChoice:
                bs.containerWidget(edit=self._columnWidget,
                                   selectedChild=w, visibleChild=w)

        # ok from now on our delegate can be called
        self._delegate = weakref.ref(delegate)
        self._doneBuilding = True

def get_number(clientID):
    roster, activity = bsInternal._getGameRoster(), bsInternal._getForegroundHostActivity()
    choices = []
    if len(roster) > 0:
        players_ids = []
        my_ids = [i['players'] for i in roster if i['clientID'] == clientID]
        my_ids = [i['id'] for i in my_ids[0]] if len(my_ids) > 0 else None
        dt = [[c["id"] for c in i["players"]] for i in roster]
        for i in dt:
            for d in i:
                players_ids.append(d)
        players_ids.sort()
        if len(my_ids) > 0: choices = [players_ids.index(i) for i in my_ids]
    elif activity is not None and hasattr(activity, 'players') and len(activity.players) > 0:
        for i in activity.players:
            if i.exists() and hasattr(i, 'getInputDevice') and i.getInputDevice().getClientID() == clientID:
                choices.append(activity.players.index(i))
    return choices

def get_account(clientID, full=True):
    roster, activity = bsInternal._getGameRoster(), bsInternal._getForegroundHostActivity()
    account = None
    if len(roster) > 0:
        for i in roster: 
            if i['clientID'] == clientID: 
                account = i['displayString'].decode('utf-8')
                break
    elif activity is not None and hasattr(activity, 'players') and len(activity.players) > 0:
        for i in activity.players:
            if i.exists() and hasattr(i, 'getInputDevice') and i.getInputDevice().getClientID() == clientID:
                account = i.getInputDevice()._getAccountName(True)
                break
    if not full and account is not None:
        for icon in ['googlePlusLogo', 'gameCenterLogo', 'gameCircleLogo', \
            'ouyaLogo', 'localAccount', 'alibabaLogo', \
            'oculusLogo', 'nvidiaLogo']: 
            ic = bs.getSpecialChar(icon)
            if ic in account: account = account.replace(ic, '')
    return account

def _popupWindow(self, choices=[], choicesDisplay=None, popupType=None):
    if popupType is not None: self._popupType = popupType
    return bsUI.PopupMenuWindow(position=getattr(self, 'popupMenuPosition', (0,0)),
        scale=2.3 if bsUI.gSmallUI else 1.65 if bsUI.gMedUI else 1.23,
        choices=choices,
        choicesDisplay=[bs.Lstr(value=i) for i in choices] if choicesDisplay is None else choicesDisplay,
        currentChoice=None,
        color=gPopupWindowColor,
        delegate=self)

def _onPartyMemberPress(self, clientID, isHost, widget):
    try:
        if bsInternal._getForegroundHostSession() is not None: choicesDisplay = [bs.Lstr(resource='kickText')] 
        else:
            if bsInternal._getConnectionToHostInfo().get('buildNumber', 0) < 14248: return
            choicesDisplay = [bs.Lstr(resource='kickVoteText')]
        choices = ['kick', 'hardcore', 'bombdash']
        for i in ['HardCore','BombDash']: choicesDisplay.append(bs.Lstr(value=i))
        self.popupMenuPosition = widget.getScreenSpaceCenter()
        bsUI.PopupMenuWindow(position=self.popupMenuPosition,
                        scale=2.3 if bsUI.gSmallUI else 1.65 if bsUI.gMedUI else 1.23,
                        choices=choices,
                        choicesDisplay=choicesDisplay,
                        currentChoice=None,
                        color=gPopupWindowColor,
                        delegate=self)
        self._popupType = 'partyMemberPress'
        self._popupPartyMemberClientID = clientID
        self._popupPartyMemberIsHost = isHost
    except Exception as E: bs.screenMessage(str(E))

def popupMenuSelectedChoice(self, popupWindow, choice):
    if choice in ['hardcore','bombdash'] and self._popupType != 'partyMemberPress': return
    hasID = hasattr(self, '_popupPartyMemberClientID')
    if not hasID or (hasID and self._popupPartyMemberClientID is None): self._popupPartyMemberClientID = -1
    if self._popupType == 'partyMemberPress':
        bs.textWidget(edit=self._textField, text='')
        if choice == 'hardcore': self._popupWindow(choices=commands_all, popupType='commands_hc')
        elif choice == 'bombdash': self._popupWindow(choices=commands_bd.keys(), choicesDisplay=[bs.Lstr(value=i) for i in commands_bd.values()], popupType='commands_bd')
    if self._popupType in ['commands_hc','commands_bd']:
        if choice in ['hardcore','bombdash']: return
        account, device = get_account(self._popupPartyMemberClientID), get_account(self._popupPartyMemberClientID, False)
        number = get_number(self._popupPartyMemberClientID)
        bs.textWidget(edit=self._textField, text='')
        if self._popupType == 'commands_hc':
            if choice in ['/sm','/list']: bs.textWidget(edit=self._textField, text=choice)
            elif choice == '/skin':
                if account is not None: self._popupWindow(choices=data.get("skins", ["delete", "spaz"]), popupType={'skins': account})
            elif choice == '/prefix':
                if account is not None: self._popupWindow(choices=data.get("chunks", ["spark", "delete"]), popupType={'prefixes': account})
            elif choice == '/time': 
                self._popupWindow(choices=data.get("times", ["normal","cycle"]), popupType='choice_number')
            elif choice in ['/sleep','/hp','/ph']:
                if len(number) > 0: self._popupWindow(choices=["0", "5", "10", "501", "99999999999"], popupType={choice: number})
                else: bs.textWidget(edit=self._textField, text='')
            elif choice in commands_account_needed:
                if account is not None: bs.textWidget(edit=self._textField, text=choice+' '+account)
            elif choice in commands_number_needed: 
                if len(number) > 0:
                    bs.textWidget(edit=self._textField, text=choice)
                    if len(number) > 1: self._popupWindow(choices=[str(i) for i in number], popupType='choice_number')
                    else: 
                        self._popupType = 'choice_number'
                        choice = str(number[0])
                else: bs.textWidget(edit=self._textField, text='')
        else:
            if choice in commands_bd_nothing_needed: bs.textWidget(edit=self._textField, text=choice)
            elif choice in ['account'] and account is not None: bs.screenMessage(account)
            elif choice in ['/kick', '/ban']: bs.textWidget(edit=self._textField, text=choice+' '+str(self._popupPartyMemberClientID))
            else: 
                if len(number) > 0:
                    bs.textWidget(edit=self._textField, text=choice)
                    if len(number) > 1: self._popupWindow(choices=[str(i) for i in number], popupType='choice_number')
                    else: 
                        self._popupType = 'choice_number'
                        choice = str(number[0])
                else: bs.textWidget(edit=self._textField, text='')
    if self._popupType == 'choice_number':  bs.textWidget(edit=self._textField, text=(bs.textWidget(query=self._textField)+' '+choice))
    if isinstance(self._popupType, dict):
        if len(self._popupType) > 0:
            key, vals = self._popupType.keys()[0], self._popupType.values()[0]
            if 'skins' in self._popupType and choice != '/skin': bs.textWidget(edit=self._textField, text=('/skin '+choice+' '+vals))
            elif 'prefixes' in self._popupType and choice != '/prefix':
                if choice == 'delete': bs.textWidget(edit=self._textField, text=('/prefix delete '+vals))
                else: self._popupWindow(choices=data.get("emitters", ["spark", "delete"]), popupType={'emitters': [vals, choice]})  
            elif 'emitters' in self._popupType and choice != '/prefix':
                bs.textWidget(edit=self._textField, text=('/prefix '+vals[0]+' '+vals[1]+' '+choice+' '))
            elif self._popupType.keys()[0] in ['/ph', '/hp', '/sleep'] and choice not in ['/ph', '/hp', '/sleep']:
                bs.textWidget(edit=self._textField, text=(key+' '+choice))
                if len(vals) > 1: self._popupWindow(choices=[str(i) for i in vals], popupType='choice_number')
                else: bs.textWidget(edit=self._textField, text=(bs.textWidget(query=self._textField)+' '+str(vals[0])))
    elif self._popupType not in ['choice_number','commands_hc','commands_bd','bombdash','hardcore']:
        self.popupMenuOld(popupWindow=popupWindow, choice=choice)

bsUI.PopupMenuWindow = PopupMenuWindow
bsUI.PartyWindow.popupMenuOld = bsUI.PartyWindow.popupMenuSelectedChoice
bsUI.PartyWindow.popupMenuSelectedChoice = popupMenuSelectedChoice
bsUI.PartyWindow._onPartyMemberPress = _onPartyMemberPress
bsUI.PartyWindow._popupWindow = _popupWindow