# Python-to-Executable-Or-Module

This is a GitHub Action that builds Windows, Mac, and Linux
binaries and modules from Python using the amazingly compatible
[nuitka](https://github.com/Nuitka/Nuitka) Python compiler.

## Key Features

- **Build Stand-along Executables** - Build a executable from your python script
  (stand-alone *.exe or *.bin file executables and even `.app` bundles for Mac)
- **Build Binary Python Modules** - Build binary `*.pyd` modules that can be
  imported into other python scripts
- **Mac, Linux, and Windows** - Support for Windows, Mac (including .app
  bundles), and Linux
- **GUI Support** - Supports GUIs made e.g. with tkinter and Qt ([PyQt6](https://pypi.org/project/PyQt6/), and [PySide6](https://pypi.org/project/PySide6/))
- **Lots More!** - All the features of [Nuitka Python Compiler](https://nuitka.net) including support for [Nuitka Commercial Features](https://nuitka.net/doc/commercial.html) like obfuscation, embedding data files, and more (for those with a license).

# Simple to Use
See [Usage Details](#usage-details) below for more info.
## 1) Create a python script
```python
## hello_world.py
print("hello world!")
```
Run it in python
```
C:\> python hello_world.py
hello world!
```

## 2) Build an executable
Use this action as a step in one of your project's CI workflow jobs ([details below](#usage-details)):
```yaml
# Build python script into a stand-alone exe
- uses: Nuitka/Nuitka-Action@main
  with:
    nuitka-version: main
    script-name: hello_world.py
```

## 3) Run the executable
```
C:\> hello_world.exe
hello world!
```

## Current Limitations

- Not all Nuitka options are currently exposed as input parameters to this
  action. We welcome PRs in case you find anything missing.

- The version of the Nuitka package (and its dependencies) are currently hard-coded. Eventually, we'll add support for you to specify versions of these packages -- probably just by disabling installing these packages as part of the action so you can do it in your workflow.

- Not many examples yet that demonstrate how to use this action in practice.

# Some Example Projects

| Project | Example Workflow (YAML) |
| ---- | ---- |
| [Node Editor GUI using Qt/Pyside6](https://github.com/jimkring/logic-node-editor) | [![Executable Build](https://github.com/jimkring/logic-node-editor/actions/workflows/main.yml/badge.svg)](https://github.com/jimkring/logic-node-editor/actions/workflows/main.yml) |
| [Kasa TP-Link CLI App](https://github.com/jimkring/kasa-cli) | [![Build-All-Platforms](https://github.com/jimkring/kasa-cli/actions/workflows/windows-exe.yml/badge.svg)](https://github.com/jimkring/kasa-cli/actions/workflows/windows-exe.yml) |

# Usage Details

See [action.yml](action.yml) for details on how this action works under the
hood. It is actually pretty simple.

## Build a python script into an exe

See [jimkring/test-nuitka-action/](https://github.com/jimkring/test-nuitka-action/actions) for examples of this workflow in action.

```yaml
jobs:

  build:
    # Windows is currently the only platform this action supports
    runs-on: windows-latest

    steps:

      # Check-out repository
      - uses: actions/checkout@v4

      # Setup Python
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x' # Version range or exact version of a Python version to use, using SemVer's version range syntax
          architecture: 'x64' # optional x64 or x86. Defaults to x64 if not specified

      # Build python script into a stand-alone exe
      - uses: Nuitka/Nuitka-Action@main
        with:
          nuitka-version: main
          script-name: hello_world.py
          onefile: true

      # Uploads artifact
      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: exe
          path: build/hello_world.exe
```

## GUI Builds

Similar to the others, but with `enable-plugins: pyside6` or `enable-plugins:tk-inter` to
ensure that those libraries are included correctly.

```yaml
- name: Qt GUI with PySide6
  uses: Nuitka/Nuitka-Action@main
  with:
    nuitka-version: main
    script-name: my_qt_gui_app.py
    standalone: true
    enable-plugins: pyside6
```

```yaml
- name: Python GUI With TkInter
  uses: Nuitka/Nuitka-Action@main
  with:
    nuitka-version: main
    script-name: my_tkinter_gui_app.py
    standalone: true
    enable-plugins: tk-inter
```

## Multi-Platform Builds

To build for a given platform, just choose a runner of the appropriate operating system.  You can even build for multiple platforms in a single workflow using a matrix strategy, as shown below:

Here we see a workflow from the [jimkring/kasa-cli](https://github.com/jimkring/kasa-cli) project.

```yaml
jobs:
  build:
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest, windows-latest]

    runs-on: ${{ matrix.os }}

    steps:
      - name: Check-out repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10' # Version range or exact version of a Python version to use, using SemVer's version range syntax
          architecture: 'x64' # optional x64 or x86. Defaults to x64 if not specified
          cache: 'pip'
          cache-dependency-path: |
            **/requirements*.txt

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt -r requirements-dev.txt

      - name: Build Executable
        uses: Nuitka/Nuitka-Action@main
        with:
          nuitka-version: main
          script-name: kasa_cli
          onefile: true

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ${{ runner.os }} Build
          path: |
            build/*.exe
            build/*.bin
            build/*.app/**/*
```

And here's what a resulting job run looks like:

https://github.com/jimkring/kasa-cli/actions/runs/2682890462

![image](https://user-images.githubusercontent.com/381432/179555752-021fd3d6-3f33-4f5f-bc44-0461491813fc.png)

You can see that it creates executable binaries for Mac, Linux, and Windows.

## Python and Package Dependencies

This action installs the following **Python** packages specified by the [requirements.txt](requirements.txt) of this action repo.

```
ordered-set==4.1.0
    # via -r requirements.in
wheel==0.38.4
    # via -r requirements.in
zstandard==0.20.0
```

## Value syntax

Since Action workflows accept no lists, for options that can be given multiple times
we provide support for splitting arguments by newline, which allows you to give multiple
values like this (new with Nuitka 2.0).

```yaml
include-data-dir: |
  source_path_dir1=dest_path_dir1
  source_path_dir2=dest_path_dir2
  source_path_dir3=dest_path_dir3
```

This works for all options that can be given multiple times on the command line.

# Additional Documentation

See [Nuitka](https://github.com/Nuitka/Nuitka) for full documentation on Nuitka. It's really a fantastic tool!


# License

The scripts and documentation in this project are released under the [MIT License](LICENSE).

Nuitka is licensed under the [Apache 2.0 License](https://github.com/Nuitka/Nuitka/blob/develop/LICENSE.txt)

Python is licensed under the [Python Software Foundation (PSF) License](https://github.com/python/cpython/blob/main/LICENSE).

## You are Responsible for Complying with your Project's Dependencies' Licenses

This tool compiles and/or copies your project's package dependencies (and their dependencies) into the output executable, which will be considered a combined and/or derivative work of those packages.

> **_Important:_** You are responsible for compliance with the licenses of your project's package dependencies. Please consult with an attorney about your individual/project's compliance needs and strategy.

## How to Comply With Dependency Package Licenses

There are some great license checker tools that you might consider integrating with your project. Generally speaking, they enable you to specify which licenses (or types) are approved or disapproved and alert you whenever your project has a package dependency that is not approved.

Here are a couple license checker tools:

- [python-license-check](https://github.com/dhatim/python-license-check) - can be run as a GitHub pre-commit hook.
- [dependencies-license-compliance-checker](https://github.com/marketplace/actions/dependencies-license-compliance-checker) - a github action that can be run before your executable build.

