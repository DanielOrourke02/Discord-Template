from discord.ext import commands
from colorama import Fore
from time import ctime
import discord
import asyncio
import json

prefix = '.'  # ignore this the prefix is slash commands anyway
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), help_command=None)

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
        synced = await bot.tree.sync()  # Loads/syncs commands
        print(f"{t}{Fore.LIGHTBLUE_EX} | {len(synced)} command(s).\n{Fore.RESET}")

        guild_count = 0
        for guild in bot.guilds:
            print(f"{Fore.RED}- {guild.id} (name: {guild.name})\n{Fore.RESET}")
            guild_count += 1
        print(f"{t}{Fore.LIGHTBLUE_EX} | {bot.user.display_name} is in {guild_count} guilds.\n{Fore.RESET}")

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help"))

    except Exception as e:
        print(e)


@bot.tree.command(name="help")
async def help_command(interaction: discord.Interaction):
    # Define the list of commands with descriptions
    commands_list = [
        {"name": "help", "description": "Displays this message"},
        {"name": "ping", "description": "Pings the bot"},
        {"name": "invite", "description": "Add the bot to your server"},
        {"name": "button", "description": "Displays an example button"},
    ]

    # Construct the help message as an embed
    embed = discord.Embed(title="Bot Commands", color=discord.Colour.blue())
    for command in commands_list:
        embed.add_field(name=f"/{command['name']}", value=command['description'], inline=False)

    # Send the help message as an ephemeral response
    await interaction.response.send_message(embed=embed)


# Simple Test command
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Pong!",
        description="Pong! {0}".format(round(bot.latency, 1)),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="invite")
async def invite(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Add me!!",
        description=f"[Add me]({bot_invite}) to your server!",
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)



async def ticket_button_callback(interaction):
    await interaction.response.send_message(f"Thanks for clicking me!", ephemeral=True)


@bot.tree.command(name="button")
async def button_command(interaction: discord.Interaction):  # Corrected parameter name
    try:
        view = discord.ui.View()
        button = discord.ui.Button(label="Create Ticket", style=discord.ButtonStyle.green)

        button.callback = ticket_button_callback
        view.add_item(button)

        # Create an embed
        embed = discord.Embed(
            title="Example Button",
            description="Here is an interactive button!",
            color=discord.Color.green()
        )

        # Send a message with the button and attach the view
        await interaction.response.send_message(embed=embed, view=view)
    except Exception as e:
        print(e)


# Use an asynchronous function to run the setup and the bot
async def run_bot():
    await bot.start(bot_token)


# Run the bot using the asynchronous function
asyncio.run(run_bot())