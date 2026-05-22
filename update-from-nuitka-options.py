#!/usr/bin/env python3

import os
import subprocess
import sys
import textwrap

from nuitka.containers.OrderedSets import OrderedSet
from nuitka.options.CommandLineOptionsTools import OurOptionParser
from nuitka.utils.FileOperations import changeTextFileContents
from nuitka.utils.Jinja2 import getTemplate

def _resolve_via_git(owner, repo, tag):
    repo_url = f"https://github.com/{owner}/{repo}.git"

    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", repo_url, tag],
            capture_output=True, text=True, timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None, None

    sha = None
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        s, ref = line.split("\t")
        if ref == f"refs/tags/{tag}":
            sha = s
            break

    if not sha:
        return None, None

    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", repo_url],
            capture_output=True, text=True, timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None, None

    version = None
    version_prefix = f"{tag}."
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        s, ref = line.split("\t")
        ref_name = ref.rsplit("/", 1)[-1]
        if s == sha and ref_name.startswith(version_prefix) and "^{}" not in ref_name:
            if version is None or len(ref_name) < len(version):
                version = ref_name

    return sha, version


def resolve_action_ref(action_ref):
    parts = action_ref.rsplit("@", 1)
    if len(parts) != 2:
        return action_ref

    owner_repo, tag = parts
    owner, repo = owner_repo.split("/", 1)

    sha, version = _resolve_via_git(owner, repo, tag)

    if sha and version:
        return f"{owner_repo}@{sha} # {version}"

    return action_ref


template = getTemplate(
    package_name=None,
    template_subdir=os.path.dirname(__file__) or ".",
    template_name="action.yml.j2",
    extensions=("jinja2.ext.do",),
)


parser = None


def _getParser():
    global parser

    if parser is None:
        sys.argv.append("--help-all")
        from nuitka.options.OptionParsing import parser
        from nuitka.plugins.Plugins import addStandardPluginCommandLineOptions

        addStandardPluginCommandLineOptions(parser=parser, plugin_help_mode=True)
        del sys.argv[-1]

    return parser


def getOptions():
    for option in _getParser().iterateOptions():
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

        from nuitka.options.OptionParsing import SUPPRESS_HELP

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
    help_str = option.help
    if help_str.startswith("[REQUIRED]"):
        help_str = help_str[11:]

    assert not help_str[-1].isspace(), option

    result = (
        option._long_opts[0].lstrip("-")
        + ":\n  description: |\n"
        + textwrap.indent(help_str, prefix="    ")
    )

    if option.github_action_default is not None:
        if type(option.github_action_default) is bool:
            option.github_action_default = (
                "true" if option.github_action_default else "false"
            )

        assert type(option.github_action_default) is str, option
        result += "\n  default: " + option.github_action_default

    return result


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


def get_plugin_options():
    plugin_groups = OrderedSet()

    for option in getOptions():
        container = getattr(option, "container", None)
        if isinstance(container, OurOptionParser):
            continue

        # TODO: No support for Nuitka VM yet.
        if "pelock" in container.title or "themida" in container.title:
            continue

        if container.title.startswith("Plugin options of "):
            plugin_groups.add(container)

    result = []

    for option_group in plugin_groups:
        result.append("### %s ###" % option_group.title)

        for option in option_group.option_list:
            if not option.github_action:
                continue

            result.append(formatOption(option))

        result.append("")

    return textwrap.indent("\n".join(result), "  ")


action_yaml = template.render(
    get_top_options=get_top_options,
    get_group_options=get_group_options,
    get_plugin_options=get_plugin_options,
    resolve_action_ref=resolve_action_ref,
)

if changeTextFileContents("action.yml", action_yaml):
    print("Updated.")
else:
    print("Already up to date.")
