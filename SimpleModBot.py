import json
from discord.ext import commands
try:
    import discord
except ImportError:
    import pip
    pip.main(['install', 'discord'])
    import discord

try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    with open('config.json', 'w') as f:
        config = {}
        print("config file created.")
        json.dump({'discord_token': '', 'response': '', 'words': ['']}, f)


desc = """
Simple moderation bot.
"""
bot = commands.Bot(command_prefix='prefix here', description=desc)

@bot.event
async def on_message(message: discord.Message):
    channel = message.channel
    if message.author.bot:
        return
    if any([word in message.content for word in config['words']]):
        await channel.send('{}: {}'.format(message.author.mention, config['response']))


@bot.event
async def on_ready():
    app_info = await bot.application_info()
    bot.owner = app_info.owner
    print('Bot: {0.name}:{0.id}'.format(bot.user))
    print('Owner: {0.name}:{0.id}'.format(bot.owner))
    print('------------------')
    perms = discord.Permissions.none()
    perms.administrator = True
    url = discord.utils.oauth_url(app_info.id, perms)
    print('To invite me to a server, use this link\n{}'.format(url))

    # Setting `Playing ` status
    # await bot.change_presence(activity=discord.Game(name="a game"), status=discord.Status.online)

    # Setting `Streaming ` status
    # await bot.change_presence(activity=discord.Streaming(name="a stream", url="https://www.twitch.tv/dankmemerdiscord"))

    # Setting `Listening ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"), status=discord.Status.online)

    # Setting `Watching ` status
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"), status=discord.Status.online)

if __name__ == '__main__':
    try:
        bot.run(config['discord_token'])
    except KeyError:
        print("config not yet filled out.")
    except discord.errors.LoginFailure as e:
        print("Invalid discord token.")
