# Most Reacts Bot
Discord bot to tally up your top 5 reactions (in a channel, specific emoji, or overall).

## About Me
I'm an undergraduate student at the University of Nevada, Reno majoring in Computer Science. Always enjoyed working with computers so it seemed like a natural choice. The first langauge I ever used was Python and then switched to C/C++, learning OOP and good practices, so in a sense I've come full circle. Without that base knowledge I'm sure this code would look (more) like bundles of spaghetti.

More information can be found here at my website www.nalvarez.net and if you have a question about this project, inbox me on reddit (/u/panthercoffee72).

# The Problem and Solution
I had a problem. My Discord server wanted to give out awards for the posts with the most reactions (overall, and of a specific emoji). Nothing I could find online would accomplish this. So I cracked my knuckles and got to reading the API documentation. Through trial and error, I eventually got the result I wanted and learned quite a bit along the way.

Those familiar with writing Discord bots will notice I actually don't use any bot commands at all, it all falls under the client. This is because I had already written the working code using the client commands, and it did what I wanted, so I called it a day. If you take it upon yourself to refactor it using the bot commands instead of client events, please let me know. If I wanted to expand the functionality to do other things, that would greatly simplify things (namely, taking in arguments with the commands instead of hardcoding the string to check for).

## Notes
You **WILL** need to modify this code for it to work on your server. Namely, the token (obviously), the list of channel IDs, the list of channel names respective to the order of IDs, and the commands you want. I made it pretty straightforward in the prefilled stuff so you should be able to figure it out.

!most_reacts_here and !most_reacts_all will work out of the box. Custom emoji searches will need to be programmed by you since I don't know what the names of them are.

The Discord API is your best friend, and I spent many hours mulling over it. https://discordpy.readthedocs.io/en/latest/api.html#

This tutorial is also useful if you have no idea where to start: https://realpython.com/how-to-make-a-discord-bot-python/

## Known Issues
Channel names and IDs are hardcoded. This can be circumvented but then I'd have to mess with the progress message, and maybe there's channels you don't want to check when searching the whole server.

Make sure the bot has read, send, and history permissions in each channel in the list.

# Overview of Project Components
## Classes
### MostReactedTop5
**Functions**

----Constructor----

What it does: Creates a MostReactedTop5 object with specified arguments. As seen in the commands, five objects are made in the form of Emoji1st ... Emoji5th.

*Arguments: ranking (int), emoji_name (str), specific (bool)*

Ranking (applied to `post_ranking`) is the respective place of the post (1st through 5th). Takes values (1, 5).

Emoji Name (applied to `emoji_name`) is the string representation of the emoji. For custom emojis, that is the name between colons (ex. :custom_emoji: is entered as custom_emoji). Unicode emojis need to be copy and pasted from an online emoji website and sent as a string. If there is no specific emoji, it is passed in as None.

Specific (applied to `has_specific_emoji`) is a flag set, where 0 means the class can hold any emoji and 1 means it will hold only one.

----printResults()----

What it does: Sends a message to the return channel (the channel the command was sent in) detailing the results of the search. It lists who sent it, what date, in what channel, the content of the message, and the total number of whatever kind of reaction it received. It will also post the first attachment (like a photo) if the post contained one.

*Arguments: rtn_channel (discord.Channel)*

Return channel is passed in from the printTop5() function and this is where the results will be posted. We also retrieve the file (if any) from the internet here.

## Functions
Listed in order of being called.

### on_message
What it does: This is Discord's event handler for when a message is sent. Within it, you can code the commands to be checked.

For the commands, we check for the name of the command in the message content. If that's found we set `y_iterator` to the appropriate number (-1 for whole server searches, or the index of a specific channel from `Channel_IDs`). Our channel is set to the channel the command was sent in. We then create our five classes and put them in a list.

discordSearch() is called, passing in our iterator, the list of classes, what type of search we're doing, and the channel. Honestly, I don't think this `ch` variable does anything, because I set it to None in all other commands, but I'm too lazy to take it out and risk breaking something.

After the search we set our channel again to the one the command was sent in and print our top 5, sending in our list of classes and the return channel.

### discordSearch
What it does: Initializes variables needed for rest of functions, and begins searching based upon the value of `type_search`.

*Arguments: z (int), class_name (List), type_search (int), r_ch (discord.Channel)*

Z represents our `y_iterator` and is how we keep track of where we're searching, and is used for progress messages.

