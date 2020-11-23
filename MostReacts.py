#Created by Nick Alvarez (https://github.com/nicky189) (https://www.nalvarez.net)
#Most Reacts Bot

#I could not find anything that tallied up reactions so I did it myself.
#You WILL need to modify this code for this to work properly. Notably: Token, Channel_IDs, Channel_Names, commands
#This website is your best friend: https://discordpy.readthedocs.io/en/latest/api.html#


import os
import discord
import asyncio
import math
import copy
from datetime import datetime
from discord import Game
from discord.ext.commands import Bot
from discord import TextChannel
from discord.utils import get
from discord.ext import commands

TOKEN = "YourTokenHere"
client = discord.Client()

c_btt = SomeInt #Channel ID for bot-torture-testing

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

Channel_IDs = [int1, int2, int3...]
Channel_Names = ['name1', 'name2', 'name3'...]

btt_channel = client.get_channel(c_btt)

#Class definition for ranking objects
class MostReactedTop5:

    total_posts = 0

    def __init__(self, ranking, emoji_name, specific): #Rank (1-5), name of emoji (string for custom, copy and paste from emoji website for unicode), checking specific emoji (0/1)
        self.max_react_count = 0 #The highest reaction count
        self.max_react_name = 'Nothing' #The name of the emoji
        self.message_id_max = 0 #ID of the message with the most reactions
        self.message_text_max = 'Nothing' #Contents of the message
        self.message_author_max = 'Nobody' #Who wrote the message
        self.message_channel_max = 'nothing' #Where it was posted
        self.message_channel_class = None
        self.message_date_max = datetime(1971,1,1,00,00)
        self.message_file_max = None
        self.message_jump_url_max = None
        self.total_posts = 0 #Total posts searched
        self.reacted_posts = 0 #Searched posts with reaction
        self.reaction_count = 0 #Reactions found overall
        self.emoji_name = emoji_name #name of reaction to be searched
        self.post_ranking = ranking
        self.has_specific_emoji = specific
        
    async def printResults(self, rtn_channel):
        self.message_channel_class = client.get_channel(self.message_channel_class)
        self.message_file_max = await self.message_channel_class.fetch_message(self.message_file_max)
        self.message_file_max = self.message_file_max.attachments
        try: #Discord throws an HTTP exception even with this and the on_error event below
            if (self.message_file_max):
                await rtn_channel.send(content=(f'-------------------------\n**Rank: {self.post_ranking}**\nMessage from **{self.message_author_max}** in #{self.message_channel_max} on {self.message_date_max.strftime("%D")}:\n> {self.message_text_max}\nReceived {self.max_react_count} reactions with emoji {self.max_react_name}'), file=(await self.message_file_max[0].to_file()))
            else:
                await rtn_channel.send(f'-------------------------\n**Rank: {self.post_ranking}**\nMessage from **{self.message_author_max}** in #{self.message_channel_max} on {self.message_date_max.strftime("%D")}:\n> {self.message_text_max}\nReceived {self.max_react_count} reactions with emoji {self.max_react_name}')
        except HTTPException:
            await rtn_channel.send(f'-------------------------\n**Rank: {self.post_ranking}**\nMessage from **{self.message_author_max}** in #{self.message_channel_max} on {self.message_date_max.strftime("%D")}:\n> This message is too large to display. _Jump to the message instead: {self.message_jump_url_max}_\nReceived {self.max_react_count} reactions with emoji {self.max_react_name}')

#Gathers data from selected post and sends to selected class rank
async def reactionDataHandler(r, class_name, m, r_i):
    class_name.max_react_count = r.count
    class_name.message_id_max = m.id
    class_name.max_react_name = str(r_i)
    class_name.message_author_max = m.author.display_name
    class_name.message_text_max = m.clean_content
    class_name.message_channel_max = m.channel.name
    class_name.message_date_max = m.created_at
    class_name.message_file_max = m.id
    class_name.message_channel_class = m.channel.id
    class_name.message_jump_url_max = m.jump_url

