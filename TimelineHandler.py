"""Macstodon - a Mastodon client for classic Mac OSMIT LicenseCopyright (c) 2022 Scott Small and ContributorsPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associateddocumentation files (the "Software"), to deal in the Software without restriction, including without limitation therights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permitpersons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of theSoftware.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THEWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS ORCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OROTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""# ############### Python Imports # ##############import Listsimport Qdimport reimport stringimport urllibimport W# #################### Third-Party Imports# ###################from third_party.BeautifulSoup import BeautifulSoup# ########### My Imports# ##########from MacstodonConstants import VERSIONfrom MacstodonHelpers import dprint, handleRequest, ImageWidget, okDialog, okCancelDialog, \    TitledEditText, TimelineList# ############ Application# ###########class TimelineHandler:    def __init__(self, app):        """        Initializes the TimelineHandler class.        """        self.app = app        self.defaulttext = "Click on a toot or notification in one of the above lists..."        self.timelines = {            "home": [],            "local": [],            "notifications": []        }    # #########################    # Window Handling Functions    # #########################    def getTimelineWindow(self):        """        Defines the Timeline window        """                # Set window size. Default to 600x400 which fits nicely in a 640x480 display.        # However if you're on a compact Mac that is 512x342, we need to make it smaller.        screenbounds = Qd.qd.screenBits.bounds        if screenbounds[2] <= 600 and screenbounds[3] <= 400:            bounds = (0, 20, 512, 342)        else:            bounds = (600, 400)        w = W.Window(bounds, "Macstodon %s - Timeline" % VERSION, minsize=(512, 342))        w.panes = W.HorizontalPanes((8, 8, -8, -20), (0.65, 0.3, 0.05))        w.panes.tlpanes = W.VerticalPanes(None, (0.34, 0.33, 0.33))        w.panes.tlpanes.home = TimelineList(None, "Home Timeline", self.timelines["home"], btnCallback=self.refreshHomeCallback, callback=self.homeClickCallback, flags=Lists.lOnlyOne)        w.panes.tlpanes.local = TimelineList(None, "Local Timeline", self.timelines["local"], btnCallback=self.refreshLocalCallback, callback=self.localClickCallback, flags=Lists.lOnlyOne)        w.panes.tlpanes.notifications = TimelineList(None, "Notifications", self.timelines["notifications"], btnCallback=self.refreshNotificationsCallback, callback=self.notificationClickCallback, flags=Lists.lOnlyOne)        w.panes.tootgroup = W.Group(None)        w.panes.tootgroup.toottxt = TitledEditText((56, 0, 0, 0), title="", text=self.defaulttext, readonly=1, vscroll=1)                # Avatar, reply/boost/favourite/bookmark buttons        # TODO: booster img        w.panes.tootgroup.authorimg = ImageWidget((0, 0, 48, 48))        w.panes.tootgroup.boosterimg = ImageWidget((24, 24, 24, 24))        w.panes.tootgroup.reply = W.EditText((4, 56, 16, 16), "R", readonly=1)        w.panes.tootgroup.boost = W.EditText((28, 56, 16, 16), "B", readonly=1)        w.panes.tootgroup.favrt = W.EditText((4, 80, 16, 16), "F", readonly=1)        w.panes.tootgroup.bmark = W.EditText((28, 80, 16, 16), "M", readonly=1)        w.panes.controlbtns = W.Group(None)        w.panes.controlbtns.logoutbutton = W.Button((56, 0, 80, 0), "Logout", self.timelineLogoutCallback)        w.panes.controlbtns.tootbutton = W.Button((-80, 0, 80, 0), "Post Toot", self.tootCallback)        return w    # ##################    # Callback Functions    # ##################    def timelineClickCallback(self, name):        """        Run when the user clicks somewhere in the named timeline        """        w = self.app.timelinewindow        if name == "home":            list = w.panes.tlpanes.home        elif name == "local":            list = w.panes.tlpanes.local        selected = list.getselection()        if len(selected) < 1:            w.panes.tootgroup.authorimg.clearImage()            w.panes.tootgroup.boosterimg.clearImage()            w.panes.tootgroup.toottxt.setTitle("")            w.panes.tootgroup.toottxt.set(self.defaulttext)            return        else:            index = selected[0]            toot = self.timelines[name][index]            self.formatAndDisplayToot(toot)    def homeClickCallback(self):        """        Run when the user clicks somewhere in the home timeline        """        self.timelineClickCallback("home")    def localClickCallback(self):        """        Run when the user clicks somewhere in the local timeline        """        self.timelineClickCallback("local")    def notificationClickCallback(self):        """        Run when the user clicks somewhere in the notification timeline        """        w = self.app.timelinewindow        list = w.panes.tlpanes.notifications        selected = list.getselection()        if len(selected) < 1:            w.panes.tootgroup.authorimg.clearImage()            w.panes.tootgroup.boosterimg.clearImage()            w.panes.tootgroup.toottxt.setTitle("")            w.panes.tootgroup.toottxt.set(self.defaulttext)            return        else:            index = selected[0]            notification = self.timelines["notifications"][index]            if notification["type"] in ["favourite", "reblog", "status", "mention", "poll", "update"]:                toot = notification["status"]                self.formatAndDisplayToot(toot)            else:                okDialog("Sorry, displaying the notification type '%s' is not supported yet" % notification["type"])                w.panes.tootgroup.authorimg.clearImage()                w.panes.tootgroup.boosterimg.clearImage()                w.panes.tootgroup.toottxt.setTitle("")                w.panes.tootgroup.toottxt.set(self.defaulttext)    def refreshHomeCallback(self, limit=None):        """        Run when the user clicks the Refresh button above the home timeline        """        self.updateTimeline("home", limit)        self.app.timelinewindow.panes.tlpanes.home.set(self.formatTimelineForList("home"))    def refreshLocalCallback(self, limit=None):        """        Run when the user clicks the Refresh button above the local timeline        """        self.updateTimeline("local", limit)        self.app.timelinewindow.panes.tlpanes.local.set(self.formatTimelineForList("local"))    def refreshNotificationsCallback(self, limit=None):        """        Run when the user clicks the Refresh button above the notifications timeline        """        self.updateTimeline("notifications", limit)        listitems = self.formatNotificationsForList()        self.app.timelinewindow.panes.tlpanes.notifications.set(listitems)    def timelineLogoutCallback(self):        """        Run when the user clicks the "Logout" button from the timeline window.        Just closes the timeline window and reopens the login window.        """        self.app.timelinewindow.close()        self.app.loginwindow = self.app.authhandler.getLoginWindow()        self.app.loginwindow.open()    def tootCallback(self):        """        Run when the user clicks the "Post Toot" button from the timeline window.        It opens up the toot window.        """        self.app.tootwindow = self.app.toothandler.getTootWindow()        self.app.tootwindow.open()    # ####################    # Formatting Functions    # ####################    def cleanUpUnicode(self, content):        """        Do the best we can to manually clean up unicode stuff        """        content = string.replace(content, "‚Ä¶", "...")        content = string.replace(content, "‚Äô", "'")        content = string.replace(content, "‚Ä§", ".")        content = string.replace(content, "‚Äî", "-")        content = string.replace(content, "‚Äú", '"')        content = string.replace(content, "‚Äù", '"')        content = string.replace(content, "&quot;", '"')        content = string.replace(content, "√©", "é")        content = string.replace(content, "√∂", "ö")        content = string.replace(content, "&#39;", "'")        content = string.replace(content, "&amp;", "&")        content = string.replace(content, "&gt;", ">")        content = string.replace(content, "&lt;", "<")        return content    def formatAndDisplayToot(self, toot):        """        Formats a toot for display and displays it in the bottom third        """        w = self.app.timelinewindow        # clear existing toot        w.panes.tootgroup.authorimg.clearImage()        w.panes.tootgroup.boosterimg.clearImage()        w.panes.tootgroup.toottxt.setTitle("")        w.panes.tootgroup.toottxt.set("Loading toot...")        display_name = toot["account"]["display_name"] or toot["account"]["username"]        display_name = self.cleanUpUnicode(display_name)        if toot["reblog"]:            image, iwidth, iheight = self.app.imagehandler.getImageFromURL(toot["reblog"]["account"]["avatar"], "account")            bimage, biwidth, biheight = self.app.imagehandler.getImageFromURL(toot["account"]["avatar"], "account")            reblog_display_name = toot["reblog"]["account"]["display_name"] or toot["reblog"]["account"]["username"]            reblog_display_name = self.cleanUpUnicode(reblog_display_name)            title = "%s boosted %s (%s)" % (display_name, reblog_display_name, toot["reblog"]["account"]["acct"])            content = toot["reblog"]["content"]            sensitive = toot["reblog"]["sensitive"]            spoiler_text = toot["reblog"]["spoiler_text"]        else:            image, iwidth, iheight = self.app.imagehandler.getImageFromURL(toot["account"]["avatar"], "account")            bimage, biwidth, biheight = None, None, None            title = "%s (%s)" % (display_name, toot["account"]["acct"])            content = toot["content"]            sensitive = toot["sensitive"]            spoiler_text = toot["spoiler_text"]        # Check for CW        if sensitive:            cwText = "This toot has a content warning. " \                "Press OK to view or Cancel to not view.\r\r%s"            try:                okCancelDialog(cwText % spoiler_text)            except KeyboardInterrupt:                w.panes.tootgroup.toottxt.set(self.defaulttext)                return        dprint(content)        # Replace HTML linebreak tags with actual linebreaks        content = string.replace(content, "<br>", "\r")        content = string.replace(content, "<br/>", "\r")        content = string.replace(content, "<br />", "\r")        content = string.replace(content, "<p>", "")        content = string.replace(content, "</p>", "\r\r")        content = self.cleanUpUnicode(content)        # Extract links        #soup = BeautifulSoup(content)        #links = soup("a")        #dprint("** ANCHORS **")        #dprint(links)        # Strip all other HTML tags        content = re.sub('<[^<]+?>', '', content)        # Render content into UI        w.panes.tootgroup.authorimg.setImage(image, iwidth, iheight)        if bimage:            w.panes.tootgroup.boosterimg.setImage(bimage, biwidth, biheight)        w.panes.tootgroup.toottxt.setTitle(title)        w.panes.tootgroup.toottxt.set(content)    def formatTimelineForList(self, name):        """        Formats toots for display in a timeline list        """        listitems = []        for toot in self.timelines[name]:            if toot["reblog"]:                if toot["reblog"]["sensitive"]:                    content = toot["reblog"]["spoiler_text"]                else:                    content = toot["reblog"]["content"]            else:                if toot["sensitive"]:                    content = toot["spoiler_text"]                else:                    content = toot["content"]                        content = self.cleanUpUnicode(content)                        # Replace linebreaks with spaces            content = string.replace(content, "<br>", " ")            content = string.replace(content, "<br/>", " ")            content = string.replace(content, "<br />", " ")            content = string.replace(content, "<p>", "")            content = string.replace(content, "</p>", " ")                        # Strip all other HTML tags            content = re.sub('<[^<]+?>', '', content)            display_name = toot["account"]["display_name"] or toot["account"]["username"]            display_name = self.cleanUpUnicode(display_name)            if toot["reblog"]:                reblog_display_name = toot["reblog"]["account"]["display_name"] or toot["reblog"]["account"]["username"]                reblog_display_name = self.cleanUpUnicode(reblog_display_name)                listitem = "%s boosted %s\r%s" % (display_name, reblog_display_name, content)            else:                listitem = "%s\r%s" % (display_name, content)            listitems.append(listitem)        return listitems    def formatNotificationsForList(self):        """        Formats notifications for display in a list        """        listitems = []        for notification in self.timelines["notifications"]:            display_name = notification["account"]["display_name"] or notification["account"]["username"]            if notification["type"] == "mention":                listitem = "%s mentioned you in their toot" % display_name            elif notification["type"] == "status":                listitem = "%s posted a toot" % display_name            elif notification["type"] == "reblog":                listitem = "%s boosted your toot" % display_name            elif notification["type"] == "follow":                listitem = "%s followed you" % display_name            elif notification["type"] == "follow_request":                listitem = "%s requested to follow you" % display_name            elif notification["type"] == "favourite":                listitem = "%s favourited your toot" % display_name            elif notification["type"] == "poll":                listitem = "%s's poll has ended" % display_name            elif notification["type"] == "update":                listitem = "%s updated their toot" % display_name            elif notification["type"] == "admin.sign_up":                listitem = "%s signed up" % display_name            elif notification["type"] == "admin.report":                listitem = "%s filed a report" % display_name            else:                # unknown type, ignore it, but print to console if debugging                dprint("Unknown notification type: %s" % notification["type"])            listitems.append(listitem)        return listitems    def updateTimeline(self, name, limit = None):        """        Pulls a timeline from the server and updates the global dicts                TODO: hashtags and lists        """        params = {}        if limit:            params["limit"] = limit        if len(self.timelines[name]) > 0:            params["min_id"] = self.timelines[name][0]["id"]        if name == "home":            path = "/api/v1/timelines/home"        elif name == "local":            path = "/api/v1/timelines/public"            params["local"] = "true"        elif name == "public":            # not currently used anywhere            path = "/api/v1/timelines/public"        elif name == "notifications":            path = "/api/v1/notifications"        else:            dprint("Unknown timeline name: %s" % name)            return        encoded_params = urllib.urlencode(params)        data = handleRequest(self.app, path + "?" + encoded_params, use_token=1)        if not data:            # handleRequest failed and should have popped an error dialog            return        # if data is a list, it worked        if type(data) == type([]):            for i in range(len(data)-1, -1, -1):                self.timelines[name].insert(0, data[i])        # if data is a dict, it failed        elif type(data) == type({}) and data.get("error") is not None:            okDialog("Server error when refreshing %s timeline:\r\r %s" % (name, data['error']))        # i don't think this is reachable, but just in case...        else:            okDialog("Server error when refreshing %s timeline. Unable to determine data type." % name)