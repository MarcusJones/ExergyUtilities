if 1:
    import importlib

    ##########################################################
    # Imports
    ##########################################################
    if importlib.util.find_spec("numpy"):       import numpy as np
    if importlib.util.find_spec("pandas"):      import pandas as pd
    if importlib.util.find_spec("sklearn"):     import sklearn as sk
    if importlib.util.find_spec("keras"):       import keras as ks
    if importlib.util.find_spec("matplotlib"):  
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
    if importlib.util.find_spec("seaborn"):
        import seaborn as sns
    if importlib.util.find_spec("PIL"):         import PIL as PIL
    if importlib.util.find_spec("pyspark"):     import pyspark as pyspark


    # Add my utilities
    import sys
    util_path = r"/home/batman/git/py_ExergyUtilities"
    sys.path.append(util_path)
    if importlib.util.find_spec("ExergyUtilities"):         import ExergyUtilities as exergy

    ##########################################################
    # Utilities for modules
    ##########################################################
    def print_m(modname,symbol):

        try: this_module = globals()[symbol]
        except: this_module = None

        if not this_module:
            symbol = "NOT LOADED"

        try: this_version = this_module.__version__
        except: this_version = "N/A"

        print("{:<20} {:<15} {}".format(modname, symbol, this_version))

        #try: 
        #except: print("{:<10} NOT LOADED".format(modname))

    def mj():
        print("Ensure IP Kernel is properly set!")
        print_imports()

    def print_imports():
        print("Loaded modules:")
        print_m("numpy","np")
        print_m("pandas","pd")
        print_m("sklearn","sk")
        print_m("keras","ks")
        print()
        print_m("matplotlib","mpl")
        print_m("matplotlib.pyplot","plt")
        print_m("matplotlib.image","mpimg")
        print_m("seaborn","sns")    
        print_m("PIL","PIL")
        print()
        print_m("ExergyUtilities","exergy")
        print()
        print_m("pyspark","pyspark")


    ##########################################################
    # Plotting style
    ##########################################################
    custom_style_template = {
        'axes.axisbelow': True,
        'axes.edgecolor': 'white',
        'axes.facecolor': '#EAEAF2',
        'axes.grid': True,
        'axes.labelcolor': '.15',
        'axes.linewidth': 0,
        'font.family': 'Arial',
        'grid.color': 'white',
        'grid.linestyle': '-',
        'image.cmap': 'Greys',
        'legend.frameon': False,
        'legend.numpoints': 1,
        'legend.scatterpoints': 1,
        'lines.solid_capstyle': 'round',
        'pdf.fonttype': 42,
        'text.color': '.15',
        'xtick.color': '.15',
        'xtick.direction': 'out',
        'xtick.major.size': 0,
        'xtick.minor.size': 0,
        'ytick.color': '.15',
        'ytick.direction': 'out',
        'ytick.major.size': 0,
        'ytick.minor.size': 0}


    custom_style_dark = {'axes.axisbelow': True,
        'axes.edgecolor': 'white',
        'axes.facecolor': '0.3',
        'axes.grid': True,
        'axes.labelcolor': 'white',
        'axes.linewidth': 0,
        #'font.family': 'Arial',
        'grid.color': 'white',
        'grid.linestyle': '-',
        'image.cmap': 'Greys',
        'legend.frameon': False,
        'legend.numpoints': 1,
        'legend.scatterpoints': 1,
        'lines.solid_capstyle': 'round',
        'pdf.fonttype': 42,
        'text.color': 'white',
        'xtick.color': 'white',
        'xtick.direction': 'out',
        'xtick.major.size': 0,
        'xtick.minor.size': 0,
        'ytick.color': 'white',
        'ytick.direction': 'out',
        'ytick.major.size': 0,
        'ytick.minor.size': 0}

    sns.set_style("darkgrid", rc=custom_style_dark)
