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
        card = randint(1,52)
        if card == 1:
            await bot.send_message(message.channel, 'https://cdn.shopify.com/s/files/1/0080/8372/products/tattly_peagreen_designs_ace_of_hearts_web_applied_05_grande.jpg')
        if card == 2:
            await bot.send_message(message.channel, 'https://c2.staticflickr.com/8/7216/7377124070_d108805c49_b.jpg')
        if card == 3:
            await bot.send_message(message.channel, 'https://www.cornholeantics.com/image/cache/data/Gambling/The-Ace-of-Clubs-Cornhole-Boards-1000x563.jpg')
        if card == 4:
            await bot.send_message(message.channel, 'https://www.amazingtattooideas.com/wp-content/uploads/2016/11/Ace-of-Spades-Card-Forearm-Tattoo.jpg')
        if card == 5:
            await bot.send_message(message.channel, 'http://spiritualnutrition.org/wp-content/uploads/2012/01/200px-Playing_card_spade_2.svg_.png')
        if card == 6:
            await bot.send_message(message.channel, 'https://coloringgames.com/uploads/605/2-of-clubs-alice-in-wonderland-coloring-page.png')
        if card == 7:
            await bot.send_message(message.channel, 'https://cdn.dribbble.com/users/738113/screenshots/2836487/screenshot_2.png')
        if card == 8:
            await bot.send_message(message.channel, 'https://i.pinimg.com/originals/6e/c6/8a/6ec68a417cfa4955fec3b5adfbd7f81e.jpg')
        if card == 9:
            await bot.send_message(message.channel, 'https://orig00.deviantart.net/6872/f/2012/093/1/5/3_of_clubs_tattoo_by_mewmew88-d4uwjn3.jpg')
        if card == 10:
            await bot.send_message(message.channel, 'https://orig00.deviantart.net/6872/f/2012/093/1/5/3_of_clubs_tattoo_by_mewmew88-d4uwjn3.jpg')
        if card == 11:
            await bot.send_message(message.channel, 'https://cardseer.files.wordpress.com/2016/05/3d.png')
        if card == 12:
            await bot.send_message(message.channel, 'https://orig00.deviantart.net/648f/f/2012/226/9/4/3_of_hearts_card_final__by_minaalthea-d5b4isb.jpg')
        if card == 13:
            await bot.send_message(message.channel, 'https://i.pinimg.com/736x/0a/43/9d/0a439d2f15f9555dc63a6ddd58294ce2--playing-card-design-trump-card.jpg')
        if card == 14:
            await bot.send_message(message.channel, 'https://stickershop.line-scdn.net/stickershop/v1/product/1114553/LINEStorePC/main@2x.png')
        if card == 15:
            await bot.send_message(message.channel, 'http://destiny-cards.co.uk/wp-content/uploads/2015/05/four-of-diamonds-l.png')
        if card == 16:
            await bot.send_message(message.channel, 'https://4vector.com/i/free-vector-four-of-hearts-clip-art_105028_Four_Of_Hearts_clip_art_hight.png')
        if card == 17:
            await bot.send_message(message.channel, 'http://keyassets.timeincuk.net/inspirewp/live/wp-content/uploads/sites/5/2016/02/5-of-Clubs-630x474.jpg')
        if card == 18:
            await bot.send_message(message.channel, 'https://previews.123rf.com/images/alancotton/alancotton1504/alancotton150400242/39188986-outline-map-of-the-state-of-florida-and-used-as-the-5-of-spades-motif-in-a-playing-card.jpg')
        if card == 19:
            await bot.send_message(message.channel, 'https://cdn.dribbble.com/users/151467/screenshots/2934264/drawing5ofdiamondsearthimgur.jpg')
        if card == 20:
            await bot.send_message(message.channel, 'https://cdn.bandmix.com/bandmix_us/media/237/237769/611547-p.jpg')
        if card == 21:
            await bot.send_message(message.channel, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Playing_card_club_6.svg/2000px-Playing_card_club_6.svg.png')
        if card == 22:
            await bot.send_message(message.channel, 'https://i.ytimg.com/vi/KsTO3lmoGBk/maxresdefault.jpg')
        if card == 23:
            await bot.send_message(message.channel, 'https://playingcardcollector.files.wordpress.com/2013/07/40_thoughts_playing_cards_six_of_diamonds.jpg')
        if card == 24:
            await bot.send_message(message.channel, 'https://i.pinimg.com/originals/b4/ac/3f/b4ac3f6ac338f2d414f77eca2ef9069e.jpg')
        if card == 25:
            await bot.send_message(message.channel, 'https://s3.amazonaws.com/img.playingarts.com/two-big/7-of-clubs-adhemas-batista.jpg')
        if card == 26:
            await bot.send_message(message.channel, 'https://i.ytimg.com/vi/SpYuvKjlRFE/maxresdefault.jpg')
        if card == 27:
            await bot.send_message(message.channel, 'https://m.media-amazon.com/images/I/91Pa0RbFVFL._CLa%7C2140,2000%7C61wU5NxycUL.png%7C0,0,2140,2000+648.0,529.0,809.0,971.0._UX342_.png')
        if card == 28:
            await bot.send_message(message.channel, 'https://i.pinimg.com/736x/e2/0a/b0/e20ab0e4d1b9ac5052f91b1e65fff1a8--the-great-the-ojays.jpg')
        if card == 29:
            await bot.send_message(message.channel, 'http://printbymagic.com/wp-content/uploads/2015/09/64-8-OF-CLUBS-PRINTED-ON-RED-BACK.jpg')
        if card == 30:
            await bot.send_message(message.channel, 'https://pre00.deviantart.net/3ad9/th/pre/f/2013/106/6/9/eight_of_spades_by_vikiusha-d61y28o.jpg')
        if card == 31:
            await bot.send_message(message.channel, 'http://ocw.nur.ac.rw/OCWExternal/Akamai/6/6.163/f05/imagegallery/images/card2.jpg')
        if card == 32:
            await bot.send_message(message.channel, 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Playing_card_heart_8.svg/1000px-Playing_card_heart_8.svg.png')
        if card == 33:
            await bot.send_message(message.channel, 'https://i.ytimg.com/vi/o19amQ-7dz4/maxresdefault.jpg')
        if card == 34:
            await bot.send_message(message.channel, 'https://previews.123rf.com/images/dinky123uk/dinky123uk1005/dinky123uk100500418/16684505-9-of-spades-playing-card.jpg')
        if card == 35:
            await bot.send_message(message.channel, 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/0bfa6838711121.560697e2a12fb.jpg')
        if card == 36:
            await bot.send_message(message.channel, 'http://www.cabinfevercreations.com/uploads/7/1/9/8/7198529/s135188204601019855_p123_i1_w2016.jpeg')
        if card == 37:
            await bot.send_message(message.channel, 'https://mir-s3-cdn-cf.behance.net/project_modules/disp/5ccbc922167865.560459eb5d16e.jpg')
        if card == 38:
            await bot.send_message(message.channel, 'https://i.pinimg.com/originals/61/82/c3/6182c3f015ccd3c3cdc2b35814c91a86.jpg')
        if card == 39:
            await bot.send_message(message.channel, 'https://img00.deviantart.net/b499/i/2009/186/e/8/mal_10_diamonds_tattoo_ver__by_koshii.jpg')
        if card == 40:
            await bot.send_message(message.channel, 'https://i.pinimg.com/736x/e7/7c/21/e77c217648cf9e9c2677b91f74e516b3--house-of-cards-card-deck.jpg')
        if card == 41:
            await bot.send_message(message.channel, 'https://maskawraps.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/c/a/card_-_jack_of_clubs_1.jpg')
        if card == 42:
            await bot.send_message(message.channel, 'http://lghttp.46505.nexcesscdn.net/801C770/images/media/catalog/product/cache/1/image/650x/040ec09b1e35df139433887a97daa66f/l/a/large_1951_p5106_2x3_jack_spades_4_1.jpg')
        if card == 43:
            await bot.send_message(message.channel, 'https://orig00.deviantart.net/7ee5/f/2007/001/a/c/jack_of_diamonds_by_fayrenpickpocket.jpg')
        if card == 44:
            await bot.send_message(message.channel, 'https://i.pinimg.com/originals/7d/d2/73/7dd2731f455934464bbf78c033058d2a.jpg')
        if card == 45:
            await bot.send_message(message.channel, 'http://www.quirksee.org/wp-content/uploads/2013/06/Freddie-Mercury-as-the-Queen-of-Clubs-Imgur.jpg')
        if card == 46:
            await bot.send_message(message.channel, 'https://www.featurepics.com/FI/Thumb300/20110612/Queen-Spades-1911581.jpg')
        if card == 47:
            await bot.send_message(message.channel, 'https://pre00.deviantart.net/d526/th/pre/i/2015/076/b/1/harley_quinn__queen_of_diamonds_by_timberking-d8m1046.jpg')
        if card == 48:
            await bot.send_message(message.channel, 'https://cdn.shopify.com/s/files/1/1478/7218/products/Whosits_Red-Queen-Crewneck_Alice-Wonderland_BACK_394x.jpg')
        if card == 49:
            await bot.send_message(message.channel, 'https://cdn.dribbble.com/users/740188/screenshots/2946187/koc_seankerry_1x.jpg')
        if card == 50:
            await bot.send_message(message.channel, 'https://c8.alamy.com/comp/B8Y7CM/king-of-spades-with-a-gun-B8Y7CM.jpg')
        if card == 51:
            await bot.send_message(message.channel, 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/English_pattern_king_of_diamonds.svg/2000px-English_pattern_king_of_diamonds.svg.png')
        if card == 52:
            await bot.send_message(message.channel, 'https://cdn.shopify.com/s/files/1/2024/0301/products/AF1110-A_760x.jpg')
    if message.content.startswith('--TBOT'):
        if message.author.id == '442765136550297610':
                exit()
    with open('users.pkl', 'wb') as fp:
            pickle.dump(user, fp, protocol=pickle.HIGHEST_PROTOCOL)
bot.run(os.environ['TOKEN'])