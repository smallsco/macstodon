"""Macstodon - a Mastodon client for classic Mac OSMIT LicenseCopyright (c) 2022-2023 Scott Small and ContributorsPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associateddocumentation files (the "Software"), to deal in the Software without restriction, including without limitation therights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permitpersons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of theSoftware.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THEWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS ORCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OROTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""# ############### Python Imports # ##############import reimport stringimport W# ########### My Imports# ##########from MacstodonConstants import VERSIONfrom MacstodonHelpers import cleanUpUnicode, dprint, handleRequest, okDialog, TitledEditText# ############ Application# ###########class TootHandler:    def __init__(self, app):        """        Initializes the TootHandler class.        """        self.app = app        self.replyToID = None        self.visibility = "public"    # #########################    # Window Handling Functions    # #########################    def getTootWindow(self, replyTo=None):        """        Defines the Toot window.        """        prefs = self.app.getprefs()        if not prefs.max_toot_chars:            prefs.max_toot_chars = self.getMaxTootChars()            prefs.save()        tootwindow = W.Dialog((320, 210), "Macstodon %s - Toot" % VERSION)        heading = "Type your toot below (max %s characters):" % prefs.max_toot_chars        if replyTo:            self.replyToID = replyTo["id"]            title = "Replying to %s:" % replyTo["account"]["acct"]            text = "@%s " % replyTo["account"]["acct"]            content = replyTo["content"]            # Replace HTML linebreak tags with actual linebreaks            content = cleanUpUnicode(content)            content = string.replace(content, "<br>", "\r")            content = string.replace(content, "<br/>", "\r")            content = string.replace(content, "<br />", "\r")            content = string.replace(content, "<p>", "")            content = string.replace(content, "</p>", "\r\r")            # Strip all other HTML tags            content = re.sub('<[^<]+?>', '', content)            tootwindow.reply = TitledEditText((10, 6, -10, -140), title=title, text=content, readonly=1, vscroll=1)            tootwindow.toot = TitledEditText((10, 76, -10, -70), title=heading, text=text, vscroll=1)        else:            self.replyToID = None            tootwindow.toot = TitledEditText((10, 6, -10, -70), title=heading, vscroll=1)        # Visibility radio buttons        visButtons = []        tootwindow.vis_public = W.RadioButton((10, 145, 55, 16), "Public", visButtons, self.visPublicCallback)        tootwindow.vis_unlisted = W.RadioButton((75, 145, 65, 16), "Unlisted", visButtons, self.visUnlistedCallback)        tootwindow.vis_followers = W.RadioButton((150, 145, 75, 16), "Followers", visButtons, self.visFollowersCallback)        tootwindow.vis_mentioned = W.RadioButton((230, 145, 75, 16), "Mentioned", visButtons, self.visMentionedCallback)                # If replying to an existing toot, default to that toot's visibility.        # Default to public for new toots that are not replies.        if replyTo:            if replyTo["visibility"] == "unlisted":                self.visibility = "unlisted"                tootwindow.vis_unlisted.set(1)            elif replyTo["visibility"] == "private":                self.visibility = "private"                tootwindow.vis_followers.set(1)            elif replyTo["visibility"] == "direct":                self.visibility = "direct"                tootwindow.vis_mentioned.set(1)            else:                self.visibility = "public"                tootwindow.vis_public.set(1)        else:            tootwindow.vis_public.set(1)        # Content warning checkbox and text field        tootwindow.cw = W.CheckBox((10, -45, 30, 16), "CW", self.cwCallback)        tootwindow.cw_text = W.EditText((50, -45, -10, 16))                # If replying to a toot with a CW, apply the CW to the reply.        # For new toots, default to the CW off.        if replyTo:            if replyTo["sensitive"]:                tootwindow.cw.set(1)                tootwindow.cw_text.set(replyTo["spoiler_text"])            else:                tootwindow.cw_text.show(0)        else:            tootwindow.cw_text.show(0)        # Close button        tootwindow.close_btn = W.Button((10, -22, 60, 16), "Close", tootwindow.close)        # Toot button        # This button is intentionally not made a default, so that if you press Return        # to make a multi-line toot it won't accidentally send.        tootwindow.toot_btn = W.Button((-69, -22, 60, 16), "Toot!", self.tootCallback)        return tootwindow    # ##################    # Callback Functions    # ##################    def cwCallback(self):        """        Called when the CW checkbox is ticked or unticked. Used to show/hide the        CW text entry field.        """        self.app.tootwindow.cw_text.show(not self.app.tootwindow.cw_text._visible)    def visPublicCallback(self):        """        Sets visibility to public when the Public radio button is clicked.        """        self.visibility = "public"    def visUnlistedCallback(self):        """        Sets visibility to unlisted when the Unlisted radio button is clicked.        """        self.visibility = "unlisted"    def visFollowersCallback(self):        """        Sets visibility to private when the Followers radio button is clicked.        """        self.visibility = "private"    def visMentionedCallback(self):        """        Sets visibility to direct when the Mentioned radio button is clicked.        """        self.visibility = "direct"    def tootCallback(self):        """        Called when the user presses the Toot button, and posts their toot.        """        req_data = {            "status": self.app.tootwindow.toot.get(),            "visibility": self.visibility        }        if self.replyToID:            req_data["in_reply_to_id"] = self.replyToID        if self.app.tootwindow.cw.get() == 1:            req_data["sensitive"] = "true"            req_data["spoiler_text"] = self.app.tootwindow.cw_text.get()        path = "/api/v1/statuses"        data = handleRequest(self.app, path, req_data, use_token=1)        if not data:            # handleRequest failed and should have popped an error dialog            return        if data.get("error_description") is not None:            okDialog("Server error when posting toot:\r\r %s" % data['error_description'])        elif data.get("error") is not None:            okDialog("Server error when posting toot:\r\r %s" % data['error'])        else:            okDialog("Tooted successfully!")            self.app.tootwindow.close()    # ################    # Helper Functions    # ################    def getMaxTootChars(self):        """        Gets the maximum allowed number of characters in a toot. Not all instances support        this, the default is 500 characters if not present in the response.        """        path = "/api/v1/instance"        data = handleRequest(self.app, path)        if not data:            return 500        if data.get("error_description") is not None:            dprint("Server error when getting max toot chars: %s" % data["error_description"])            return 500        elif data.get("error") is not None:            dprint("Server error when getting max toot chars: %s" % data["error"])            return 500        else:            max_toot_chars = data.get("max_toot_chars", 500)            dprint("max toot chars: %s" % max_toot_chars)            return max_toot_chars