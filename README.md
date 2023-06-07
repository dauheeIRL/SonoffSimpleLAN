# SonoffSimpleLAN
Non async control of Sonoff switches

Works perfectly for me - just plonk the 2 py files into your folder

so if you are here, you can do a little coding in python. there are a number of libraries out there:
-some for the older unencrypted firmware version of sonoff
some that don't actually use the DIY LAN capability and scrape the itlead website to control devices-
-and a number either no longer maintained libraries or ones that are specific to HomeAssistant

So how I got here was I used https://github.com/mattsaxon/pysonofflan which was great except it had a few issues. No longer maintained so I forked and fixed up what I could. When I moved my app from Debian to windows, it started to hang when trying to turn a device on/off - it could be some nuance of the windows python interface or even just a different version of a sub library (I matched some like zeroconf and asyncio but still didn't work). The problem was somewhere in the bowels of asyncio and I didn't have a month to learn all the nuances (I don't code a lot)

So basically what this script is a NON-asyncio copy of the library I mentioned above - that library itself is a copy of a copy etc so we are standing on the shoulders of giants here ( OK the monitoring is aysyncio)

This script works for me, its actually lightening fast and faster than the asyncio version. It has no embedded dependancies but if doesn't run, make sure to install any includes in the files

So basically, if you want to just turn stuff on/off, you can see the comment in my script

now has additional monitoring to get an event raised if a switch is turned on/off at the physical switch - this can be usefull for something like having a dummy outlet/channel that you can get to perform a different action i.e. turn lightswitch on and send a tweet

If there is some poor soul out there that is in the same situation as me, having a need but not enough skills, by all means ask me a question. Asyncio butchered my noodle and I couldn't maintain the fork of pysonofflanr3 any more, but still love my sonoff switches and didn't want to have to go flashing them with custom firmware

