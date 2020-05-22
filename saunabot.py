import discord
import discord.ext
from discord.ext import commands
import asyncio
import os
from mcstatus import MinecraftServer
import time
import subprocess
from pathlib import Path
import sys
from os.path import join
import requests

#
# bot created by Vilhu#0001 on discord
# project was originally for my own personal use, that's why the function names and commands are like that.
#

bot = commands.Bot(command_prefix = "s!",case_insensitive=True, help_command=None)
bot.servertype = "undefined, use `s!setservertype`"

@bot.event
async def on_ready():
	print("Bot ready")
	await bot.change_presence(activity=discord.Game(name='s!help'))
	#await snapshutdown() # uncomment this to enable autoshutdown for snapshot server. not sure if it works, i don't exactly recommend using it.

@bot.command()
async def help(ctx):
	emhelp = discord.Embed(title="Command list", color=0x00ff00)
	emhelp.add_field(name="s!help: ", value="Opens this embed", inline=False)
	emhelp.add_field(name="s!saunamc ", value="Checks server status", inline=False)
	emhelp.add_field(name="s!saunaon [argument] ", value="Turns on the Minecraft server.", inline=False)
	emhelp.add_field(name="s!saunaoff", value="Shuts down the minecraft server.", inline=False)
	emhelp.set_footer(text="Saunabot 1.0 - https://github.com/vilhu-github/sauna")
	await ctx.channel.send(embed=emhelp)

@bot.command()
async def saunamc(ctx):
	if not blistchecker(ctx) == True:
		try:
			await saunamc1(ctx)
		except:
			await saunamc2(ctx)

@bot.command()
async def ping(ctx):
	await ctx.send("Pong!")

@bot.command()
async def saunaon(ctx, arg):
	if not blistchecker(ctx) == True:
		if arg == "vanilla":
			if onchecker() == True:
				await ctx.channel.send(content="Server is already running, "+ ctx.author.mention)
			else:
				runmc()
				msg = await ctx.channel.send(content="Starting the server. You can use `!saunamc` to check its status.")
				msg # there was something that made this useful
				await asyncio.sleep(3) # shorten or delete this if you wish
				await msg.edit(content="Server started. You can use `s!saunamc` to check its status. :white_check_mark:")
				bot.servertype = "vanilla" # or something else, feel free to change
		elif arg == "snapshot": #change that to something else if needed
			if onchecker() == True:
				await ctx.channel.send(content="Server is already running, "+ ctx.author.mention)
			else:
				runmcsnap() # starts the snapshot server
				msg = await ctx.channel.send(content="Starting the server. You can use `!saunamc` to check its status.")
				msg
				await asyncio.sleep(3)
				await msg.edit(content="Server started. You can use `s!saunamc` to check its status. :white_check_mark:")
				bot.servertype = "snapshot" # feel free to change if needed
		else:
			await ctx.message.add_reaction('⚠️')

@saunaon.error
async def saunaon_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.message.add_reaction("❓")

@bot.command()
async def servertype(ctx): # sends the mc server type, was originally a debug command but thought that i'll just leave it here
	await ctx.send(bot.servertype)


@bot.command()
async def kill(ctx): # shuts down your computer. windows only? not sure. i might add a confirmation in the future tho
	if ctx.author.id == your-id-here:
		await ctx.channel.send("Shutting down. Not cancelable.")
		os.system("shutdown /s /t 5")
	else:
		await ctx.message.add_reaction('⚠️')

@bot.command()
async def blacklist(ctx, arg):
	if ctx.author.id == your-id-here:
		blacklister(arg) # blacklists a user id given in the argument
		await ctx.channel.send("<@{}> was blacklisted from the bot.".format(arg))

@blacklist.error
async def blacklist_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.message.add_reaction('⚠️')

async def snapshutdown(): # no idea why i didn't do this with ext.tasks but this works (i think?) so i'm not gonna touch it
	while True:
		if bot.servertype == "snapshot":
			try:
				if shutchecker():
					await asyncio.sleep(600)
					if shutchecker():
						snapkill()
			except:
				pass
		else:
			await asyncio.sleep(300)


def onchecker():
	for p in psutil.process_iter(attrs=['pid', 'name']):
		if "java" in (p.info['name']).lower(): #  i don't actually know why it doesn't kill your game client. or at least doesn't on my end.
			return True

def snapkill(): # kills the server process
	for p in psutil.process_iter(attrs=['pid', 'name']):
		if "java" in (p.info['name']).lower() and bot.servertype == "snapshot": # i don't actually know why it doesn't kill your game client. or at least doesn't on my end.
			p.kill()

