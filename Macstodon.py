"""Macstodon - a Mastodon client for classic Mac OSMIT LicenseCopyright (c) 2022 Scott Small and ContributorsPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associateddocumentation files (the "Software"), to deal in the Software without restriction, including without limitation therights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permitpersons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of theSoftware.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THEWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS ORCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OROTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""## macfreeze: path Software:Programming:Python 1.5.2c1:Mac:Tools:IDE# macfreeze: exclude msvcrt# macfreeze: exclude SOCKS# macfreeze: exclude TERMIOS# macfreeze: exclude termios# macfreeze: exclude _imaging_gif## ################################# Splash Screen - hooks the import# process, so import it first # ################################import MacstodonSplash# ############### Python Imports # ##############import AE, AppleEventsimport FrameWorkimport macfsimport MacOSimport macostoolsimport osimport W, Wapplicationfrom MacPrefs import kOnSystemDisk# ########### My Imports# ##########from MacstodonConstants import DEBUG, VERSIONfrom MacstodonHelpers import okDialogfrom AuthHandler import AuthHandlerfrom ImageHandler import ImageHandlerfrom TimelineHandler import TimelineHandlerfrom TootHandler import TootHandler# ############ Application# ###########class Macstodon(Wapplication.Application):    """    The application itself.    """    # Creator type of this application    MyCreatorType = 'M$dN'    # Location of prefs in Preferences Folder    preffilepath = ":Macstodon Preferences"    # ########################    # Initialization Functions    # ########################    def __init__(self):        """        Run when the application launches.        """        Wapplication.Application.__init__(self, self.MyCreatorType)        # All applications should handle these Apple Events,        #  but you'll need an aete resource.        AE.AEInstallEventHandler(            # We're already open            AppleEvents.kCoreEventClass,            AppleEvents.kAEOpenApplication,             self.ignoreevent        )        AE.AEInstallEventHandler(            # No printing in this app            AppleEvents.kCoreEventClass,            AppleEvents.kAEPrintDocuments,            self.ignoreevent        )        AE.AEInstallEventHandler(            # No opening documents in this app            AppleEvents.kCoreEventClass,            AppleEvents.kAEOpenDocuments,             self.ignoreevent        )        AE.AEInstallEventHandler(            AppleEvents.kCoreEventClass,            AppleEvents.kAEQuitApplication,             self.quitevent        )        # Splash Screen        MacstodonSplash.wait()        MacstodonSplash.uninstall_importhook()        # Create image cache folders        # While the Wapplication framework creates the Macstodon Preferences file        # automatically, we have to create the cache folder on our own        vrefnum, dirid = macfs.FindFolder(kOnSystemDisk, 'pref', 0)        prefsfolder_fss = macfs.FSSpec((vrefnum, dirid, ''))        prefsfolder = prefsfolder_fss.as_pathname()        path = os.path.join(prefsfolder, ":Macstodon Cache")        acctpath = os.path.join(prefsfolder, ":Macstodon Cache:account")        mediapath = os.path.join(prefsfolder, ":Macstodon Cache:media")        macostools.mkdirs(path)        macostools.mkdirs(acctpath)        macostools.mkdirs(mediapath)        self.cachefolderpath = path        self.cacheacctfolderpath = acctpath        self.cachemediafolderpath = mediapath        # Init handlers        self.authhandler = AuthHandler(self)        self.imagehandler = ImageHandler(self)        self.timelinehandler = TimelineHandler(self)        self.toothandler = TootHandler(self)        # Open login window        self.loginwindow = self.authhandler.getLoginWindow()        self.loginwindow.open()        # Process some events!        self.mainloop()    def mainloop(self, mask=FrameWork.everyEvent, wait=0):        """        Modified version of Wapplication.mainloop() that removes        the debugging/traceback window.        """        self.quitting = 0        saveyield = MacOS.EnableAppswitch(-1)        try:            while not self.quitting:                try:                    self.do1event(mask, wait)                except W.AlertError, detail:                    MacOS.EnableAppswitch(-1)                    W.Message(detail)                except self.DebuggerQuit:                    MacOS.EnableAppswitch(-1)                except:                    if DEBUG:                        MacOS.EnableAppswitch(-1)                        import PyEdit                        PyEdit.tracebackwindow.traceback()                    else:                        raise        finally:            MacOS.EnableAppswitch(1)    def makeusermenus(self):        """        Set up menu items which all applications should have.        Apple Menu has already been set up.        """        # File menu        m = Wapplication.Menu(self.menubar, "File")        quititem = FrameWork.MenuItem(m, "Quit", "Q", 'quit')        # Edit menu        m = Wapplication.Menu(self.menubar, "Edit")        undoitem = FrameWork.MenuItem(m, "Undo", 'Z', "undo")        FrameWork.Separator(m)        cutitem = FrameWork.MenuItem(m, "Cut", 'X', "cut")        copyitem = FrameWork.MenuItem(m, "Copy", "C", "copy")        pasteitem = FrameWork.MenuItem(m, "Paste", "V", "paste")        clearitem = FrameWork.MenuItem(m, "Clear", None,  "clear")        FrameWork.Separator(m)        selallitem = FrameWork.MenuItem(m, "Select all", "A", "selectall")        # Any other menus would go here        # These menu items need to be updated periodically;        #   any menu item not handled by the application should be here,        #   as should any with a "can_" handler.        self._menustocheck = [            undoitem, cutitem, copyitem, pasteitem, clearitem, selallitem        ]    # no window menu, so pass    def checkopenwindowsmenu(self):        pass    # ##############################    # Apple Event Handling Functions    # ##############################    def ignoreevent(self, theAppleEvent, theReply):        """        Handler for events that we want to ignore        """        pass    def quitevent(self, theAppleEvent, theReply):        """        System is telling us to quit        """        self._quit()    # #######################    # Menu Handling Functions    # #######################    def do_about(self, id, item, window, event):        """        User selected "About" from the Apple menu        """        MacstodonSplash.about()    def domenu_quit(self):        """        User selected "Quit" from the File menu        """        self._quit()# Run the appMacstodon()