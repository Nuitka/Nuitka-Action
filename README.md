# Nuitka-Build-Executable-from-Python-Script

This builds a stand-alone executable from a python script using [nuitka](https://github.com/Nuitka/Nuitka), the python compiler.

# Usage

See [action.yml](action.yml)

### Build a python script into an exe

```yaml
jobs:
  build:
    # Windows is currently the only platform this action supports
    runs-on: windows-latest

    steps:
      # Check-out repository
      - uses: actions/checkout@v3

      # Build python script into a stand-alone exe
      - uses: jimkring/nuitka-build-executable-from-python-script@main
        with:
          script-name: test.py
      
      # Uploads artifact
      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: exe
          path: build/test.exe

```

## Inbound License Compliance is your Responsibility (i.e. dependencies)

> **_Important:_** It is your responsibility to comply with the license terms of the packages and software libraries used by your python script (i.e. the package dependencies of your project), as these will be compiled or (in the case of DLLs) copied into the resulting executable to form a combined and/or derivative work.


# Limitations

- Currently, this action will use the python version that gets run via the `python` command on the runner. So, you should [setup-python](https://github.com/actions/setup-python) on the runner in a step prior to calling this action.

# Roadmap

- Add input parameters for various nuitka build settings and options
- Support for Mac and Linux
- Allow specifying desired python version
- Optional caching nuitka dependencies (that it self downloads when needed)
- Option to not install package dependencies and rely on dependencies being set in the calling workflow
- Create a repo with various examples and tests for this action

### Python and Package Dependencies

This action installs the following python packages (which are specified in the [requirements.txt](requirements.txt) of this action repo)

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
