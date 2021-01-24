import light_uniquebots as lub
import discord

client = discord.Client()
ubot_token = "uniquebots_token"
lub_client = lub.LUBClient(bot=client, token=ubot_token)

client.run("discord_token")