# Python-to-Executable-Or-Module

This GitHub Action builds Windows, Mac, and Linux programs and extension modules from Python using
the amazingly compatible [nuitka](https://github.com/Nuitka/Nuitka) Python compiler.

## Key Features

- **Build Standalone Executables** - Build an executable from your **Python** code (standalone
  `*.exe` or `*.bin` file executables and even `.app` bundles for Mac)
- **Build Binary Python Modules** - Build binary `*.pyd` modules that are importable by other
  **Python** scripts
- **Mac, Linux, and Windows** - Support for Windows, Mac (including .app bundles), and Linux
- **GUI Support** - Supports GUIs made, for example, with **TkInter**\*\* and Qt
  [PySide6](https://pypi.org/project/PySide6/)), and ([PyQt6](https://pypi.org/project/PyQt6/)
- **Lots More!** - All the features of \[Nuitka [Python Compiler](https://nuitka.net), including
  support for [Nuitka Commercial Features](https://nuitka.net/doc/commercial.html) like obfuscation,
  embedding data files, and more (for those with a license).

# Simple to Use

See [Usage Details](#usage-details) below for more info.

## 1) Create a **Python** script

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

Use this action as a step in one of your project's CI workflow jobs
([details below](#usage-details)):

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

- Not enough examples yet that demonstrate how to use this action in practice. Please help proving
  them.

# Common traps

- Uploading artifacts should make sure `include-hidden-files` is present or else incomplete folders
  will be copied in case of `.libs` folders.

- For ``mode`` the value ``app`` is the default and needs to be switched. For
  packages you need to use ``module``.

# Some Example Projects

- TODO: We need to add a repository demonstrating how to use the different
  modes and typical applications. Help is welcome

# Usage Details

See [action.yml](action.yml) for details on how this action works under the hood. It is actually
extremely simple.

## Build a python script into an exe

```yaml
jobs:

  build:
    runs-on: windows-latest

    steps:

      # Check-out repository
      - uses: actions/checkout@v4

      # Setup Python
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x' # Version range or exact version of a Python version to use, using SemVer's version range syntax
          architecture: 'x64' # optional x64 or x86. Defaults to x64 if not specified

      # Build python script into a single execute or app folder (macOS)
      - uses: Nuitka/Nuitka-Action@main
        with:
          nuitka-version: main
          script-name: hello_world.py
          mode: app

      # Uploads artifact
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: exe
          path: build/hello_world.exe
          include-hidden-files: true
```

## GUI Builds

Similar to the others, but with `enable-plugins: pyside6` or `enable-plugins:tk-inter` to ensure
that those libraries are included correctly.

```yaml
- name: Qt GUI with PySide6
  uses: Nuitka/Nuitka-Action@main
  with:
    nuitka-version: main
    script-name: my_qt_gui_app.py
    mode: standalone
    enable-plugins: pyside6
```

```yaml
- name: Python GUI With TkInter
  uses: Nuitka/Nuitka-Action@main
  with:
    nuitka-version: main
    script-name: my_tkinter_gui_app.py
    mode: standalone
    enable-plugins: tk-inter
```

## Multi-Platform Builds

Configure a runner of the appropriate operating system to build for a given platform. You can even
do multiple platforms in a single workflow using a matrix strategy, as shown below:

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
          mode: app

      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ${{ runner.os }} Build
          path: |
            build/*.exe
            build/*.bin
            build/*.app/**/*
          include-hidden-files: true
```

You will see that it creates executable binaries for Mac, Linux, and Windows.

## Python and Package Dependencies

This action installs the following **Python** packages specified by the
[requirements.txt](requirements.txt) of this action repo.

```
ordered-set==4.1.0
    # via -r requirements.in
wheel==0.38.4
    # via -r requirements.in
zstandard==0.20.0
```

## Value syntax

Since Action workflows accept no list values, for options that in **Nuitka** can be given multiple
times, there is support for splitting those arguments by newline, which allows you to specify
multiple values like this.

```yaml
include-data-dir: |
  source_path_dir1=dest_path_dir1
  source_path_dir2=dest_path_dir2
  source_path_dir3=dest_path_dir3
```

# Additional Documentation

See [Nuitka](https://github.com/Nuitka/Nuitka) for full documentation on Nuitka. It's a really
fantastic tool!

# License

**Nuitka Action** scripts and documentation in this project are under the [MIT License](LICENSE).

**Nuitka** has the [Apache 2.0 License](https://github.com/Nuitka/Nuitka/blob/develop/LICENSE.txt)

**Python** has the
[Python Software Foundation (PSF) License](https://github.com/python/cpython/blob/main/LICENSE).

## You are Responsible for Complying with your Project's Dependencies' Licenses

This tool compiles and copies your project's package dependencies (and their dependencies) into the
output executable, which will be considered a combined or derivative work of those packages.

> **_Important:_** You are responsible for compliance with the licenses of your project's package
> dependencies. Please consult with an attorney about your individual/project's compliance needs and
> strategy.

## How to Comply With Dependency Package Licenses

There are some license checker tools that you might consider integrating with your project.
Generally speaking, they enable you to specify which licenses (or types) are approved or disapproved
and alert you whenever your project has a package dependency that is not approved.

Here is a list of license checker tools:

- [python-license-check](https://github.com/dhatim/python-license-check) - can be run as a GitHub
  pre-commit hook.
- [dependencies-license-compliance-checker](https://github.com/marketplace/actions/dependencies-license-compliance-checker)
  \- a github action that you can run before your executable build.
