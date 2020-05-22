# saunabot
This is the github page for saunabot. It's made to integrate your self-hosted Minecraft server with Discord so your friends can turn on or off the server using a simple command.

You will need to change some things directly in the code. It's super messy, and I do plan to clean it up and make it look like a real bot eventually.

#List of things you need to do/change before using:
A lot of these are commented in the code too.
- Lines 50-74, optional changes commented in the code
- Lines 86-92, enter your Discord user ID there or delete the lines. I personally like the command.
- Lines 94-98, enter your Discord user ID. Bot won't work without it and allows you to blacklist people from using commands.
- Lines 129-136, change YOUR-PORT to the port your server is using. IP-address too if necessary.
- Lines 139-160, a lot. urls for the embeds, ports etc.
- Lines 162-170, see ^
- Lines 173-183, paths and possibly file names.
- Line 218, **your bot token. Don't share it.**

pip installs:
https://pypi.org/project/pip/

Not sure what's pre-installed and what isn't so:
- discord
- asyncio
- mcstatus
Check imports for complete list.

#Questions?
My Discord is Vilhu#0001. Message me on there or open an issue on github.