def shutchecker(): # i don't know. important for the kill command.
	serverz = MinecraftServer("127.0.0.1", YOUR-PORT) #could be used to check other server statuses too, maybe by a command? might actually make that eventually.
	statusz = serverz.status()
	try:
		if statusz.players.online == 0:
			return True
	except:
		pass


async def saunamc1(ctx):
	server = MinecraftServer("127.0.0.1", YOUR-PORT) # 25565 is the default. change ip if needed. could be used to check other server statuses too, maybe by a command? might actually make that eventually.
	status = server.status()
	if status.players.online == 0: # the way i did this is actually stupid as hell but i cba to fix it
		embed = discord.Embed(title="Server status", color=0x00ff00)
		embed.set_thumbnail(url="url goes here")
		embed.add_field(name="Playing: ", value=status.players.online, inline=False)
		embed.add_field(name="Ping: ", value=f"{status.latency * 1000} ms", inline=False) # will be around 0 but oh well
		embed.add_field(name="Server version", value=bot.servertype, inline=False) # the variable is set with the startup command. only really useful if you have multiple servers
		embed.set_footer(text="something-here")
		await ctx.channel.send(embed=embed)
	elif status.players.online >= 0: # i have no clue why i did this thing like this. will fix eventually
		server2 = MinecraftServer("127.0.0.1", YOUR-PORT) #could be used to check other server statuses too, maybe by a command? might actually make that eventually.
		query = server2.query()
		status2 = server2.status()
		embed = discord.Embed(title="Server status", color=0x00ff00) # see notes from above
		embed.set_thumbnail(url="something something something")
		embed.add_field(name="Playing:", value="{0}".format(", ".join(query.players.names), inline=False))
		embed.add_field(name="Ping: ", value=status2.latency, inline=False)
		embed.add_field(name="Server version:", value=bot.servertype, inline=False)
		embed.set_footer(text="something-here")
		await ctx.channel.send(embed=embed)

async def saunamc2(ctx):
	if not onchecker() == True:
		embed = discord.Embed(title="Server status", color=0xff0000)
		embed.set_thumbnail(url="direct-link-to-your-server-icon")
		embed.add_field(name="Playing: ", value="Server offline", inline=False)
		embed.set_footer(text="your-footer-here") # i usually like to put the server ip here
		await ctx.channel.send(embed=embed)
	else:
		await ctx.channel.send("Server is starting or not available. Please contact the server admin if this persists.") # this should only appear if the check runs before the server is actually up or if the server is on but something else is fucked like port forwarding


def runmc(): # main server
	for f_name in os.listdir("some-path-here"): # enter the minecraft server's path
		if f_name.endswith("start.bat"): # batch file is probably the easiest way to start the server. my start.bat starts another .bat so the bot itself doesn't die.
			path = "some path here" # the path again
			subprocess.call(join(path, f_name)) # actually starts the server

def runmcsnap(): # snapshot server
	for f_name in os.listdir("some-path-here"): # enter the minecraft server's path
		if f_name.endswith("start.bat"): # batch file is probably the easiest way to start the server. my start.bat starts another .bat so the bot itself doesn't die.
			path = "some-path-here" # the path again
			subprocess.call(join(path, f_name)) # actually starts the server

def blacklister(arg):
	with open('blacklisted.txt', 'a') as file:
		file.write(arg + "\n")

def blistchecker(ctx):
	with open('blacklisted.txt') as f:
		if str(ctx.author.id) in f.read():
			return True

@bot.event
async def on_message(ctx): # not actually sure why this isn't a command
	if ctx.content.startswith("s!snapshotoff"): # used to kill the snapshot server as it doesn't have an easy auto-shutdown. kills the process. it's not nice, but it works.
		if not blistchecker(ctx) == True:
			if bot.servertype == "snapshot":
				await ctx.channel.send("Are you sure you want to kill the snapshot-server? Abuse may lead to blacklisting. If you wish to continue, type `YES` within 15 seconds. (cAsE-senSitive).")

				def check(m):
					return m.content == "YES" and m.author == ctx.author

				try:
					await bot.wait_for("message", timeout=15.0, check=check)
				except asyncio.TimeoutError:
					await ctx.add_reaction('⚠️')
				else:
					if onchecker() == True: # makes sure that the server is actually on
						await ctx.channel.send("Closing the snapshot server. Some things may have rollbacked a little.")
						snapkill() # function to kill the process
			else:
				await ctx.channel.send("Snapshot server is not running at the moment.")

	await bot.process_commands(ctx) # enables commands


bot.run("your-bot-token-here. don't share it with anyone.")
