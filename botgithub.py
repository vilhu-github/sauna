#saunabot by vilhu

import discord
import discord.ext
from discord.ext import commands
import asyncio
import os
#import mcstatus
from mcstatus import MinecraftServer
import time
import subprocess
from pathlib import Path
import sys
from os.path import join
import requests

bot = commands.Bot(command_prefix = "!")


@bot.event
async def on_ready():
	print("Botti on yhdistetty Discordiin ja valmiina käyttöön.")
	#print("ID: " + bot.user.id + bot.user.name)
	await bot.change_presence(activity=discord.Activity(name="ServerDomainHere", type=1))
	abc = 0

user = 'x'
key = 'y'

@bot.event
async def on_message(message):
	if message.content.startswith('!saunamc'):
		try:
			server = MinecraftServer("127.0.0.1", 25566)
			status = server.status()
			if status.players.online == 0:
				#await trigger_typing(channel)
				time.sleep(1)
				embed = discord.Embed(title="SaunaMC palvelimen tila", color=0x00ff00)
				embed.set_thumbnail(url="https://www.shareicon.net/data/256x256/2016/11/15/853176_sauna_512x512.png")
				embed.add_field(name="Pelaamassa: ", value=status.players.online, inline=False)
				embed.add_field(name="Ping: ", value=status.latency, inline=False)
				embed.set_footer(text="z")
				await message.channel.send(embed=embed)
				#await message.channel.send("Palvelin vastasi ajassa {0}ms, pelaajia: {1}".format(status.latency, status.players.online))
			elif status.players.online > 0:
				#await trigger_typing(channel)
				#del abc
				time.sleep(1)
				server2 = MinecraftServer("127.0.0.1", 25566)
				query = server2.query()
				status2 = server2.status()
				#await message.channel.send("Palvelimella pelaa tällä hetkellä: {0} ".format(", ".join(query.players.names)))
				#await message.channel.send("Palvelin vastasi ajassa: {0}ms ".format(status.latency))
				embed2 = discord.Embed(title="SaunaMC palvelimen tila", color=0x00ff00)
				embed2.set_thumbnail(url="https://www.shareicon.net/data/256x256/2016/11/15/853176_sauna_512x512.png")
				embed2.add_field(name="Pelaamassa:", value="{0}".format(", ".join(query.players.names), inline=False))
				embed2.add_field(name="Ping: ", value=status2.latency, inline=False)
				embed2.set_footer(text="z")
				await message.channel.send(embed=embed2)
		except:
			embed3 = discord.Embed(title="SaunaMC palvelimen tila", color=0xff0000)
			embed3.set_thumbnail(url="https://www.shareicon.net/data/256x256/2016/11/15/853176_sauna_512x512.png")
			embed3.add_field(name="Pelaamassa: ", value="Palvelin näyttää olevan pois päältä. HUOMIO: Hexxit-palvelin ei tue tätä komentoa.", inline=False)
			embed3.add_field(name="Ping: ", value="ConnectionRefusedError: [WinError 10061]", inline=False)
			embed3.set_footer(text="z")
			await message.channel.send(embed=embed3)
			#await message.channel.send("Palvelin näyttää olevan pois päältä.")
	elif message.content.startswith("!saunapäälle vanilla"):
		role = discord.utils.get(message.guild.roles, name="mcadm")
		if role in message.author.roles:
			try:
				server4 = MinecraftServer("127.0.0.1", 25566)
				status6 = server4.status()
				time.sleep(3)
				if status6.players.online >= 0:
					#await trigger_typing(channel)
					time.sleep(1)
					await message.channel.send("Komentoa ei voitu suorittaa, palvelin on jo päällä.")
			except:
				for f_name in os.listdir("z"): #path goes here
					if f_name.endswith("start.bat"):
						osos = os.getcwd()
						polku = "z" #path goes here
						subprocess.call(join(polku, f_name))
						#await trigger_typing(channel)
						time.sleep(1)
						await message.channel.send("Käynnistetään vanilla-palvelin...")
						time.sleep(4)
						await message.channel.send(content="Palvelimen käynnistys onnistui, voit varmistaa päälläolon komennolla !saunamc.")
						time.sleep(6)
		else:
			#await trigger_typing(channel)
			time.sleep(1)
			await message.channel.send("Sinulla ei ole oikeutta suorittaa tätä komentoa. Pyydä käyttäjää mcadm-roolilla suorittamaan komento.")

	elif message.content.startswith("!saunapäälle hexxit"):
		role = discord.utils.get(message.guild.roles, name="mcadm")
		if role in message.author.roles:
			try:
				server7 = MinecraftServer("127.0.0.1", 25566)
				query7 = server7.query()
				print(query7.players.names)
				#await trigger_typing(channel)
				time.sleep(1)
				await message.channel.send("Komentoa ei voitu suorittaa, palvelin on jo päällä.")
			except:
				for f_name in os.listdir("z"): #path goes here
					if f_name.endswith("start.bat"):
						osos = os.getcwd()
						polku = "z" #path goes here
						subprocess.call(join(polku, f_name))
						#await trigger_typing(channel)
						time.sleep(1)
						await message.channel.send("Käynnistetään Hexxit-palvelin...")
						time.sleep(4)
						await message.channel.send("Palvelimen käynnistys onnistui, voit varmistaa päälläolon komennolla !saunamc.")
		else:
			#await trigger_typing(channel)
			time.sleep(1)
			await message.channel.send("Sinulla ei ole oikeutta suorittaa tätä komentoa. Pyydä käyttäjää mcadm-roolilla suorittamaan komento.")


bot.run("asd")
