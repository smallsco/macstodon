<h1 align="center">Macstodon</h1>
<h4 align="center">A silly little Mastodon client for Classic Mac OS</h4>

## About
Macstodon is an app (well, a script really) written in MacPython 1.5.2 that lets you post a plain text toot to a Mastodon server.

It has been tested on a Macintosh IIfx running System 7.1.1. I don't know what the minimum requirements are but I'm guessing at least 7.0 to support the Python runtime.

**No support is provided for this app, and I don't plan on maintaining it long-term. This is just a fun hack project, not a serious development effort.**

## Screenshots
![Login Screenshot](readme_screenshots/login.png?raw=true)  
![Auth Screenshot](readme_screenshots/auth.png?raw=true)  
![Toot Screenshot](readme_screenshots/toot.png?raw=true)

## Features
It lets you authenticate and post toots in plain text - that's it! No timelines or support for any other Mastodon features.

## How to Run It
1. Download and install MacPython 1.5.2 from here: <https://homepages.cwi.nl/~jack/macpython/downloads/old/MacPython152.hqx>
2. Clone this repository and copy its' contents to your old Mac!
3. Double click `macstodon.py` which will launch the `Python IDE` program.
4. In the IDE window which comes up, click the `Run All` button located at the top of the window.
5. Now the program is running. Type the full URL to your Mastodon server, minus the trailing slash, and click "Login".
6. Your web browser will launch to a Mastodon authentication page. Log in, and you will be redirected to a page with a code on it.
7. Copy this code and return to the Macstodon application. In the `Auth` window that has appeared, paste this code, and click the `OK` button.
8. You will now be at the Toot window. Type some text into the text area and press the `Toot!` button to post it to Mastodon.
9. When you're done, quit the Python IDE. The next time you run it, you will not need to re-authenticate.

## Known Issues
* SSL is not supported at all. You will need to run an SSL-stripping proxy on another machine and configure your Mac to use it. I recommend using [WebOne](https://github.com/atauenis/webone). Note that you might need to add your Mastodon server to the `ForceHTTPS` section of WebOne's config file depending on how your Mastodon server is configured.
* This also means you'll need to use `http` instead of `https` in the server URL - Python 1.5.2's `urllib` doesn't have any support whatsoever for `https`.
* Performance is pretty bad when it comes to parsing JSON responses.
* There are no progress bars, and this is a slow app. It may appear to freeze, but it's probably just working.
* There is no support for Unicode whatsoever. This app may not work for you if you have an emoji in your username. Sorry.
* The app crashes when you click the `Logout` button in the Toot window. I don't know why this is, but I suspect I'm not using the widget toolkit properly (it's not documented)
* Macstodon is not a standalone app yet, it is only a Python script. This is because my Mac crashes when I try to compile it into an app. Need help here!
* In general, there is little-to-no error handling. If the Mastodon server returns something unexpected to a request, expect crashes.

## Troubleshooting
When in doubt, delete the preferences file. It is named `Macstodon Prefs` and lives in the Preferences folder in your System Folder. Deleting the preferences file will make Macstodon forget about the saved server, tokens, etc.

## Credits
Special thanks to the following third-party software, for whom without Macstodon would not be possible:

**JSON Decoding Algorithm**  
Copyright ©2016 Henri Tuhola  
License: MIT
<https://github.com/cheery/json-algorithm>

Extra special thanks to:  
[Dan](https://mastodon.lol/@billgoats) - for the inspiration to work on this project  
[Mingo](https://oldbytes.space/@mingo) - for [suggesting the name](https://oldbytes.space/@mingo/109316322622806248)  
