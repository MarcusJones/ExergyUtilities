"""
Requirements
To build the pandas docs there are some extra requirements: you will need to have sphinx and ipython installed. 
numpydoc is used to parse the docstrings that follow the Numpy Docstring Standard (see above), 
but you don't need to install this because a local copy of numpydoc is included in the pandas source code. 
nbsphinx is used to convert Jupyter notebooks. You will need to install it if you intend to modify any of the notebooks 
included in the documentation.

Furthermore, it is recommended to have all optional dependencies installed. This is not needed, but be aware that you will see 
some error messages. Because all the code in the documentation is executed during the doc build, the examples using this optional 
dependencies will generate errors. Run pd.show_versions() to get an overview of the installed version of all dependencies.

Warning

Sphinx version >= 1.2.2 or the older 1.1.3 is required.

"""