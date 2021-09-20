import discord
from discord.ext import commands
import os
import minecraft_commands


bot = commands.Bot("!", description="The SPW's new helper bot for Discord.")


@bot.event
async def on_ready():
    print("----------------------------------")
    print(f"Logged in as {bot.user.name}")
    print(bot.user.id)
    print("----------------------------------")


@bot.group(aliases=("mc",))
async def minecraft(ctx):
    """Query and control the Minecraft Server."""
    if ctx.invoked_subcommand == None:
        await ctx.send_help()


@minecraft.command()
async def status(ctx):
    """Get the status and ip address of the Minecraft Server."""
    status = minecraft_commands.get_status()

    await ctx.reply(status.message())


@minecraft.command(aliases=("run",))
async def start(ctx):
    """Start the Minecraft Server."""
    if minecraft_commands.get_running():
        await ctx.reply("Server is already running")
        return

    await ctx.send("Starting server...")
    if minecraft_commands.run_server():
        await ctx.reply("Server now running!")
    else:
        await ctx.reply(
            "Server is taking longer than expected to start. "
            "Please check with `!minecraft status` in a few seconds."
        )


@minecraft.command()
async def stop(ctx):
    """Shut down the Minecraft Server"""
    if not minecraft_commands.get_running():
        await ctx.reply("Server is already shut down")
        return

    await ctx.send("Shutting down server")
    minecraft_commands.stop_server()
    await ctx.send("Server now shut down")


def main():
    bot.run(os.environ["SPEEDWAGON_BOT_KEY"])


if __name__ == "__main__":
    main()
