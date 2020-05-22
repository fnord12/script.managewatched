![Icon](https://github.com/fnord12/script.managewatched/blob/master/resources/icon.png)

Managed Watch for Kodi
======

## What is it?
The stock Mark Watched/UnWatched function in Kodi does three things:

* Adjusts the Playcount (Playcount of 0 means Unwatched, > 0 means Watched).
* Adjusts the Last Played Date to the current time if marked Watched, blank in Unwatched.
* Clears the Resume/Continue data.

Sometimes (for me, often!) you just want to update ONE of those fields.  You want to mark a video watched without it showing up on your Recently Watched playlist.  You want to clear the Resume data (and get rid of that resume icon) without losing the current playcount or last played date.  This script allows you to adjust each of these things separately.


---
## The functions:
__Reset Watched__ - Clears the Last Played value and resume data without affecting Playcount (Watch Status).  This is for when you want to retain the fact that something was watched but don't need it on your Recently Watched and Continue Watching playlists.

__Mark Watched__ - Marks a video watched without affecting the Last Played value.  For indicating that you watched something a long time ago.  You want that checkmark, but don't need to see it on Recently Watched.

__Mark Unwatched__ - Clears all three fields (same as stock Kodi)

__Clear Resume__ - Clears the resume field only.

__Edit Played Date__ - Manually edit the Last Played Date field.

---
## Setup

1. Install the add-on (obviously)

2. The functions will now be available in the Context Menu.  But if you want to map the individual functions to keys, you can adjust your [keymap file](https://kodi.wiki/view/Keymap#Location_of_keymaps).

There are five functions you can call. All are available via the context menu, under Manage Watched.  The example shows them mapped to example keys; you can choose whatever keys you want:

```
<Global>
        <keyboard>
			#other stuff that may already be here...
			
			<r mod="ctrl">RunScript(script.managewatched,reset)</r>
			<w mod="ctrl">RunScript(script.managewatched,mark)</w>
			<u mod="ctrl">RunScript(script.managewatched,unmark)</u>
			<c mod="ctrl">RunScript(script.managewatched,clear)</c>
			<e mod="ctrl">RunScript(script.managewatched,edit)</e>
	</keyboard>
</Global>

```

Personally i only have Reset and Mark Watched set to keys.  The rest are used rarely enough that the context menu suffices.  And the stock Kodi Mark Unwatched works as well (and is faster) than my Mark Unwatched.

3. If you want the context menu item to appear under the Manage... menu instead of the main context menu, you can edit the addon.xml file.  Change ```<menu id="kodi.core.main">``` to ```<menu id="kodi.core.manage">```.  If you want, while you are in that file, you can also update the context menu items to remind you of the keyboard shortcuts (e.g. ```<label>Reset Watched</label>``` to ```<label>Reset Watched (Cntrl-R)</label>```.  You can even adjust the language if you don't prefer English since i didn't provide a .po file (sorry!).

Change will take affect after you restart Kodi.

4. Reset Watched and Mark Watched set the Last Played Date to a distant date in the past, to retain the fact that it was watched without affecting your lists.  The date is "2000-01-01 00:00:01".  If you don't like that date and you are feeling adventurous, you can update managewatched.py.  The variable is assigned that date in two places.

5. In order to affect containers (TVShows, Seasons, and Movie Sets), this script uses a direct data query.  If you are not using the stock Kodi database, some additional configuration may be required.

A tip if using MYSQL:
>
>Download mysql-connector-python-8.0.17.tar.gz Source from 
>https://pypi.org/project/mysql-connector-python/#files
>copy from zip only folder ../lib/mysql/*.* to ../addons/script.tagoverview/mysql
>
>Add database parameters in CDatabase.py
>under
>class CDatabase:
>
>    baseconfig = {
>    }
>
>Add database parameters in MySQLconfig.py
>under
>class Config(object):

---
## Caveats:

---
### Challenges

1. This script uses JSON to update the fields.  JSON is SLOW.  This will be noticible mainly when affecting containers (TVShows, Seasons, and Movie Sets).  For large containers, Kodi may feel like it is hanging.  In my experience, it will eventually finish.

2. In order to make your changes visible to you, i use Kodi's Skin Refresh function.  The Skin Refresh function was really meant to allow Skin developers the ability to check their work, and it occassionally/rarely causes a crash.

3. As noted above, i needed to set the Last Played field to some old date for some of the functions.  It uses "2000-01-01 00:00:01".  You can edit that default date in the code if you want, or you can use Edit Played Date on a case by case basis.  (If enough people find it useful, i can make this and a few other parameters configurable through a normal Kodi Addons > Settings screen).

---
### Warnings

Tested in Kodi 18 Leia only.  Tested with local files only (not with streaming, not with SMBs).  It should still work in other cases; i just don't know.

