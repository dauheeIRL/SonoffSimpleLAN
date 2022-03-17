# SonoffSimpleLAN
Non async control of Sonoff switches

This is a really raw file, but works perfectly for me.

so if you are here, you can do a little coding in python. there are a number of libraries out there:
some for the older unencrypted firmware version of sonoff
some that don't actually use the DIY LAN capability and scrape the itlead website to control devices
and a number either no longer maintained libraries or ones that are specific to HomeAssistant

So how I got here was I used https://github.com/mattsaxon/pysonofflan which was great except it had a few issues. No longer maintained so I forked and fixed up what I could. When I moved my app from Debian to windows, it started to hang when trying to turn a device on/off - it could be some nuance of the windows python interface or even just a different version of a sub library (I matched some like zeroconf and asyncio but still didn't work). The problem was somewhere in the bowels of asyncio and I didn't have a month to learn all the nuances (I don't code a lot)

So basically what this script is a NON-asyncio copy of the library I mentioned above - that library itself is a copy of a copy etc so we are standing on the shoulders of giants here.

This script works for me, its actually lightening fast and faster than the asyncio version. It still has some embedded dependancies on pysonofflanR3 so you will need to install that - but the only thing is I have fixed up a few asyncio things in it so you will need to take from https://github.com/dauheeIRL/pysonofflan (mine) if you want to use any of the asyncio stuff.

