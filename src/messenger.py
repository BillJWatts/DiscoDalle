"""Module containing all message sending logic"""
import discord


async def send_message(channel, message: str):
    await channel.send(message)


async def send_image(channel, image: discord.File):
    await channel.send(file=image)