#Unused, moved to printTop5()
async def classFixup(c):
    for j in range(0,5):
        c[j].post_ranking = (j+1)

#Finds top 5 posts
async def reactionRanker(r, class_name, m, r_i):
    class_name[0].reacted_posts += 1
    class_name[0].reaction_count += r.count    

    if (class_name[0].max_react_count < r.count):
        class_name[4] = copy.deepcopy(class_name[3])
        class_name[3] = copy.deepcopy(class_name[2])
        class_name[2] = copy.deepcopy(class_name[1])
        class_name[1] = copy.deepcopy(class_name[0])
        await reactionDataHandler(r, class_name[0], m, r_i)
    elif (class_name[1].max_react_count <= r.count):
        class_name[4] = copy.deepcopy(class_name[3])
        class_name[3] = copy.deepcopy(class_name[2])
        class_name[2] = copy.deepcopy(class_name[1])
        await reactionDataHandler(r, class_name[1], m, r_i)
    elif (class_name[2].max_react_count <= r.count):
        class_name[4] = copy.deepcopy(class_name[3])
        class_name[3] = copy.deepcopy(class_name[2])
        await reactionDataHandler(r, class_name[2], m, r_i)
    elif (class_name[3].max_react_count <= r.count):
        class_name[4] = copy.deepcopy(class_name[3])
        await reactionDataHandler(r, class_name[3], m, r_i)
    elif (class_name[4].max_react_count <= r.count):
        await reactionDataHandler(r, class_name[4], m, r_i)

#Loading message
async def progressMessage(class_name, f, search_percent, z, type_search, ch_posts):
    if (class_name.has_specific_emoji): #Specific emoji, any channel
        if (f == 0): #First message sent
            return (f'**Max :{class_name.emoji_name}: Reactions for Server** (loading... {search_percent}%)\nSearched {class_name.total_posts} posts, now checking #welcome')
        elif (f == 1): #Mid search of channel message
            return (f'**Max :{class_name.emoji_name}: Reactions for Server** (loading... {math.trunc(100*search_percent)}%)\nSearched {class_name.total_posts+ch_posts} posts, now checking #{Channel_Names[z+1]}')
        elif (f==2): #Final message modified to just the title
            return (f'**Max :{class_name.emoji_name}: Reactions for Server**\nSearched {class_name.total_posts} posts since 1/1/2020, {class_name.reacted_posts} of which had a total of {class_name.reaction_count} reactions.')
    elif (type_search == 0): #Specific channel, any emoji
        if (f == 0): #First message sent
            return (f'**Max Reactions for #{Channel_Names[z]}** (loading...)\nSearched {class_name.total_posts} posts, now checking #{Channel_Names[z]}')
        elif (f == 1): #Mid search of channel message
            return (f'**Max Reactions for #{Channel_Names[z]}** (loading...)\nSearched {class_name.total_posts+ch_posts} posts, now checking #{Channel_Names[z]}')
        elif (f==2): #Final message modified to just the title
            return (f'**Max Reactions for #{Channel_Names[z]}**\nSearched {class_name.total_posts} posts since 1/1/2020, {class_name.reacted_posts} of which had a total of {class_name.reaction_count} reactions.')
    elif (type_search == 2): #Any channel, any emoji
        if (f == 0): #First message sent
            return (f'**Max Reactions for Server** (loading... {search_percent}%)\nSearched {class_name.total_posts} posts, now checking #welcome')
        elif (f == 1): #Mid search of channel message
            return (f'**Max Reactions for Server** (loading... {math.trunc(100*search_percent)}%)\nSearched {class_name.total_posts+ch_posts} posts, now checking #{Channel_Names[z+1]}')
        elif (f==2): #Final message modified to just the title
            return (f'**Max Reactions for Server**\nSearched {class_name.total_posts} posts since 1/1/2020, {class_name.reacted_posts} of which had a total of {class_name.reaction_count} reactions.')

