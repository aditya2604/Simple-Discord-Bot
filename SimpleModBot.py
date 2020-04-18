import json
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
client = discord.Client(description=desc)


@client.event
async def on_message(message: discord.Message):
    channel = message.channel
    if message.author.bot:
        return
    if any([word in message.content for word in config['words']]):
        await channel.send('{}: {}'.format(message.author.mention, config['response']))


@client.event
async def on_ready():
    app_info = await client.application_info()
    client.owner = app_info.owner
    print('Bot: {0.name}:{0.id}'.format(client.user))
    print('Owner: {0.name}:{0.id}'.format(client.owner))
    print('------------------')
    perms = discord.Permissions.none()
    perms.administrator = True
    url = discord.utils.oauth_url(app_info.id, perms)
    print('To invite me to a server, use this link\n{}'.format(url))

    # uncomment to set a playing status for the bot:
    #activity = discord.Game(name="game")
    # await client.change_presence(status=discord.Status.idle, activity=activity)

if __name__ == '__main__':
    try:
        client.run(config['discord_token'])
    except KeyError:
        print("config not yet filled out.")
    except discord.errors.LoginFailure as e:
        print("Invalid discord token.")
