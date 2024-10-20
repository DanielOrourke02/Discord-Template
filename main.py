from discord.ext import commands, pages
from colorama import Fore
from time import ctime
import discord
import json


# For guidance: https://guide.pycord.dev/


# discord.Bot() is for application commands
# commands.Bot() is for prefix commands
# bridge.Bot() is for both application and prefix commands
bot = discord.Bot(intents=discord.Intents.default())

# Cool variable for styling etc
t = f"{Fore.LIGHTYELLOW_EX}{ctime()}{Fore.RESET}" 

# --------------------LOAD THE CONFIG--------------------

# probably best if you use a .env but I prefer to use json

with open('config.json', 'r') as file:
    config = json.load(file)

# Accessing individual values from the config
bot_token = config["BOT_TOKEN"]

# --------------------------------------------------------

# runs when the bot is deployed/logged in
@bot.event
async def on_ready():
    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}")

    try:
        guild_count = 0
        for guild in bot.guilds: # loops for every guild the bot is in
            print(f"{Fore.RED}- {guild.id} (name: {guild.name})\n{Fore.RESET}") # output guild name
            guild_count += 1 # increment
        
        # output num of guilds bot is in
        print(f"{t}{Fore.LIGHTBLUE_EX} | {bot.user.display_name} is in {guild_count} guilds.\n{Fore.RESET}")

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help")) # presence

    except Exception as e:
        print(e)

# tip: 'ephemeral=True' means the response is ONLY VISIBLE to the author (user who ran the command)

@bot.slash_command(name="help", description="Lists all commands")
@commands.cooldown(1, 3, commands.BucketType.user) # 3 second cooldown 
async def help_command(ctx: discord.ApplicationContext):
    command_info = [(command.name, command.description) for command in bot.commands]
    chunks = [command_info[i:i + 15] for i in range(0, len(command_info), 15)]
    pages_list = [
        discord.Embed(
            title="List of commands:",
            description="\n".join([f"`/{name}` - {description}" for name, description in chunk]),
            color=discord.Color.blurple()
        ) for chunk in chunks
    ]
    paginator = pages.Paginator(pages=pages_list, loop_pages=True, timeout=30)
    await paginator.respond(ctx.interaction, ephemeral=False) # lists all commands dynamically (and uses Paginator to make the embed)


@bot.slash_command(name="ping", description="Displays bot's latency")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Pong!",
        description="Pong! {0}".format(round(bot.latency, 1)),
        color=discord.Color.blurple()
    )

    await ctx.respond(embed=embed, ephemeral=True)


# runs of button click (thats why its a 'callback')
async def button_callback(ctx):
    await ctx.respond(f"Thanks for clicking me!", ephemeral=True)


@bot.slash_command(name="button", description="Create an example button")
@commands.cooldown(1, 3, commands.BucketType.user)
async def button_command(ctx: discord.ApplicationContext):
    try:
        view = discord.ui.View()
        button = discord.ui.Button(label="Create Ticket", style=discord.ButtonStyle.green) # create button

        button.callback = button_callback(ctx) # when button is clicked run this func
        view.add_item(button) # add button to the view

        # Create an embed
        embed = discord.Embed(
            title="Example Button",
            description="Here is an interactive button!",
            color=discord.Color.blurple()
        )

        # Send a message with the view attached to it (includes the button)
        await ctx.respond(embed=embed, view=view)
    except Exception as e:
        print(e)

bot.run(bot_token)