#Searches specific channel history
async def historySearch(z, class_name, search_percent, progress_id, channel, ch_posts, type_search):
    async for message in channel.history(limit=22000, after=datetime(2020, 1, 1)): #The options here can be modified to narrow/widen your search. Check Discord API
        if ((((ch_posts+1) % 443) - 442) >= 0):
            await progress_id.edit(content=(await progressMessage(class_name[0], 1, search_percent, z, type_search, ch_posts)))
        if (message.reactions): #Does the message have a reaction?
            for i in message.reactions: #Let's check each individual type of reaction on the message, if there are multiple
                reaction = i
                if (class_name[0].has_specific_emoji): #Searching for specific emoji
                    if (reaction.custom_emoji): #Not unicode
                        if (reaction.emoji.name == str(class_name[0].emoji_name)): #Matches name passed into class object
                            await reactionRanker(reaction, class_name, message, i)
                    elif (reaction.custom_emoji == 0): #Searching for unicode emoji
                        if (str(i) == str(class_name[0].emoji_name)):
                            await reactionRanker(reaction, class_name, message, i)
                else: #Searching for any emoji
                    await reactionRanker(reaction, class_name, message, i)
        ch_posts += 1
    class_name[0].total_posts += ch_posts
    print(f'Completed search of {ch_posts} in #{Channel_Names[z+1]}')

#Determines whether or not to search one channel or all of them
async def discordSearch(z, class_name, type_search, r_ch): #Iterator, name of list of classes, type of search (0: One channel, any emoji, 1: Any channel, one emoji, 2: Any channel, any emoji), name of channel to search if type_search = 0, otherwise pass None
    search_percent = 0
    ch_posts = 0 #Specific channel search amount
    btt_channel = client.get_channel(c_btt)
    await asyncio.sleep(1)
    if (type_search): #Searching entire server
        progress_id = await btt_channel.send(await progressMessage(class_name[0], 0, search_percent, z, type_search, ch_posts))
        for y in Channel_IDs:
            channel = client.get_channel(y)
            await historySearch(z, class_name, search_percent, progress_id, channel, ch_posts, type_search)
            z += 1
            search_percent = (z+1)/len(Channel_Names)
            if ((z + 1) < len(Channel_Names)):
                await progress_id.edit(content=(await progressMessage(class_name[0], 1, search_percent, z, type_search, ch_posts)))
            if (search_percent == 1):
                await progress_id.edit(content=(await progressMessage(class_name[0], 2, search_percent, z, type_search, ch_posts)))
    else: #Searching one channel
        channel = client.get_channel(Channel_IDs[z])
        #channel = client.get_channel(c_btt)
        progress_id = await channel.send(await progressMessage(class_name[0], 0, search_percent, z, type_search, ch_posts))
        ch_posts = 0 #Specific channel search amount
        #channel = client.get_channel(Channel_IDs[z])
        await historySearch(z, class_name, search_percent, progress_id, channel, ch_posts, type_search)
        print(f'Completed search of {ch_posts} in #{Channel_Names[z]}')
        await progress_id.edit(content=(await progressMessage(class_name[0], 2, search_percent, z, type_search, ch_posts)))

#Top 5 results are printed in channel the command was sent
async def printTop5(c, channel):
    for x in range(1, 5):
        c[x].post_ranking = (x+1)
        c[x].total_posts = c[0].total_posts
        
    await c[0].printResults(channel)
    await asyncio.sleep(1)
    await c[1].printResults(channel)
    await asyncio.sleep(1)
    await c[2].printResults(channel)
    await asyncio.sleep(1)
    await c[3].printResults(channel)
    await asyncio.sleep(1)
    await c[4].printResults(channel)

#@bot.command()
async def leave():
    print(f'Leave command entered.')
    #await btt_channel.send('Goodbye...')
    await client.logout()
@client.event
async def on_error(event, *args, **kwargs):
    message = args[0] #Gets the message object
    ch = client.get_channel(message.channel.id)
    await ch.send('An error occurred. Most likely, this message exceeded 2000 characters and could not be retrieved.')

