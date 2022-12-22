## CHANGELOG

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

* Added a beautiful new application icon by [MhzModels](https://mastodon.art/@mhzmodels)
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
