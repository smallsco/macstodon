<h1 align="center"><img src="readme_screenshots/logo.png" alt="Macstodon"></h1>
<h4 align="center">A basic Mastodon client for Classic Mac OS<br>created by <a href="https://oldbytes.space/@smallsco">@smallsco@oldbytes.space</a></h4>

## About
Macstodon is an app written in MacPython 1.5.2 for Classic Mac OS that lets you post toots and view timelines using a Mastodon server. It has been developed on a Macintosh IIfx running System 7.1.1.

System Requirements are:

* A 68k Macintosh with a 68020, 68030, or 68040 processor
* At least 1.5 MB of free memory (more if you want to be able to view avatars)
* System 7.1 to Mac OS 8.1
* 32-bit addressing enabled

The following extensions are required for System 7 users, and can be found in the "Required Extensions - System 7" folder distributed with Macstodon. System 7 users will need to copy them into the Extensions subfolder of their System Folder:

* CFM-68K Runtime Enabler
* ObjectSupportLib
* NuDragLib.slb

While not strictly _required_, installing Internet Config is strongly recommended as it will:

* allow Macstodon to automatically open your web browser to the authentication URL during the initial login process
* allow you to globally set a HTTP proxy, so that you can use an SSL-stripping proxy. Without this you are restricted to pure HTTP instances (and I'm not sure if any such instances exist)

**No support is provided for this app, and I don't plan on maintaining it long-term. This is just a fun hack project, not a serious development effort.**

## Screenshots
<p align="center">
    <img src="readme_screenshots/timeline.png?raw=true" alt="Timeline View">
</p>
<p align="center">
    <img src="readme_screenshots/toot.png?raw=true" alt="Replying to a Toot">
</p>
<p align="center">
    <img src="readme_screenshots/contentwarning.png?raw=true" alt="Content Warning Dialog">
</p>

## Features

* Authentication
* Post plain-text toots with full control of visibility, and optional content warnings
* View your home and local timelines
* View your notifications
* Favourite, boost, and bookmark toots
* Reply to toots from others

That's it for now. Maybe more features will be implemented in a later version.

## How to Run It
1. Download and install the latest version of Macstodon from the Releases page: <https://github.com/smallsco/macstodon/releases>
2. Decompress the archive and place the Macstodon application whereever you like on your hard disk.
3. If you're running System 7, copy the files in the `Required Extensions - System 7` folder into the `Extensions` folder (subdirectory of `System Folder`) and reboot your Mac.
4. Double-click the Macstodon app to run it!
5. In the "Server" window that appears, type the full URL to your Mastodon server, using **http** instead of **https**, and **without the trailing slash**. Then click the `Login` button.
6. After a moment, your web browser should automatically launch to your Mastodon instance's authentication page. Log in here, and you will be redirected to another page with a code on it. Copy this code to the clipboard.
7. Now return to the Macstodon application. An `Auth` window will have appeared with another text box, paste the code into this box and press the `OK` button.
8. After a moment, the `Timeline` window will appear and Macstodon will start loading the timelines and notifications from your instance. This will take some time, please be patient.
9. When the progress dialog has gone away, you will be able to interact with the Timeline window. Click on a toot or notification to view it in the bottom third of the window. Or click the `Refresh` button above one of the timelines to refresh that timeline with the latest data.
10. If you click the `Post Toot` button in the `Timeline` window, a `Toot` window will appear. In this window you can type a message and press the `Toot!` button to post it to the Mastodon server. After tooting you can click `Close` to return to the `Timeline` window.
11. Clicking `Logout` in the `Timeline` window will return you to the `Server` window.
12. Clicking `Quit` in the `Server` window will quit Macstodon. The next time you run it, you will not need to re-authenticate unless you change the server URL.

## How to compile it
1. Download the Macstodon source code from GitHub, and place it whereever you like on your hard disk.
2. Download MacPython 1.5.2 from here: <https://homepages.cwi.nl/~jack/macpython/downloads/old/MacPython152.hqx>
3. Decompress the MacPython archive and run the isntaller. Make sure you install the **CFM-68K** version of MacPython if prompted.
4. Run the **EditPythonPrefs** application that comes with MacPython. Add the followiung line to the System-Wide preferences. Then save your changes and exit.
	```
	$(PYTHON):Extensions:Imaging:PIL
	```  
5. Decompress the `Macstodon.rsrc.sit.hqx` file until you have `Macstodon.rsrc`. Keep this in the same directory as `Macstodon.py`.
6. Edit line 24 of the `Macstodon.py` file, which looks like this:
	```
	# macfreeze: path Software:Programming:Python 1.5.2c1:Mac:Tools:IDE
	```  
	Change the *Software:Programming:Python 1.5.2c1:Mac:Tools:IDE* path to point to the **Mac:Tools:IDE** folder of the location where you installed MacPython.
7. Edit line 81 of the `macgen_bin.py` file, which comes with MacPython and is located in the **Mac:Tools:macfreeze** directory. Comment out this line, it should look like this after your change:
	```
	#fss.SetCreatorType('Pyta', APPL)
	```  
	(This fixes a bug in MacPython 1.5.2, where the build system is overriding the creator type of the application defined in the RSRC with its' own. You can still build Macstodon without this fix, but it won't have its' lovely icon!)
8. Double-click the `Macstodon.py` file to launch the `Python IDE` application. When the source code window appears, press `Run All`. This will launch Macstodon within the Python IDE, which will create a bunch of `.pyc` files in the source directory.
9. Force quit the Python IDE, because Macstodon corrupts its' state and won't let you quit normally...
10. Drag and drop the `Macstodon.py` file onto the `BuildApplication` app that comes with MacPython.
11. When prompted, select the `Build 68K Application` radio button.
12. Select where you want to save the app to.
13. Wait about 10 minutes or so for the build to finish. When it's done, you should have your own self-compiled copy of Macstodon!

## Known Issues
* SSL is not supported at all, because neither the Classic Mac OS nor the ancient version of MacPython used to build Macstodon know anything about it.
* This means, in order to access your instance, you will almost certainly need to run an SSL-stripping proxy server running on another computer on your network, and configure your Mac to use it. THis is outside the scope of this readme, however:
	* I strongly recommend the use of the [WebOne](https://github.com/atauenis/webone) proxy, which is what I develop with. If you are also using WebOne, you may need to make the following config changes:
	* You may need to add your Mastodon server's hostname to the `ForceHTTPS` section of WebOne's config file, depending on how your Mastodon instance is configured.
	* Also, some instances (i.e. `bitbang.social`) require that the User-Agent is configured to something modern-looking before they will accept connections through WebOne. This is known to work:  
	```
	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15
	```
* You will need to use **http** instead of **https** in the server URL for Macstodon. This is a limitation of the *urllib* library in MacPython 1.5.2.
* Performance of parsing large JSON responses is *terrible*. I'm sorry, I don't know how to fix this. If it looks like Macstodon has hung during the "Parsing Response" stage of a progress bar, it probably hasn't, it's just taking it's sweet time. Go make a coffee and come back :)
* There is no support for Unicode whatsoever, and there never will be. Toots or usernames with emojis and special characters in them will look funny.
* There is no PowerPC build available because the MacPython 1.5.2 builder for PPC isn't respecting the runtime preferences that I have configured. This is *probably* a bug in this particular version of MacPython, and is *probably* fixed in later versions - which aren't 68K compatible. So if you really, really want a PPC version of this, you can try building it with MacPython 2.2 or 2.3 - I haven't tested this, though, and don't know if it will work without code changes.
* If Macstodon actually crashes or unexpectedly quits while loading data from the server, try allocating more memory to it using the Get Info screen in the Finder.
* If the `Timeline` window is closed, you can't get it back and will have to quit Macstodon from the File menu and relaunch it.
* If images (avatars) fail to load, but the rest of the app seems to be working just fine, this means you need to give Macstodon more memory. Allocating more memory to it using the Get Info screen in the Finder will resolve this issue (you should also remove the image cache, see below)

## Troubleshooting
When in doubt, delete the preferences file. It is named `Macstodon Prefs` and lives in the Preferences folder in your System Folder. Deleting the preferences file will make Macstodon forget about the saved server, tokens, etc.  

There is also a subfolder of the Preferences folder named Macstodon Cache. This folder contains avatars and other images that have been resized, so we don't need to download and resize them again the next time we encounter them in the wild. Occasionally this can become corrupted and an original image can be cached instead of a resized one, leading to poor performance and high memory usage. If this happens, you can delete this folder, it will be recreated on the next launch.

## Credits
Special thanks to the following third-party software, for whom without Macstodon would not be possible:

**BeautifulSoup pre-1.3**  
Copyright ©2004 Leonard Richardson  
License: Python  
<https://docs.python.org/3/license.html>

**JSON Decoding Algorithm**  
Copyright ©2016 Henri Tuhola  
License: MIT  
<https://github.com/cheery/json-algorithm>

Extra special thanks to:  
[Dan](https://mastodon.lol/@billgoats) - for the inspiration to work on this project  
[Mingo](https://oldbytes.space/@mingo) - for [suggesting the name](https://oldbytes.space/@mingo/109316322622806248)  
[MhzModels](https://mastodon.art/@mhzmodels) - for the beautiful logo at the top of this README, and the Macstodon application icon!
