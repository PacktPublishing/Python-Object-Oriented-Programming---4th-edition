


# Python-Object-Oriented-Programming---4th-edition
Code Repository for Python Object-Oriented Programming - 4th edition, Published by Packt

The case study relies on a number of external packages. 
It's often best to start with a tool like `conda`
to build virtual environments and download packages. 
This can also be done with other virtual environment managers.

The following steps will help you build a working Python environment. Later, we'll add the additional
packages used by the case study.

1. Get **miniconda**. Find it here: https://docs.conda.io/en/latest/miniconda.html.

2. Install **miniconda**. Find the instructions here: https://conda.io/projects/conda/en/latest/user-guide/install/index.html.
   For the most part, the instructions can be summarized as "double-click the installer."
   There are potential complications, so it can help to read through the the instructions.

3. Use the **conda** tool to create a virtual environment that has Python. We'll add the required packages for this case study.

   ```sh
   % conda create -n CaseStudy python=3.9
   % conda activate CaseStudy
   ```

4. Now that this is available, you can run Python. Try the following:

    ```sh
    % python
    >>> print("Hello, world!")
    Hello, world!
    >>> exit()
   ```
   
## Installing Other Components

Now that you have a working Python environment, we can add some of packages we'll be using.

```sh
    % conda install bs4 pytest pillow
```

This will ask if you want to proceed. The answer is "y", for "yes." It will then download
and install the four packages listed above, plus the packages they depend on.

Not every package can be installed by **conda**, so PIP is sometimes needed. Specifically,
we want to automate our testing with the `tox` tool, which isn't easily installed by **conda**.

```sh
    % python -m pip install tox
```

The file `environment.yml` has the exported environment used to produce this example.

Once PIP has been run, **conda** can lose track of the extra installations. To make
changes, it's often helpful to create a new conda environment with the packages available
from **conda**, and then add PIP packages.

Your versions may be slightly newer than the ones used by the author.

## Multiple Python Version Setup

The full test suite requires multiple versions of Python and the tox utility.

There is some complexity when using Windows.
See https://tox.readthedocs.io/en/latest/developers.html?highlight=windows#multiple-python-versions-on-windows

The easiest way to do this is to create an additional conda environment,

```sh
    conda create --name=tox-py38 python=3.8
```

This environment will have the needed Python run-time.

For Windows, only, edit the `python3.8.bat` file to point to
this environment's executables. Generally, the name supplied will
be correct.

## Running the Test Suite

The test suite requires tox and Python 3.8 (see above for additional installs.)

Use the following command to run all of the tests.

```sh
    % make test
```

To run tests for a specific chapter, you can change the
working director and run `tox`. Here's an exception for
Chapter 2.

```sh
    % (cd ch_02; tox)
```

This will change to the chapter 2 directory, `ch_02`,
and run `tox` in that directory.

For Windows, use `cmd`:

```cmd
    C:\path\to\repo> cmd /c "CHDIR ch_02&&tox"
```


## An Integrated Development Environment

You can edit Python code with any text editor. It can be easier to use
a sophisticated IDE, but some developers are happy with simple text editors.
There's no "best" IDE for Python. While the author uses PyCharm and Komodo Edit, some people
prefer VS Code, or Spyder.

Good UML diagrams can be created with the http://draw.io diagram editor. This creates
`drawio` text files that can saved as part of a project. It can export PNG files for publication.
This is very easy to install and use.

Another  choice is to use plantuml. See https://plantuml.com. This can be incorporated
into a markdown processing plug-in used by the PyCharm IDE.
The plugin depends on **graphviz**, making the installation fairly complex.

- Add the Markdown tool to PyCharm.

- In the preferences for Markdown, install and enable PlantUML.

- Use **conda** to install `graphviz` as well as installing the `plantuml-markdown` tools.
  The `markdown_py` application can create an HTML draft of a Markdown doc. 
  It needs to be installed separately, if this is needed.

- Update the OS environment settings to set the `GRAPHVIZ_DOT` environment variable to name the conda virtual environment.
  where `graphviz` was installed.
  The macOS and Linux users should update their `~/.zshrc` or `~/.bashrc` file, depending on which shell is in use.
  Windows users should set their system environment variables.

- It may be necessary to create a `plantuml` shell script in `/usr/local/bin`. 
  See https://github.com/mikitex70/plantuml-markdown for details on installation.

The `plantuml` can be used to tranform UML files to PNG images.

The Project Structure
=====================

Each chapter's code is in a separate directory, `ch_01`, `ch_02`, etc.

Within the chapter, there's some combination of `docs`, `src`, and `tests` folders.
There will also be a `pyproject.toml` file with parameters used to control tools
like **tox**.

Chapters and Case Study Content
===============================

1.  Object-Oriented Design.
    Creating the 4+1 views of the problem domain.

2.  Objects in Python.
    Core data model of samples and training data.

3.  When Objects Are Alike.
    Algorithm Alternatives for k-NN -- euclidean, manhattan, chebyshev, minkowski

4.  Expecting the Unexpected.
    Central authentication and authorization for a web service.

5.  When to Use Object-Oriented Programming.
    Input validations for training data as well as requests.
    Properties. Context Managers.

6.  Abstract Base Classes (abc’s) and Operator Overloading.
    Filtering and subsetting the training data to create test sets. Shuffling. Sorting. Random Selection. Filters.

7.  Python Data Structures.
    The ``@dataclass`` definitions and ``NamedTuple`` implementation choices.

8.  Functional Techniques.
    The essential k-NN algorithm as a functional design.
    Computing test results for different K values and distance algorithms.

9.  Strings and Serialization.
    JSON serialization and deserialization of training data, requests and responses.

10. The Iterator Pattern.
    Revisiting the k-NN design to permit future flexibility.

11. Common Design Patterns. (No case study.)

12. Advanced Design Patterns. (No case study.)

13. Testing Object-Oriented Programs.
    Using Test-Driven Develoment on a small ciphering algorithm.
    
14. Concurrency.
    Compressing image files using Run-Length Encoding.
### Download a free PDF

 <i>If you have already purchased a print or Kindle version of this book, you can get a DRM-free PDF version at no cost.<br>Simply click on the link to claim your free PDF.</i>
<p align="center"> <a href="https://packt.link/free-ebook/9781801077262">https://packt.link/free-ebook/9781801077262 </a> </p>