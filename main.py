from discord.ext import commands, pages
from colorama import Fore
from time import ctime
import discord
import asyncio
import json

bot = discord.Bot(intents=discord.Intents.all())

# just a variable for formatting
t = f"{Fore.LIGHTYELLOW_EX}{ctime()}{Fore.RESET}"

# --------------------LOAD THE CONFIG--------------------

with open('config.json', 'r') as file:
    config = json.load(file)

# Accessing individual values from the config
bot_token = config["BOT_TOKEN"]
bot_invite = config["BOT_INVITE"]

# --------------------------------------------------------

@bot.event
async def on_ready():
    print(f"{t}{Fore.LIGHTBLUE_EX} | Ready and online - {bot.user.display_name}\n{Fore.RESET}")

    try:
        guild_count = 0
        for guild in bot.guilds:
            print(f"{Fore.RED}- {guild.id} (name: {guild.name})\n{Fore.RESET}")
            guild_count += 1
        print(f"{t}{Fore.LIGHTBLUE_EX} | {bot.user.display_name} is in {guild_count} guilds.\n{Fore.RESET}")

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help"))

    except Exception as e:
        print(e)


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
    await paginator.respond(ctx.interaction, ephemeral=False)


@bot.slash_command(name="ping", description="Displays bot's latency")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Pong!",
        description="Pong! {0}".format(round(bot.latency, 1)),
        color=discord.Color.green()
    )

    await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command(name="invite")
@commands.cooldown(1, 3, commands.BucketType.user)
async def invite(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Add me!!",
        description=f"[Add me]({bot_invite}) to your server!",
        color=discord.Color.green()
    )

    await ctx.respond(embed=embed, ephemeral=True)


async def ticket_button_callback(ctx):
    await ctx.respond(f"Thanks for clicking me!", ephemeral=True)


@bot.slash_command(name="button", description="Create an example button")
@commands.cooldown(1, 3, commands.BucketType.user)
async def button_command(ctx: discord.ApplicationContext):  # Corrected parameter name
    try:
        view = discord.ui.View()
        button = discord.ui.Button(label="Create Ticket", style=discord.ButtonStyle.green)

        button.callback = ticket_button_callback(ctx)
        view.add_item(button)

        # Create an embed
        embed = discord.Embed(
            title="Example Button",
            description="Here is an interactive button!",
            color=discord.Color.green()
        )

        # Send a message with the button and attach the view
        await ctx.respond(embed=embed, view=view)
    except Exception as e:
        print(e)

bot.run(bot_token)