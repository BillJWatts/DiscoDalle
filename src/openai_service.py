import base64
import io
import logging
import os

import discord
import openai
from openai import error as openai_errors
from random_word import RandomWords

from dd_errors import InvalidRequestError, NaughtyRequestError, NoTokensError

openai.api_key = os.getenv("OPENAI_API_TOKEN")
RW = RandomWords()


def generate_image(prompt: str, artist: str) -> discord.File:
    """Generate an image from a given prompt using OpenAI image generation API

    Args:
        prompt (str): input prompt given by the user
        artist (str): Discord display name of the artist

    Returns:
        discord.File: generated image as an discord.File
    """
    logging.info(f"Sending request to OpenAI DALLE2 with prompt: {prompt}")

    image_b64 = _openai_image_generation_post(prompt)

    logging.info("OpenAI DALLE2 request successful")

    return _b64_to_discord_file_type(image_b64, artist)


def _openai_image_generation_post(prompt: str) -> str:
    """Calls OpenAI image generation API with a prompt

    Args:
        prompt (str): input prompt given by the user

    Raises:
        NaughtyRequestError: If prompt is rejected by OpenAI safety system
        InvalidRequestError: If request is invalid
        NoTokensError: If the OpenAI account has run out of generation tokens

    Returns:
        str: base 64 string of a jpg image
    """
    try:
        response = openai.Image.create(
            prompt=prompt, n=1, size="1024x1024", response_format="b64_json"
        )
        return response["data"][0]["b64_json"]

    except openai_errors.InvalidRequestError as error:
        if "safety system" in error._message:
            raise NaughtyRequestError()
        else:
            raise InvalidRequestError()

    except openai_errors.RateLimitError:
        raise NoTokensError()


def _b64_to_discord_file_type(image_b64: str, artist: str) -> discord.File:
    """Converts a base 64 string to a discord.File and gives it a filename

    Args:
        image_b64 (str): base64 string of a jpg
        artist (str): Discord display name of the artist

    Returns:
        discord.File
    """
    bytes_data = io.BytesIO(base64.b64decode(image_b64))
    return discord.File(fp=bytes_data, filename=_generate_file_name(artist))


def _generate_file_name(artist: str) -> str:
    """Generates a random filename using random words (more fun)

    Args:
        artist (str): Discord display name of the artist

    Returns:
        str: filename
    """
    return f"{artist}_{RW.get_random_word()}_{RW.get_random_word()}.jpg"
