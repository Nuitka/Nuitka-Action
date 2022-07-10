# Python-Script-to-Executable

This is a GitHub Action that builds a stand-alone executable from a python script in your project using the amazing [nuitka](https://github.com/Nuitka/Nuitka) python compiler.

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
- uses: jimkring/python-script-to-executable@v0.1.1
  with:
    script-name: hello_world.py
```

## 3) Run the exectuable
```
C:\> hello_world.exe
hello world!
```

# Usage Details

See [action.yml](action.yml) for details on how this action works under the hood.

### Build a python script into an exe

See [jimkring/test-nuitka-action/](https://github.com/jimkring/test-nuitka-action/actions) for an example of this workflow being used.

```yaml
jobs:

  build:
    # Windows is currently the only platform this action supports
    runs-on: windows-latest

    steps:
    
      # Check-out repository
      - uses: actions/checkout@v3

      # Setup Python
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x' # Version range or exact version of a Python version to use, using SemVer's version range syntax
          architecture: 'x64' # optional x64 or x86. Defaults to x64 if not specified

      # Build python script into a stand-alone exe
      - uses: jimkring/python-script-to-executable@v0.1.1
        with:
          script-name: hello_world.py

      # Uploads artifact
      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: exe
          path: build/hello_world.exe
```

# Limitations (and Roadmap)

- No input parameters yet for the many options provided by Nuitka for building the exe.
- No support yet for Mac and Linux [Roadmap].
- Cannot yet override the hard-coded versions of Nuitka and its dependencies which may conflict with the dependencies of your project. Need an option to not upgrade/downgrade these if they are already installed.
- Not many examples that demonstrate this action in use.

### Python and Package Dependencies

This action installs the following python packages (which are specified in the [requirements.txt](requirements.txt) of this action repo).

```
nuitka==0.9.4
    # via -r requirements.in
ordered-set==4.1.0
    # via -r requirements.in
wheel==0.37.1
    # via -r requirements.in
zstandard==0.18.0
    # via -r requirements.in
```

## Additional Documentation

See [Nuitka](https://github.com/Nuitka/Nuitka) for full documentation on Nuitka. It's really a fantastic tool!


# License

The scripts and documentation in this project are released under the [MIT License](LICENSE).

Nuitka is licensed under the [Apache 2.0 License](https://github.com/Nuitka/Nuitka/blob/develop/LICENSE.txt)

Python is licensed under the [Python Software Foundation (PSF) License](https://github.com/python/cpython/blob/main/LICENSE).

## You are Reponsible for Complying with your Project's Dependencies' Licenses 

This tool compiles and/or copies your project's package dependencies (and their dependencies) into the output executable, which will be considered a combined and/or derivative work of those packages.

> **_Important:_** You are responsibile for compliance with the licenses of your project's package dependencies. Please consult with an attorney about your individual/project's compliance needs and strategy.

## How to Comply With Dependency Package Licenses

There are some great license checker tools that you might consider integrating with your project. Generally speaking, they enable you to specify which licenses (or types) are approved or disaproved and alert you whenever your project has a package dependency that is not approved.

Here are a couple license checker tools:

- [python-license-check](https://github.com/dhatim/python-license-check) - can be run as a GitHub pre-commit hook.
- [dependencies-license-compliance-checker](https://github.com/marketplace/actions/dependencies-license-compliance-checker) - a github action that can be run before your executable build.