Class Name is our list of classes. For progress messages, the first element is passed as that is where the amount of posts is tracked.

Type Search has three values (0, 2). 0 is a search of one channel and non-zero is a search of the whole server. 1 represents a search for a specific emoji and 2 is a search for any emoji.

Return channel is not used. Never coded it out.

If we search the entire server, we send a progress message *with a percentage* and then start a loop through Channel_IDs. Each loop calls historySearch() and updates the progress message.

### progessMessage
What it does: Sends or updates a message in Discord detailing the status of the search.

*Arguments: class_name (MostReactedTop5), f (int), search_percent (int), z (int), type_search (int), ch_posts (int)*

Class Name is the first element of our class list, which is where details about posts counted are stored.

F is a flag, determining where we are in the search. 0 is the initial message (called only once), 1 is mid-search, and 2 is a completed search, removing any loading indication.

Search Percent is calculated in discordSearch() and is based upon the length of `Channel_Names` and the value of our iterator `z`.

Z is our iterator.

Type search is discussed in discordSearch(). This determines whether or not to show a loading percentage (not feasible if searching only one channel).

Channel posts is a counter of how many posts in that specific channel have been searched.

The function creates an appropriate title, based on where and what it's searching for, and details the percent completion (if applicable), how many posts it has searched, and where it is currently searching.

### historySearch
What it does: Runs Discord's channel search to provide a discord.Message iterator based upon the loops options. Read the Discord API (see: TextChannel) for information on the parameters you can set. In this case, it checks up to 22,000 posts per channel and if they are after January 1st, 2020.

*Arguments: z (int), class_name (List), search_percent (int), progress_id (discord.Message), channel (discord.Channel), ch_posts (int), type_search (int)*

Z is our iterator.

Class Name is our list of classes, as we need the list for reactionRanker().

Search percent is needed for progressMessage().

Progress ID is the message we need to update. Calls progressMessage().

Channel is the channel we're currently searching, sent in from discordSearch().

Channel posts is our counter for the number of posts searched. Updated with each loop then added to first class object in list at end of function call.

Type search is used for progressMessage().

This function is built around if-else statements. First, we check our iterator (remember, it's of type discord.Message) has a reaction. If so, we're going to loop through all of its reactions if there are multiple. Now, we check if our class has the specific emoji flag set. If so, are we checking for a custom or unicode emoji. Finally, we make sure it matches the class's emoji name and runs reactionRanker(). If we are searching for any emoji, we instead skip the name and type checking and just run reactionRanker().

### reactionRanker
What it does: Compares our reaction count on the message to what is stored in our class objects, and assigns it to an object if necessary.

*Arguments: r (discord.Reaction), class_name (List), m (discord.Message), r_i (discord.Reaction)*

R is for reaction, and it's the current reaction we're looking at.

Class name is our list of classes.

M is for message, and it's the current message we're looking at.

Reaction Iterator, also known as `i`, functions like `r` and is redundant but the code works so I kept it.

Fun fact, I wrote the pseudocode for this by hand and ran it on a table. Actually a very useful strategy.

Anyway, this function checks the number of a certain reaction on a message, and if it's higher than the 1st class object, then the process below takes place.

```
5th class copies 4th class.
4th class copies 3rd class.
3rd class copies 2nd class.
2nd class copies 1st class.
1st class calls reactionDataHandler() to update it's information from the message we're looking at.
```

Now, if the 1st and 2nd class are already higher than the current message, but say the 3rd class count is lower than the number of reactions, then that process above is called, but the 3rd class calls reaction data handler and updates its information.

### reactionDataHandler
What it does: Updates class object information with the message information that was passed in.

*Arguments: r (discord.Reaction), class_name (MostReactedTop5), m (discord.Message), r_i (discord.Reaction)*

Same as above, except the class name is a singular object and not a list now.

All we're doing here is copying over relevant information from the message.

### classFixup
What it does: Fixes post rankings as when we use copy.deepcopy() in reactionRanker(), the rankings also get copied.

*Arguments: c (List)*

C is our list of classes.

This function is deprecated and has been incorporated into printTop5().

### printTop5
What it does: Fixes rankings and calls each class object's printResults() function to send a message to the server.

*Arguments: c (List), channel (discord.Channel)*

C is our list of classes.

Channel is the channel we want to send the message in, which was sent in from the command function body.
