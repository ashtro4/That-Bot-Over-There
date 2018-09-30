import os
card = 0
import pickle
import discord
from random import randint
from time import sleep
import asyncio
import requests
import aiohttp
from bs4 import BeautifulSoup
import platform
import os
user = {}
notes = {}
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
loop = asyncio.get_event_loop()
bot = commands.Bot(command_prefix='-', description='Hey, dude. You see that bot over there?')
bot.remove_command('help')
dotenv_path = join(dirname(__file__), 'stuff.env')
load_dotenv(dotenv_path)
TOKEN = os.getenv('TOKEN')
CLIENTID = os.getenv('CLIENTID')
async def get(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
				return await response.text()
async def getscp(scpid): #asynchronously defines the getscp function
	try: #checks to see if the page is valid
		html = await get('http://scp-wiki.wikidot.com/scp-'+scpid) #this goes to the scp website and sets the html variable to the returned html
	except:
		return 'Error' #if the page causes an exception then return error
	soup=BeautifulSoup(html,'html.parser') #sets a beautifulsoup object to the html

	page_content=soup.find(id='page-content') #finds the html object with the id "page-content"
	try: #tests to see if an image exists
		image_link=soup.find(class_='scp-image-block').img['src'] #finds an image with the class "scp-image-block" which is what the image is set to
	except: #if the image and/or the caption doesnt exist then set both to None
		image_link=None
	page_content=page_content.findAll('p')[:-1] #finds all the p tags in the previously defined variable and redefines the variable. (the [:-1] at the end removes the last html item which is just the page number which we dont need)
	page_text=[] #creates a new list called page_text
	for i in page_content: #goes through all the page_content items
		try:
			i.parent['class'] #tests if the parent of the paragraph (the div that it's inside of) exists
		except:
			page_text.append(str(i.text)) #if it doesnt exist then thats good and it adds it to the page_text list
	page_text=page_text[0] + "\n" + page_text[1] + "\n" + page_text[2] + "\n" + page_text[3]

	return {'page_text':page_text,'image_link':image_link} #returns a dict with all the found info
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game=discord.Game(name="'-help'"))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0'.format(os.environ['CLIENTID']))
    print('------')
