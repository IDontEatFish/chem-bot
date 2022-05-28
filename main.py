import yaml
import discord
from discord.ext import commands
import time
import random
import json
import os


intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix='?', intents=intents)

def read_json_file(path):
    with open(path) as file:
        info_file = json.load(file) 
    return info_file 


def read_yaml_file():
    yaml_path = os.path.abspath(r'data\table.yaml')
    with open(yaml_path, encoding='utf-8') as file:
        documents = yaml.full_load(file)
    return documents

def create_embed(ctx, message, more):
    message = message.capitalize()
    author = ctx.author.id
    more[author] = message
    complex_embed = discord.Embed(title=message, color=client.color)
    for x in short_tab:
        complex_embed.add_field(name=f'{x}:', value=document[message][x], inline=False)
    complex_embed.set_footer(text=f'To view more in-depth information or more specific information type ?more.')
    return complex_embed

def randint_element():
    random_element = random.choices(list_of_elements)
    random_element = ''.join(random_element)
    return random_element

tab_path = os.path.abspath(r'data\tab.json')
tabs = read_json_file(tab_path)

short_tab = []
long_tab = []

for x in tabs['short_tab']:
    curr = tabs['short_tab'][x]
    short_tab.append(curr)
    long_tab.append(curr)

for i in tabs['long_tab']:
    curr = tabs['long_tab'][i]
    long_tab.append(curr)

        
document = read_yaml_file()
dic = {'?table <element name>': 'View a table of facts by entering an appropriate element.', '?more': 'View more in-depth information or more specific information.', '?random': 'View a table of facts of a random element.', '?game': 'Commence of the game. The purpose of this game is to guess what element corresponds with the symbol given.', '?guess': 'Guess what element corresponds with the given symbol. This command is part of the ?game command. To use this command you need to first start a game. Use the ?game command to start a game.', '?summary <element name>': 'View a brief summary by entering an appropriate element.', '?info': 'View information about the bot.', '?commands': 'View a list of the available commands.'}
command_promo = 'If you are unsure what commands to use, try ?commands'
more = {}

list_of_elements_path = os.path.abspath(r'data\elements.json')
list_of_elements = read_json_file(list_of_elements_path)


client.color = 0x00ff00


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')       

# command to view peridoic table
@client.command(name='table')
async def table(ctx, message):
    complex_embed = create_embed(ctx, message, more)  
    await ctx.message.channel.send(embed=complex_embed)

@client.command(name='more')
async def moreInfo(ctx):
    id = ctx.author.id
    if id in more:
        if more[id] not in document:
            del more[id]
        moreEmbed = discord.Embed(title=more[id], color=client.color) 
        for x in long_tab:
            moreEmbed.add_field(name=f'{x}:', value=document[more[id]][x], inline=False)
        del more[id]
        await ctx.message.channel.send(embed=moreEmbed)
    elif id not in more:
        await ctx.message.channel.send(f'Make sure you have already entered an element using the ?table <element name> command or the ?random command.')

@client.command(name='summary')
async def summary(ctx, message):
    message = message.capitalize()
    summary_embed = discord.Embed(title=message, color=client.color)
    summary_embed.add_field(name=f'Summary:', value=document[message]['Summary'])
    await ctx.message.channel.send(embed=summary_embed)

@client.command(name='random')
async def random_command(ctx):
    client.random_element = randint_element()
    random_embed = create_embed(ctx, client.random_element, more)
    await ctx.channel.send(embed=random_embed)

client.gamers = [] 
@client.command(name='game')
async def game(ctx):
    client.random_element = randint_element()
    client.lives = 3
    client.gamers.append(ctx.author.id)
    game_embed = discord.Embed(title='Symbol Gusser: ', color=client.color)
    game_embed.add_field(name='Symbol:', value=document[client.random_element]['Symbol'])
    game_embed.set_footer(text='Guess what the what element correspondes with the symbol. Do ?guess <guess>.')
    await ctx.channel.send(embed=game_embed)
    
@client.command(name='guess')
async def guess(ctx, message):
    guess_dic = {}
    message = message.capitalize()
    author = ctx.author.id
    if author in client.gamers: 
        guess_dic[author] = message
        if guess_dic[author] == client.random_element:
            await ctx.message.add_reaction('✅')    
            await ctx.channel.send(f'Well done you have guessed the correct element. You had {client.lives} lives remaining.')
            client.gamers.remove(author)
            del guess_dic[author]
        elif guess_dic[author] != client.random_element:
            client.lives -= 1
            await ctx.message.add_reaction('❌')
            if client.lives == 0:
                await ctx.channel.send(f'GAME OVER. You ran out of lives. The answer was {client.random_element}')
                client.gamers.remove(author)
                del guess_dic[author]
            else:
                await ctx.channel.send(f'Oops. Your guess was incorrect. Try again. You have {client.lives} lives remaining.') 
    elif author not in client.gamers:
        await ctx.channel.send('Before taking a guess, be sure to commence the game by using the ?game command.')


# command for custom server
@client.event
async def on_member_join(member):
    time.sleep(1)
    guild = client.get_guild(934992751202795580)
    channel = guild.get_channel(934992751202795583)
    helpEmbed = discord.Embed(title='Availible Commands: ', color=client.color)
    for x in dic:
        helpEmbed.add_field(name=x, value=dic[x], inline=False)
    helpEmbed.set_footer(text='Anytime you are unsure what command are avaible, please refer to the ?commands command.')
    await channel.send(f'Welcome {member.mention} here is all the commands I have to offer:')
    await channel.send(embed=helpEmbed)
 

@client.command(name='commands')
async def comander(ctx):
    comEmbed = discord.Embed(title='Commands:', color=client.color)
    for x in dic:
         comEmbed.add_field(name=x, value=dic[x], inline=False)
    await ctx.channel.send(embed=comEmbed)

@client.command(name='info')
async def version(ctx):
    myEmbed = discord.Embed(title='General Information:', color=client.color)
    myEmbed.add_field(name='Version Code:', value='Python 3.9.7', inline=False)
    myEmbed.add_field(name='Date Beta:', value='24/01/2022', inline=False)
    myEmbed.add_field(name='Author: ', value='IDontEatFish#6102')
    await ctx.message.channel.send(embed=myEmbed)

# error handeling
@table.error
@summary.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(f'Invalid Arguments. {command_promo}')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Double check your spelling, make sure it is an element on the periodic table. {command_promo}.')

@moreInfo.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Make sure you have already entered an element using the ?table <element name> command. {command_promo}.')

@guess.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Make sure you enter a guess. ?guess <guess>. {command_promo}.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Invalid command. {command_promo}.')

# extras
@client.command(name='purge')
async def clear(ctx, amount : int):
    if ctx.author == ctx.guild.owner:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send('Only the owner of the guild is allowed to use this command.')
    
config_path = os.path.abspath('config.json')
token = read_json_file(config_path) 
client.run(token['token'])