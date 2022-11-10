"""Module containing all info (radio data retrieval) user commands"""


from discord.ext import commands
from openai.error import OpenAIError
import logging
import messenger
from dd_errors import InvalidRequestError, NaughtyRequestError, NoTokensError
from openai_service import generate_image
from resources import get_confirmation_message


class DalleCommands(commands.Cog):
    """DiscoDalle commands"""

    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def generate(self, context: commands.Context, *args: str):
        """Take in a user prompt, calls OpenAI to generate an image from the prompt

            example: dd.generate a photorealisit drawing of a cat

        Args:
            context (commands.Context): Context of the user command
            args (str): User input prompt for image generation
        """
        prompt = " ".join(args)
        artist = context.author.display_name

        await messenger.send_message(channel=context, message=get_confirmation_message(artist))
        try:
            image = generate_image(prompt=prompt, artist=artist)
            await messenger.send_image(channel=context, image=image)

        except NaughtyRequestError:
            await messenger.send_message(
                channel=context,
                message=f"Actually {artist}... your suggestion is a bit too naughty for me",
            )

        except NoTokensError:
            await messenger.send_message(
                channel=context, message="Sorry all my credits are used up."
            )

        except (InvalidRequestError, OpenAIError) as error:
            logging.error(error._message)
            await messenger.send_message(channel=context, message="Oops, something went wrong.")


async def setup(client):
    await client.add_cog(DalleCommands(client))
