import os
import textwrap

from nuitka.OptionParsing import SUPPRESS_HELP, parser
from nuitka.utils.CommandLineOptions import OurOptionParser
from nuitka.utils.FileOperations import changeTextFileContents
from nuitka.utils.Jinja2 import getTemplate

template = getTemplate(
    package_name=None,
    template_subdir=os.path.dirname(__file__) or ".",
    template_name="action.yml.j2",
    extensions=("jinja2.ext.do",),
)


def getOptions():
    for option in parser.iterateOptions():
        # Help option
        if "--help" in option._long_opts:
            continue

        # Main option is currently not done like this
        if "--main" in option._long_opts:
            continue

        if not hasattr(option, "require_compiling"):
            continue

        # Non-compiling options do not belong into Nuitka-Action
        if not option.require_compiling or not option.github_action:
            continue

        if option.help is SUPPRESS_HELP:
            continue

        yield option


def getTopOptions():
    for option in getOptions():
        container = getattr(option, "container", None)

        if isinstance(container, OurOptionParser):
            yield option

def getGroupOptions(group_name):
    for option in getOptions():
        container = getattr(option, "container", None)

        if isinstance(container, OurOptionParser):
            continue

        if container.title == group_name:
            yield option

def formatOption(option):
    return (
        option._long_opts[0].lstrip("-")
        + ":\n  description: |\n"
        + textwrap.indent(option.help, prefix="    ")
    )


def get_top_options():
    result = []

    for option in getTopOptions():
        result.append(formatOption(option))

    return textwrap.indent("\n".join(result), "  ")

def get_group_options(group_caption):
    result = []

    for option in getGroupOptions(group_caption):
        result.append(formatOption(option))

    return textwrap.indent("\n".join(result), "  ")

action_yaml = template.render(get_top_options=get_top_options, get_group_options=get_group_options,)

if changeTextFileContents("action.yml", action_yaml):
    print("Updated.")
else:
    print("Already up to date.")
