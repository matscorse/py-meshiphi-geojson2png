#!/usr/bin/env python

# Version: 2024-11-11: First version
#
# Author: matsco@bas.ac.uk
#
# Generate PNG summary image from Meshiphi GEOJSON output

import argparse
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


_XSCALE = 40
_YSCALE = 30
_DPI = 180



def hex_to_rgba(hex_color_string):
    """
    Convert the hexadecimal colour string to RGB and Alpha.
    """
    hex_color_string=hex_color_string.lstrip('#')
    rgba = [int(hex_color_string[i:i+2], 16)/255 for i in (0, 2, 4, 6)]
    return tuple(np.array(rgba))



def check_input_filenames(input_filenames: list):
    """
    from the cli arguments create a list of which files
    actually exist.
    """
    list_of_filenames_that_actually_exist = []

    for a_filename in input_filenames:
        if not os.path.isfile(a_filename):
            print("Filename", a_filename, "is not a file (or doesn't exist): Ignoring")
        else:
            list_of_filenames_that_actually_exist.append(os.path.abspath(a_filename))
            print("Including filename:", a_filename)

    return list_of_filenames_that_actually_exist

def create_amsr2_colormap():
    """
    Generate and return the specific AMSR2 colourmap.
    """
    sic_colours = np.ones((100,4))

    sic_colours[00:10]=hex_to_rgba('#00008b00')
    sic_colours[10:20]=hex_to_rgba('#1e90ffff')
    sic_colours[20:30]=hex_to_rgba('#1efaa0ff')
    sic_colours[30:40]=hex_to_rgba('#228b22ff')
    sic_colours[40:50]=hex_to_rgba('#00fa00ff')
    sic_colours[50:60]=hex_to_rgba('#7dfa00ff')
    sic_colours[60:70]=hex_to_rgba('#adff2fff')
    sic_colours[70:80]=hex_to_rgba('#fafa00ff')
    sic_colours[80:85]=hex_to_rgba('#fa7d00ff')
    sic_colours[85:90]=hex_to_rgba('#fa0000ff')
    sic_colours[90:95]=hex_to_rgba('#ba55d3ff')
    sic_colours[95:99]=hex_to_rgba('#9400d3ff')
    sic_colours[99:  ]=hex_to_rgba('#78005aff')

    sic_cmap = ListedColormap(sic_colours)
    sic_cmap.set_bad(color='black')
    return sic_cmap


def convert_to_png(geojson_filepath: os.path, xscale, yscale, dpi, amsr_palette, criteria):

    df = gpd.read_file(geojson_filepath)
    bounds = df.geometry.total_bounds
    fig, ax = plt.subplots(figsize = (xscale, yscale))
    default_cmap = 'coolwarm'

    if str(criteria) == 'fuel':
        df.to_crs(epsg=4326).plot(column='inaccessible', ax=ax, cmap = 'RdYlBu')
        default_cmap = 'Wistia'

    if amsr_palette:
        df.to_crs(epsg=4326).plot(column=str(criteria), ax=ax, edgecolor='grey', linewidth=0.5, cmap = create_amsr2_colormap())
    else:
        df.to_crs(epsg=4326).plot(column=str(criteria), ax=ax, edgecolor='grey', linewidth=0.5, cmap = default_cmap)
    
    df.to_crs(epsg=4326).plot(column='land', ax=ax, edgecolor='brown', linewidth=0.5, cmap = 'copper')

    plt.savefig(geojson_filepath+'.png', dpi=dpi)

    return


def main():
    """
    script entry point
    """
    
    parser = argparse.ArgumentParser(description='Generate PNG summary image(s) from Meshiphi GEOJSON input file(s)')
    parser.add_argument("-x", "--xscale", help="WidthScale in inches, default="+str(_XSCALE), action="store", dest='xscale', default=_XSCALE)
    parser.add_argument("-y", "--yscale", help="HeightScale in inches, default="+str(_YSCALE), action="store", dest='yscale', default=_YSCALE)
    parser.add_argument("-d", "--dpi", help="Output resolution DPI, default="+str(_DPI), action="store", dest='dpi', default=_DPI)
    parser.add_argument("-p", "--palette_amsr", help="Use the AMSR2 colormap palette instead of the default", action="store_true", dest='palette', default=False)
    parser.add_argument("-c", "--criteria", help="Use alternate colourmap criteria, instead of default SIC", action="store", dest='criteria', default='SIC')
    parser.add_argument("files", help="One or more Meshiphi GEOJSON mesh file path(s)", type=str, nargs='+')
    args = parser.parse_args()


    # Now kick off main

    checked_files = check_input_filenames(args.files)

    for geojson_filepath in checked_files:
        convert_to_png(geojson_filepath, args.xscale, args.yscale, args.dpi, args.palette, args.criteria)



if __name__ == "__main__":
    main()