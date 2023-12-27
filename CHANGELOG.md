## CHANGELOG

### v1.1.2 (2023-12-26)

* Macstodon is now fully compatible with WebOne 0.16+, and should also feature improved compatibility with other web proxies that can strip SSL.

### v1.1.1 (2023-12-10)

* Fixed a dumb bug that would cause Macstodon to crash after authentication if you were trying to sign in to an account that had no lists.

### v1.1 (2023-11-12)

* The timeline window now allows you to select which timeline is displayed in each column, using the drop-down menu next to the refresh button.
* The preferences window now allows you to select the default timeline that is loaded in each column at Macstodon launch.
* The title bar of loading dialogs now states the overall activity taking place.
* Fixed a bug that caused the Links and Attachments buttons to have glitched icons under certain circumstances.
* Fixed a bug that would display the wrong error message if the current user ID could not be retrieved from the server.

### v1.0.1 (2023-03-22)

* Fixed a major bug that could corrupt the timeline state when removing a boost from a toot.
* Fixed the bookmark button on timeline/profiles toggling the favourite button when pressed.
* Fixed a typo in the error message when failing to favourite/unfavourite a toot.
* Updated Macstodon's default memory requirements to 4 MB minimum, 16 MB preferred

### v1.0 (2023-03-20)

* Implemented support for profiles! Click on a user's profile picture to bring up their profile in a new window.
* Implemented support for user interactions, including follow/unfollow, mute/unmute, and block/unblock.
* Implemented support for viewing and modifying user notes.
* Added a "Find User" button to the Timeline window that allows you to search for a user by name and bring up their profile.
* Clicking on "User" notifications that are not connected to a toot (i.e. "User foobar followed you") will bring up that user's profile.
* Refactored the way that Macstodon does window management, this should result in the app using less memory and running faster.
* Added a Preferences window that allows you to customize the number of toots to load into a timeline, enable/disable images and clear the cache.
* More improvements to unicode character conversion, should see much less "junk" characters now.
* Fixed a bug causing unicode character conversion to not take place in the notification list.
* Removed BeautifulSoup and replaced it with a homebrewed solution for link extraction.
* Added a button to the timeline window for displaying the links attached to a toot, and automatically opening them in your browser.
* Added a button to the timeline window for displaying the attachments on a toot, viewing their alt text, and downloading them to your computer.
* Added new icons for the Boost, Favourite, Bookmark, and Reply buttons, courtesy of [C.M. Harrington](https://mastodon.online/@octothorpe)!
* Fixed a bug where the Toot window would remain open if you logged out with it open.
* Added a menu item for logging out.
* Fixed a JSON parsing bug introduced in 0.4.2, Macstodon will no longer rewrite "false", "true", or "null" if used in a toot.
* Improved reliability of getting the toot character limit from the Mastodon instance.
* The cursor will change to a watch when a progress bar window is active.
* Fixed a bug where the CW field when posting a toot was still usable even when it was invisible.
* Replying to a CW'ed toot will add "re: " to the CW (unless it already starts with that).

### v0.4.4 (2023-02-23)

* Fixed an edge case where the app could crash after authenticating.
* Updated some links in documentation.
* Updated copyright year to 2023.

### v0.4.3 (2022-12-23)

* Repackaged the v0.4.2 release but with separate 68K and PPC apps instead of a Fat Binary.
* For PPC users, nothing has changed for you and you don't have to upgrade.
* For 68K users, this should fix the "Missing PythonCore" error that showed up in v0.4.2.

### v0.4.2 (2022-12-22)

* Replaced the JSON parser with a simpler eval-based solution which is much faster.
* Macstodon is now a Fat Binary application and supports PowerPC architectures in addition to 68K!

### v0.4.1 (2022-12-21)

* Fixed a dumb bug that would cause a crash if the Mastodon server returned invalid JSON.

### v0.4 (2022-12-21)

* Favouriting, boosting, and bookmarking toots are now fully supported.
* Introduced an ImageHandler class that handles downloading/caching of images and saving them as pixmaps.
* User avatars (including booster avatars) are displayed in the timeline window. The first time you view a toot for each user, there will be a small delay while the avatar is downloaded and cached.
* The timeline window now displays correctly at a 512x342 display resolution, and will run in full screen at this resolution.
* Content warnings are displayed when viewing toots in the timeline window. When clicking on a toot with a content warning, you will be prompted to confirm.
* Toots can be replied to, and the toot being replied to will be shown in the toot window.
* When writing a new toot or replying to an existing toot, the visibility can be set.
* Content warnings can be set when creating toots or replying to existing toots.
* The character limit is now displayed in the toot window. There will be a small delay when pulling up the toot window for the first time while this data is queried from the server.
* Code refactoring: rename helpers/consntants files, move third-party code into separate folder
* Try to clean up unicode junk in display names, not just toot content.
* Dialogs are now rendered via the widget framework, and should no longer have their contents cut off.
* Improved the auth experience by printing the OAuth URL in the auth dialog.

### v0.3 (2022-11-28)

* Added a timeline view that shows the home and local timelines, and notifications
* Added some very basic HTML parsing for timeline toots
* Bug fixes to error handling
* Broke up source code into several files

### v0.2.1 (2022-11-20)

* Added a beautiful new application icon by [MhzModels](https://tech.lgbt/@mhzmodels)
* Replaced a crash-to-console with a friendly, recoverable error message if the connection is lost during an HTTP request.

### v0.2 (2022-11-19)

* Basically rewrote it to use the widget toolkit in a sane way.
* Added simple error handling.
* Added progress bars for HTTP and JSON decoding operations.
* Can now compile into a standalone app
* No longer supports being run directly through the Python IDE
* Many, many bug fixes

### v0.1 (2022-11-12)

* Initial Release.