@bot.event
async def on_message(message):
    server = message.server.id
    person = message.author.id
    thing = str(message.author)
    try:
        with open('feedback.pkl', mode,'rb') as myfile:
            feedback = pickle.load(myfile)
    except:
        feedback = {}
    try:
        with open('users.pkl', mode='rb') as myfile:
            user = pickle.load(myfile)
    except:
        user = {}
    try:
        with open('notes.pkl', mode='rb') as myfile:
            notes = pickle.load(myfile)
    except:
        notes = {}
    try:
        taco = notes[message.author.id + "_notes_" + thing]
    except:
        notes[message.author.id + "_notes_" + thing] = {}
    try:
        forgeddaboutit = user[server + "_" + person + "_created?"]
    except:
        user[server + "_" + person + "_created?"] = 1
        user[server + "_" + person + "_balance"] = 100
    if message.author == bot.user:
    		return
    if message.author.bot:
                return
    if message.content.startswith('-scp '):
        async def main():
            scp_number = message.content[len('-scp '):]
            scp = await getscp(scp_number)
            if scp=='Error':
                    await bot.send_message(message.channel, '```Error```')
            else:
                print(scp['image_link'])
                if scp['image_link'] == None:
                    await bot.send_message(message.channel, '```{}```'.format(scp['page_text']))
                else:
                    await bot.send_message(message.channel, '{}'.format(scp['image_link']) + '\n```{}```'.format(scp['page_text']))
        await main()
    try:
        taco = feedback[message.author.id]
    except:
        feedback[message.author.id + "_feedback"] = {}
    if message.content.startswith('-feedback list') or message.content.startswith('-fb l') or message.content.startswith('-feedback l') or message.content.startswith('-fb list'):
        try:
            with open('feedback.pkl',  mode='rb') as myfile:
                feedback = pickle.load(myfile)
        except:
            feedback = {}
        if message.content.startswith('-feedback l '):
            feedback_name = message.content[len('-feedback l '):]
        if message.content.startswith('-fb l'):
            feedback_name = message.content[len('-fb l'):]
        if message.content.startswith('-feedback list'):
            feedback_name = message.content[len('-feedback list'):]
        if message.content.startswith('-fb list'):
            feedback_name = message.content[len('-fb list'):]
        try:
            await bot.send_message(message.channel, "```" + str(feedback[message.author.id + "_feedback_replied"].keys()) + "```")
        except:
            await bot.send_message(message.channel, "```Error!```")
    if message.content.startswith('-feedback read ') or message.content.startswith('-fb read ') or message.content.startswith('-fb r ') or message.content.startswith('-feedback r '):
        try:
            with open('feedback.pkl',  mode='rb') as myfile:
                feedback = pickle.load(myfile)
        except:
            feedback = {}
        if message.content.startswith('-feedback r '):
            feedback_read = message.content[len('-feedback r '):]
            print(feedback_read)
        if message.content.startswith('-fb r '):
            feedback_read = message.content[len('-fb r '):]
            print(feedback_read)
        if message.content.startswith('-feedback read '):
            feedback_read = message.content[len('-feedback read '):]
            print(feedback_read)
        if message.content.startswith('-fb read '):
            feedback_read = message.content[len('-fb read '):]
            print(feedback_read)
        try:
            await bot.send_message(message.channel, "```" + feedback[message.author.id + "_feedback_replied"][feedback_read] + "```")
        except:
            await bot.send_message(message.channel, "```Error : Feedback does not exist.```")
    if message.content.startswith('-feedback write ') or message.content.startswith('-fb write ') or message.content.startswith('-fb wr ') or message.content.startswith('-feedback wr '):
        if message.content.startswith('-feedback wr '):
            feedback_info = message.content[len('-feedback wr '):]
        if message.content.startswith('-fb wr '):
            feedback_info = message.content[len('-fb wr '):]
        if message.content.startswith('-feedback write '):
            feedback_info = message.content[len('-feedback write '):]
        if message.content.startswith('-fb write '):
            feedback_info = message.content[len('-fb write '):]
        feedback_split = feedback_info.split()
        feedback_name = feedback_split[0]
        feedback_message = feedback_info[len(feedback_name + " "):]
        thing = str(message.author)
        feedback[message.author.id + "_feedback"][feedback_name] = feedback_message
        with open('feedback.pkl', mode='wb') as myfile:
            pickle.dump(feedback, myfile, protocol=pickle.HIGHEST_PROTOCOL)
        await bot.send_message(message.channel, "```Feedback was sent successfully.```")
    if message.content.startswith('-notepad overwrite') or message.content.startswith('-np overwrite') or message.content.startswith('-np o') or message.content.startswith('-notepad o'):
        notes[message.author.id + "_overwrite_or_append"] = 'overwrite'
        await bot.send_message(message.channel, "```Writing now overwrites instead of appends.```")
        with open('notes.pkl', mode='wb') as myfile:
            pickle.dump(notes, myfile, protocol=pickle.HIGHEST_PROTOCOL)
    if message.content.startswith('-notepad append') or message.content.startswith('-notepad a') or message.content.startswith('-np a') or message.content.startswith('-np append'):
        notes[message.author.id + "_overwrite_or_append"] = 'append'
        await bot.send_message(message.channel, "```Writing now appends instead of overwrites.```")
        with open('notes.pkl', mode='wb') as myfile:
            pickle.dump(notes, myfile, protocol=pickle.HIGHEST_PROTOCOL)
    if message.content.startswith('-notepad read ') or message.content.startswith('-notepad r ') or message.content.startswith('-np r ') or message.content.startswith('-np read '):
        try:
            server = message.server.id
            person = message.author.id
            thing = str(message.author)
            if message.content.startswith('-np read '):
                note_name = message.content[len("-np read "):]
            if message.content.startswith('-np r '):
                note_name = message.content[len("-np r "):]
            if message.content.startswith('-notepad read '):
                note_name = message.content[len("-notepad read "):]
            if message.content.startswith('-notepad r '):
                note_name = message.content[len("-notepad r "):]
            await bot.send_message(message.channel, "```" + notes[message.author.id + "_notes_" + thing][note_name] + "```")
        except:
            await bot.send_message(message.channel, "```Could not read note. Does it exist?```")
    if message.content.startswith('-notepad write ') or message.content.startswith('-notepad wr ') or message.content.startswith('-np wr ') or message.content.startswith('-np write '):
        server = message.server.id
        person = message.author.id
        thing = str(message.author)
        if message.content.startswith('-notepad write '):
            note_info_prepared = message.content[len('-notepad write '):]
        if message.content.startswith('-notepad wr '):
            note_info_prepared = message.content[len('-notepad wr '):]
        if message.content.startswith('-np wr '):
            note_info_prepared = message.content[len('-np wr '):]
        if message.content.startswith('-np write '):
            note_info_prepared = message.content[len('-np write '):]
        info_noteing = note_info_prepared.split()
        note_name = info_noteing[0]
        if message.content.startswith('-notepad write '):
            note_info = message.content[len('-notepad write ' + note_name + " "):]
        if message.content.startswith('-np wr '):
            note_info = message.content[len('-np wr ' + note_name + " "):]
        if message.content.startswith('-notepad wr '):
            note_info = message.content[len('-notepad wr ' + note_name + " "):]
        if message.content.startswith('-np write '):
            note_info = message.content[len('-np write ' + note_name + " "):]
        try:
            taco = notes[message.author.id + "_overwrite_or_append"]
        except:
            await bot.send_message(message.channel, "```Use the '-notepad append/overwrite' command to set how you want to save your notes before you write one.```")
        if notes[message.author.id + "_overwrite_or_append"] == 'overwrite' or notes[message.author.id + "_overwrite_or_append"] == 'o':
            try:
                prev_note = notes[message.author.id + "_notes_" + thing][note_name]
                databsenotes[message.author.id + "_notes_" + thing][note_name] = note_info
                await bot.send_message(message.channel, "```Note overwritten!```")
            except:
                notes[message.author.id + "_notes_" + thing][note_name] = note_info
                await bot.send_message(message.channel, "```Note created!```")
        if notes[message.author.id + "_overwrite_or_append"] == 'append' or notes[message.author.id + "_overwrite_or_append"] == 'a':
            try:
                prev_note = notes[message.author.id + "_notes_" + thing][note_name]
                notes[message.author.id + "_notes_" + thing][note_name] = prev_note + " " + note_info
                await bot.send_message(message.channel, "```Note appended!```")
            except:
                notes[message.author.id + "_notes_" + thing][note_name] = note_info
                await bot.send_message(message.channel, "```Note created!```")
        with open('notes.pkl', mode='wb') as myfile:
            pickle.dump(notes, myfile, protocol=pickle.HIGHEST_PROTOCOL)
    if message.content.startswith('-notepad list') or message.content.startswith('-notepad l') or message.content.startswith('-np list') or message.content.startswith('-np l'):
        server = message.server.id
        person = message.author.id
        thing = str(message.author)
        note_list = str(notes[person+"_notes_"+thing].keys())
        notesss = 'Notes_Written'
        note_list = note_list[len("dict_keys"):]
        note_list = notesss + note_list
        if note_list == "Notes_Written([])":
            note_list = 'You have no notes!'
        await bot.send_message(message.channel, "```" + note_list + "```")
    if message.content.startswith('-notepad clear') or message.content.startswith('-np clear') or message.content.startswith('-np c') or message.content.startswith('-notepad c'):
        x = 1
        if message.content.startswith('-notepad clear'):
            message_cleared = message.content[len('-notepad clear '):]
            x = 0
        if message.content.startswith('-np clear'):
            message_cleared = message.content[len('-np clear '):]
            x = 0
        if message.content.startswith('-np c'):
            if x != 0:
                message_cleared = message.content[len('-np c '):]
        if message.content.startswith('-notepad c'):
            if x != 0:
                message_cleared = message.content[len('-notepad c '):]
        if message_cleared == "":
            notes[message.author.id + "_notes_" + thing] = {}
            with open('notes.pkl', mode='wb') as myfile:
                pickle.dump(notes, myfile, protocol=pickle.HIGHEST_PROTOCOL)
            await bot.send_message(message.channel, "```Notepad Cleared!```")
        else:
            try:
                print(message_cleared)
                del notes[message.author.id + "_notes_" + thing][message_cleared]
                with open('notes.pkl', mode='wb') as myfile:
                    pickle.dump(notes, myfile, protocol=pickle.HIGHEST_PROTOCOL)
                await bot.send_message(message.channel, "```" + message_cleared + " was removed from your notes.```")
            except:
                await bot.send_message(message.channel, "```Error deleting note. Does it exist?```")
    if message.content.startswith('-balance'):  
        server = message.server.id
        person = message.author.id
        await bot.send_message(message.channel, user[server + "_" + person + "_balance"])
    if message.content.startswith('-say'):
        words = message.content[len("-say"):]
        await bot.send_message(message.channel, words)
    if message.content.startswith('-online'):
        await bot.send_message(message.channel, "TBOT is online!")
    if message.content.startswith('-help'):
            await bot.send_message(message.channel, "```'-' is my prefix! \nThese are my commands! \n-info : gives my info! \n-balance : (placeholder) \n-scp (scp_num) : shows an scp description with picture [credit goes to mat]\n-notepad write (note_name) (note_contents) \n-notepad read (note name) : read a note with your specifed name \n-notepad overwrite/append : choose how notes are saved \n-notepad clear (optional arg) : clear either all notes or 1 specific \n-notepad list : list names of written notes.\n-feedback write (Name) (Contents) : writes a message directly to ashtro4 \n-feedback list : lists the feedback you've created that I've responded to \n-feedback read (Name) : read feedback that I've responded to. (Get name from -feedback list)\n-help : brings up this message! \n-hi : hello!\n-pizza : brings up a great slice of pizza \n-card : brings up a random card from a deck of 52. \n-say : I repeat anything you say```")
    if message.author.id != 'macaroni':  
        if message.content.startswith('-pizza'):
            pizza = randint(1,12)
            if pizza == 1:
                await bot.send_message(message.channel, "https://www.refrigeratedfrozenfood.com/ext/resources/issues/2017/July/convenience/iStock-650976180.jpg?1499362198")
            if pizza == 2:
                await bot.send_message(message.channel, 'http://roundtablepizzasurrey.com/wp-content/uploads/2017/08/chicken_tandoori_pizza.png')
            if pizza == 3:
                await bot.send_message(message.channel, "http://paypizzapal.com/wp-content/uploads/2014/01/buy-Dominos-with-PayPal.jpg")
            if pizza == 4:
                await bot.send_message(message.channel, "https://www.cicis.com/media/1243/pizza_adven_zestypepperoni.png")
            if pizza == 5:
                await bot.send_message(message.channel, "https://www.messforless.net/wp-content/uploads/2018/01/2-ingredient-pizza-dough-weight-watchers-9.jpg")
            if pizza == 6:
                await bot.send_message(message.channel, "https://www.cicis.com/media/1137/pizza_trad_alfredo.png")
            if pizza == 7:
                await bot.send_message(message.channel, "https://cdn.websites.hibu.com/c2c577b59fcc4f8eae2a5d40ed3a2fa8/dms3rep/multi/desktop/slider-3.jpg")
            if pizza == 8:
                await bot.send_message(message.channel, "https://www.jackspizza.com/media/8996/Jacks-hero.jpg")
            if pizza == 9:
                await bot.send_message(message.channel, 'https://cdn.nexternal.com/cincyfav3/images/larosas_cheese_pizzas.jpg')
            if pizza == 10:
                await bot.send_message(message.channel, "http://sugardale.com/sites/default/files/Mac-and-Cheese-Pizza_final.jpg")
            if pizza == 11:
                await bot.send_message(message.channel, "https://c8.alamy.com/comp/CEWB67/cooked-deep-dish-red-baron-pizza-with-pepperoni-topping-inside-microwave-CEWB67.jpg")
            if pizza == 12:
                await bot.send_message(message.channel, 'https://www.biggerbolderbaking.com/wp-content/uploads/2016/01/IMG_9114-1024x682.jpg')
    if message.content.startswith('-info'):
	    sleep(.5)
	    await bot.send_message(message.channel, "```I am TBOT! \n Description: Hey dude, you see That Bot Over There? \n Invite code: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0```".format(os.environ['CLIENTID']))
    if message.content.startswith('-hi'):
            await bot.send_message(message.channel, 'Hello!')
    if message.content.startswith('-card'):
        arr = []
        with open("cards.txt","r") as file:
            line = file.readline()
            while line:
              line = file.readline()
              if line == '':
                continue
              else:
                line = line.replace("\n","")
                arr.append(line)
        await bot.send_message(message.channel,random.choice(arr))


    if message.content.startswith('--TBOT'):
        if message.author.id == '442765136550297610':
                exit()
    with open('users.pkl', 'wb') as fp:
            pickle.dump(user, fp, protocol=pickle.HIGHEST_PROTOCOL)
bot.run(os.environ['TOKEN'])
