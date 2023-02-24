"""Macstodon - a Mastodon client for classic Mac OSMIT LicenseCopyright (c) 2022-2023 Scott Small and ContributorsPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associateddocumentation files (the "Software"), to deal in the Software without restriction, including without limitation therights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permitpersons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of theSoftware.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THEWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS ORCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OROTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""# ############### Python Imports # ##############import EasyDialogsimport Qdimport stringimport timeimport urllibimport Wfrom Wlists import List# ########### My Imports# ##########from MacstodonConstants import DEBUG, VERSION# ########## Functions# #########    def cleanUpUnicode(content):    """    Do the best we can to manually clean up unicode stuff    """    content = string.replace(content, "\\u003e", ">")    content = string.replace(content, "\\u003c", "<")    content = string.replace(content, "\\u0026", "&")    content = string.replace(content, "‚Ä¶", "...")    content = string.replace(content, "‚Äô", "'")    content = string.replace(content, "‚Ä§", ".")    content = string.replace(content, "‚Äî", "-")    content = string.replace(content, "‚Äú", '"')    content = string.replace(content, "‚Äù", '"')    content = string.replace(content, "&quot;", '"')    content = string.replace(content, "√©", "é")    content = string.replace(content, "√∂", "ö")    content = string.replace(content, "&#39;", "'")    content = string.replace(content, "&amp;", "&")    content = string.replace(content, "&gt;", ">")    content = string.replace(content, "&lt;", "<")    return contentdef decodeJson(data):    """    'Decode' the JSON by taking the advantage of the fact that    it is very similar to a Python dict. This is a terrible hack,    and you should never do this anywhere because we're literally    eval()ing untrusted data from the 'net.    I'm only doing it because it's fast and there's not a lot of    other options for parsing JSON data in Python 1.5.    """    data = string.replace(data, "null", "None")    data = string.replace(data, "false", "0")    data = string.replace(data, "true", "1")    data = eval(data)    return datadef dprint(text):    """    Prints a string to stdout if and only if DEBUG is true    """    if DEBUG:        print textdef okDialog(text, size=None):    """    Draws a modal dialog box with the given text and an OK button    to dismiss the dialog.    """    if not size:        size = (360, 120)    window = W.ModalDialog(size, "Macstodon %s - Message" % VERSION)    window.label = W.TextBox((10, 10, -10, -40), text)    window.ok_btn = W.Button((-80, -30, -10, -10), "OK", window.close)    window.setdefaultbutton(window.ok_btn)    window.open()def okCancelDialog(text, size=None):    """    Draws a modal dialog box with the given text and OK/Cancel buttons.    The OK button will close the dialog.    The Cancel button will raise an Exception, which the caller is    expected to catch.    """    if not size:        size = (360, 120)    global dialogWindow    dialogWindow = W.ModalDialog(size, "Macstodon %s - Message" % VERSION)    def dialogExceptionCallback():        dialogWindow.close()        raise KeyboardInterrupt    dialogWindow.label = W.TextBox((10, 10, -10, -40), text)    dialogWindow.cancel_btn = W.Button((-160, -30, -90, -10), "Cancel", dialogExceptionCallback)    dialogWindow.ok_btn = W.Button((-80, -30, -10, -10), "OK", dialogWindow.close)    dialogWindow.setdefaultbutton(dialogWindow.ok_btn)    dialogWindow.open()def handleRequest(app, path, data = None, use_token = 0):    """    HTTP request wrapper    """    try:        pb = EasyDialogs.ProgressBar(maxval=3)        if data == {}:            data = ""        elif data:            data = urllib.urlencode(data)        prefs = app.getprefs()        url = "%s%s" % (prefs.server, path)        dprint(url)        dprint(data)        dprint("connecting")        pb.label("Connecting...")        pb.inc()        try:            if use_token:                urlopener = TokenURLopener(prefs.token)                handle = urlopener.open(url, data)            else:                handle = urllib.urlopen(url, data)        except IOError:            del pb            errmsg = "Unable to open a connection to: %s.\rPlease check that your SSL proxy is working properly and that the URL starts with 'http'."            okDialog(errmsg % url)            return None        except TypeError:            del pb            errmsg = "The provided URL is malformed: %s.\rPlease check that you have typed the URL correctly."            okDialog(errmsg % url)            return None        dprint("reading http headers")        dprint(handle.info())        dprint("reading http body")        pb.label("Fetching data...")        pb.inc()        try:            data = handle.read()        except IOError:            del pb            errmsg = "The connection was closed by the remote server while Macstodon was reading data.\rPlease check that your SSL proxy is working properly."            okDialog(errmsg)            return None        try:            handle.close()        except IOError:            pass        pb.label("Parsing data...")        pb.inc()        dprint("parsing response json")        try:            decoded = decodeJson(data)            dprint(decoded)            pb.label("Done.")            pb.inc()            time.sleep(0.5)            del pb            return decoded        except:            del pb            dprint("ACK! JSON Parsing failure :(")            dprint("This is what came back from the server:")            dprint(data)            okDialog("Error parsing JSON response from the server.")            return None    except KeyboardInterrupt:        # the user pressed cancel in the progress bar window        return None# ######## Classes# #######class ImageWidget(W.Widget):    """    A widget that displays an image. The image should be passed    in as a PixMapWrapper.    """    def __init__(self, possize, pixmap=None):        W.Widget.__init__(self, possize)        # Set initial image        self._imgloaded = 0        self._pixmap = None        if pixmap:            self.setImage(pixmap)    def close(self):        """        Destroys the widget and frees up its memory        """        W.Widget.close(self)        del self._imgloaded        del self._pixmap    def setImage(self, pixmap):        """        Loads a new image into the widget. The image will be        automatically scaled to the size of the widget.        """        self._pixmap = pixmap        self._imgloaded = 1        if self._parentwindow:            self.draw()    def clearImage(self):        """        Unloads the image from the widget without destroying the        widget. Use this to make the widget draw an empty square.        """        self._imgloaded = 0        Qd.EraseRect(self._bounds)        if self._parentwindow:            self.draw()        self._pixmap = None    def draw(self, visRgn = None):        """        Draw the image within the widget if it is loaded        """        if self._visible:            if self._imgloaded:                self._pixmap.blit(                    x1=self._bounds[0],                    y1=self._bounds[1],                    x2=self._bounds[2],                    y2=self._bounds[3],                    port=self._parentwindow.wid.GetWindowPort()                )class TitledEditText(W.Group):    """    A text edit field with a title and optional scrollbars attached to it.    Shamelessly stolen from MacPython's PyEdit.    Modified to also allow setting the title, and add scrollbars.    """    def __init__(self, possize, title, text="", readonly=0, vscroll=0, hscroll=0):        W.Group.__init__(self, possize)        self.title = W.TextBox((0, 0, 0, 16), title)        if vscroll and hscroll:            editor = W.EditText((0, 16, -15, -15), text, readonly=readonly)            self._barx = W.Scrollbar((0, -16, -15, 16), editor.hscroll, max=32767)            self._bary = W.Scrollbar((-16, 16,0, -15), editor.vscroll, max=32767)        elif vscroll:            editor = W.EditText((0, 16, -15, 0), text, readonly=readonly)            self._bary = W.Scrollbar((-16, 16, 0, 0), editor.vscroll, max=32767)        elif hscroll:            editor = W.EditText((0, 16, 0, -15), text, readonly=readonly)            self._barx = W.Scrollbar((0, -16, 0, 16), editor.hscroll, max=32767)        else:            editor = W.EditText((0, 16, 0, 0), text, readonly=readonly)        self.edit = editor    def setTitle(self, value):        self.title.set(value)    def set(self, value):        self.edit.set(value)    def get(self):        return self.edit.get()class TokenURLopener(urllib.FancyURLopener):    """    Extends urllib.FancyURLopener to add the Authorization header    with a bearer token.    """    def __init__(self, token, *args):        apply(urllib.FancyURLopener.__init__, (self,) + args)        self.addheaders.append(("Authorization", "Bearer %s" % token))        class TwoLineListWithFlags(List):    """    Modification of MacPython's TwoLineList to support flags.    """    LDEF_ID = 468    def createlist(self):        import List        self._calcbounds()        self.SetPort()        rect = self._bounds        rect = rect[0]+1, rect[1]+1, rect[2]-16, rect[3]-1        self._list = List.LNew(rect, (0, 0, 1, 0), (0, 28), self.LDEF_ID, self._parentwindow.wid,                    0, 1, 0, 1)        self._list.selFlags = self._flags        self.set(self.items)class TimelineList(W.Group):    """    A TwoLineListWithFlags that also has a title attached to it.    Based on TitledEditText.    """    def __init__(self, possize, title, items = None, btnCallback = None, callback = None, flags = 0, cols = 1, typingcasesens=0):        W.Group.__init__(self, possize)        self.title = W.TextBox((0, 2, 0, 16), title)        self.btn = W.Button((-50, 0, 0, 16), "Refresh", btnCallback)        self.list = TwoLineListWithFlags((0, 24, 0, 0), items, callback, flags, cols, typingcasesens)    def setTitle(self, value):        self.title.set(value)    def set(self, items):        self.list.set(items)    def get(self):        return self.list.items    def getselection(self):        return self.list.getselection()    def setselection(self, selection):        return self.list.setselection(selection)