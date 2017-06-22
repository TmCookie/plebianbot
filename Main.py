import discord
import asyncio
import subprocess
import os.path
import os
import stat
import sys
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# checks after the discord message is starting with plz
    if message.content.startswith("plz") or message.content.startswith("Plz"):
        arg = message.content[4:]
        search = arg.split(' ')[0]
        check = arg.split(' ')
        server = message.server
        if str(server) == "None":
            ser = str(message.author)
        else:
            ser = str(message.server)
        if len(check) > 1:
            args = arg.split(' ', 1)[1]
            if os.path.exists('scripts/' + search):#checks if the plz script exist
                slashorno = subprocess.check_output(['./scripts/' + search, args]).decode('ascii') #parse the input so it can detect /
                if slashorno.startswith("/"): #if there is a slash
                    slasharg = slashorno[1:] #strips away not needed chars|
                    slashfinal = slasharg[:-1]#strips away not needed chars
                    await client.send_message(message.channel, subprocess.check_output(['./scripts/' + slashfinal]).decode('ascii')) #does the script that included slash
                else:
                    await client.send_message(message.channel, subprocess.check_output(['./scripts/' + search, args]).decode('ascii')) # if it dosent find / it will run just the script
            elif os.path.exists('userscripts/' + ser + "/" + search):#checks if the plz script is in userscripts
                slashorno = subprocess.check_output(['./userscripts/' + ser + "/" + search, args]).decode('ascii')  #parse the input so it can detect /
                if slashorno.startswith("/"): #if there is a slash
                    slasharg = slashorno[1:]#strips away not needed chars
                    slashfinal = slasharg[:-1]#strips away not needed chars
                    await client.send_message(message.channel, subprocess.check_output(['./scripts/' + slashfinal]).decode('ascii'))#does the script that included slash
                else:
                    await client.send_message(message.channel, subprocess.check_output(['./userscripts/' + ser + "/" + search, args]).decode('ascii'))# if it dosent find / it will run just the script
            elif arg.startswith("make"):#checks for plz make
                nomake = arg[5:]#removes make from plz make
                makename = nomake.split(' ')[0]#parseing
                if os.path.exists('scripts/' + makename):#check if you are trying to overwrite scripts
                    await client.send_message(message.channel, "exist! you cant overwrite main scripts!")
                else:
                    if str(server) == "None":
                        folder = str(message.author)
                    else:
                        folder = str(message.server)
                    if not os.path.exists('userscripts/' + folder):
                        os.makedirs('userscripts/' + folder)
                        file = open("userscripts/" + folder + "/" + makename, 'w+') #make userscript
                        makecommand = nomake.split(" ", 1)[1]
                        file.write('#!/usr/bin/python3')
                        file.write("\n")
                        file.write('print("""' + makecommand + '""")')#uses the simple print("""text here""")
                        await client.send_message(message.channel, "Command made! use: plz " + makename)
                        file.close()
                        st = os.stat('userscripts/' + folder + "/" + makename)
                        os.chmod('userscripts/' + folder + "/" + makename, st.st_mode | stat.S_IEXEC)#chmod because damn thing makes unrunable programms
                    else:
                        file = open("userscripts/" + folder + "/" + makename, 'w+') #make userscript
                        makecommand = nomake.split(" ", 1)[1]
                        file.write('#!/usr/bin/python3')
                        file.write("\n")
                        file.write('print("""' + makecommand + '""")')#uses the simple print("""text here""")
                        await client.send_message(message.channel, "Command made! use: plz " + makename)
                        file.close()
                        st = os.stat('userscripts/' + folder + "/" + makename)
                        os.chmod('userscripts/' + folder + "/" + makename, st.st_mode | stat.S_IEXEC)#chmod because damn thing makes unrunable programms
            elif arg.startswith("delete"): #checks for delete
                filenamedel = arg[7:]#stripts delete
                if str(server) == "None":
                    deld = str(message.author)
                else:
                    deld = str(message.server)
                if os.path.exists('scripts/' + filenamedel):#check if it exist in scripts
                    await client.send_message(message.channel, "you cant delete main scripts!") # you cant delete main scripts
                elif not os.path.exists("userscripts/" + deld + "/" + filenamedel):
                    await client.send_message(message.channel, "cant find script!")
                else:
                    os.remove("userscripts/" + deld + "/" + filenamedel) # else: just remove the script
                    await client.send_message(message.channel, "Deleted") #deleted

            else:
                await client.send_message(message.channel, "script does not exist!") # if it dosent exist after plz, dosent exist
        else:
            if arg.startswith("help"):
                await client.send_message(message.channel, subprocess.check_output(['./scripts/help', str(server), str(message.author)]).decode('ascii'))
            elif os.path.exists('scripts/' + search):#checks if the plz script exist
                slashorno = subprocess.check_output(['./scripts/' + search]).decode('ascii') #parse the input so it can detect /
                if slashorno.startswith("/"): #if there is a slash
                    slasharg = slashorno[1:] #strips away not needed chars
                    slashfinal = slasharg[:-1]#strips away not needed chars
                    await client.send_message(message.channel, subprocess.check_output(['./scripts/' + slashfinal]).decode('ascii')) #does the script that included slash
                else:
                    await client.send_message(message.channel, subprocess.check_output(['./scripts/' + search]).decode('ascii')) # if it dosent find / it will run just the script
            elif os.path.exists('userscripts/' + ser + "/" + search):#checks if the plz script is in userscripts
                slashorno = subprocess.check_output(['./userscripts/' + ser + "/" + search]).decode('ascii')  #parse the input so it can detect /
                if slashorno.startswith("/"): #if there is a slash
                    slasharg = slashorno[1:]#strips away not needed chars
                    slashfinal = slasharg[:-1]#strips away not needed chars
                    await client.send_message(message.channel, subprocess.check_output(['./scripts/' + slashfinal]).decode('ascii'))#does the script that included slash
                else:
                    await client.send_message(message.channel, subprocess.check_output(['./userscripts/' + ser + "/" + search]).decode('ascii'))# if it dosent find / it will run just the script
            else:
                await client.send_message(message.channel, "script does not exist!") # if it dosent exist after plz, dosent exist
        print(search)
with open('apitoken.txt') as f: api = f.read() #api token
client.run(api) #run discord
