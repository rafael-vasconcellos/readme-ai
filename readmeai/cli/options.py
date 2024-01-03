"""Command-line interface options for the readme-ai application."""

from __future__ import annotations

import os
from typing import Optional

import click
from click import Context, Parameter

from readmeai.config.settings import BadgeOptions, ImageOptions


def prompt_for_custom_image(
    context: Optional[Context],
    parameter: Optional[Parameter],
    value: Optional[str],
) -> str:
    """Prompts the user to input a custom image URL.

    Parameters
    ----------
    ctx
        Click context object.
    param
        Click parameter object.
    value
        Value of the parameter.

    Returns
    -------
    str
        Custom image URL.
    """
    if value == ImageOptions.CUSTOM.name:
        return click.prompt("Enter the URL for your custom image logo")
    elif value in ImageOptions.__members__:
        return ImageOptions[value].value
    else:
        raise click.BadParameter(f"Invalid image URL provided: {value}")


align = click.option(
    "-a",
    "--align",
    type=click.Choice(["center", "left"], case_sensitive=False),
    default="center",
    help="Align the text in the README.md file's header to the left or center.",
)
api_key = click.option(
    "-k",
    "--api-key",
    default=os.environ.get("OPENAI_API_KEY", None),
    help="Your GPT language model API key.",
)
badges = click.option(
    "-b",
    "--badges",
    type=click.Choice(
        [opt.value for opt in BadgeOptions], case_sensitive=False
    ),
    default="standard",
    help="""\
        Badge icon style types to select from when generating README.md badges. The following options are currently available:\n
        - flat \n
        - flat-square \n
        - for-the-badge \n
        - plastic \n
        - skills \n
        - skills-light \n
        - social \n
        - standard \n
        """,
)
emojis = click.option(
    "-e",
    "--emojis",
    is_flag=True,
    default=False,
    help="This option adds emojis to the README.md file's header sections. For example, the default header for the 'Overview' section generates the markdown code as '## Overview'. Adding the --emojis flag generates the markdown code as '## 📍 Overview'.",
)
image = click.option(
    "-i",
    "--image",
    type=click.Choice(
        [opt.name for opt in ImageOptions], case_sensitive=False
    ),
    default=ImageOptions.BLUE.name,
    callback=prompt_for_custom_image,
    show_choices=True,
    help="""\
        Project logo image displayed in the README file header. The following options are currently available:\n
        - CUSTOM \n
        - BLACK \n
        - BLUE \n
        - GREY \n
        - PURPLE \n
        - WHITE \n
        - YELLOW \n
        """,
)
model = click.option(
    "-m",
    "--model",
    default="gpt-3.5-turbo",
    help="GPT language model to use for generating various sections of the README.md file.",
)
offline = click.option(
    "--offline",
    is_flag=True,
    default=False,
    help="Use this option to generate a README.md file for free without making any LLM API calls. This option generates the same README file structure, and leaves placeholders for content thats generated by the LLM, which include the project slogan inserted in the header section, along with the 'Overview', 'Features', and 'Modules' sections.",
)
output = click.option(
    "-o",
    "--output",
    default="readme-ai.md",
    help="Define the name of the README.md file to generate.",
)
repository = click.option(
    "-r",
    "--repository",
    required=True,
    help="Required option for defining your repository's remote URL link (GitHub, GitLab, BitBucket), or a local directory path to the source code you'd like to document.",
)
temperature = click.option(
    "-t",
    "--temperature",
    default=0.9,
    type=float,
    help="Temperature LLM API parameter for generating README.md file content. A higher temperature value will generate more creative content, while a lower temperature value will generate more predictable content.",
)
max_tokens = click.option(
    "--max-tokens",
    default=3899,
    type=int,
    help="Max tokens LLM API parameter for generating README.md file content. This option defines the maximum number of tokens to generate for each section of the README.md file.",
)
template = click.option(
    "--template",
    help="Template style to use for generating the README.md file.",
)
language = click.option(
    "-l",
    "--language",
    help="Language to generate README.md file content in. The default language is English (en).",
)