@client.event
async def on_message(message):
    if message.author == client.user: #Make sure bot doesn't respond to itself
        return
    
    if message.content == '!leave': #Logoff
        await leave()

    #Custom emoji example
    if ((message.content == '!Command1NameHere') and (message.author.display_name == 'YourNickname')): #display_name not required if anyone should be able to call it
        y_iterator = -1
        ch = client.get_channel(message.channel.id)
        CE1st = MostReactedTop5(1, 'custom_emoji', 1)
        CE2nd = MostReactedTop5(2, 'custom_emoji', 1)
        CE3rd = MostReactedTop5(3, 'custom_emoji', 1)
        CE4th = MostReactedTop5(4, 'custom_emoji', 1)
        CE5th = MostReactedTop5(5, 'custom_emoji', 1)
        CE_Ranks = [CE1st, CE2nd, CE3rd, CE4th, CE5th]

        await discordSearch(y_iterator, CE_Ranks, 1, ch)
        channel = client.get_channel(message.channel.id)
        await printTop5(Phi_Ranks, channel)

    #Unicode example
    if ((message.content == '!Command2NameHere') and (message.author.display_name == 'YourNickname')): #Checks one emoji in all channels, type_search = 1
        y_iterator = -1
        ch = None
        Nf1st = MostReactedTop5(1, '😐', 1) #rank, specific emoji representation, one specific emoji flag
        Nf2nd = MostReactedTop5(2, '😐', 1)
        Nf3rd = MostReactedTop5(3, '😐', 1)
        Nf4th = MostReactedTop5(4, '😐', 1)
        Nf5th = MostReactedTop5(5, '😐', 1)
        Nf_Ranks = [Nf1st, Nf2nd, Nf3rd, Nf4th, Nf5th]

        await discordSearch(y_iterator, Nf_Ranks, 1, ch)
        channel = client.get_channel(message.channel.id)
        await printTop5(Nf_Ranks, channel)

    #Most reactions in one channel
    if ((message.content == '!most_reacts_here') and (message.author.display_name == 'YourNickname')): #Checks all emojis in one channel, type_search = 0
        y_iterator = Channel_IDs.index(message.channel.id) #Determines which channel the message was sent in and sets index to that channel based on Channel_ID[]
        ch = None
        #y_iterator = 7
        MaxChannel1st = MostReactedTop5(1, None, 0) #rank, no specific emoji representation, no specific emoji flag
        MaxChannel2nd = MostReactedTop5(2, None, 0)
        MaxChannel3rd = MostReactedTop5(3, None, 0)
        MaxChannel4th = MostReactedTop5(4, None, 0)
        MaxChannel5th = MostReactedTop5(5, None, 0)
        MaxChannel_Ranks = [MaxChannel1st, MaxChannel2nd, MaxChannel3rd, MaxChannel4th, MaxChannel5th]

        await discordSearch(y_iterator, MaxChannel_Ranks, 0, ch)
        channel = client.get_channel(message.channel.id)
        await printTop5(MaxChannel_Ranks, channel)

    #Most reactions in server
    if ((message.content == '!most_reacts_all') and (message.author.display_name == 'YourNickname')): #Checks all emojis in all channels, type_search = 2
        ch = None
        y_iterator = -1
        MaxServer1st = MostReactedTop5(1, None, 0) #rank, no specific emoji representation, no specific emoji flag
        MaxServer2nd = MostReactedTop5(2, None, 0)
        MaxServer3rd = MostReactedTop5(3, None, 0)
        MaxServer4th = MostReactedTop5(4, None, 0)
        MaxServer5th = MostReactedTop5(5, None, 0)
        MaxServer_Ranks = [MaxServer1st, MaxServer2nd, MaxServer3rd, MaxServer4th, MaxServer5th]

        await discordSearch(y_iterator, MaxServer_Ranks, 2, ch)
        channel = client.get_channel(message.channel.id) #Returns to channel message was sent in
        await printTop5(MaxServer_Ranks, channel)

client.run(TOKEN)
