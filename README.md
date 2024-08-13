# Program to merge multiple .csv files into one
Created to combine measurements stored in multiple files for further analysis.
Optional: Calculate the average (-a/--average) if there are multiple values for one id and return file with only one value per id

## Current state:
- Either all files have a header (default), or non of them (use --no_header). No mixing supported
- European .csv format with values delimited by a ';' and ',' as a decimal separator is supported (default), as well as standard .csv format (delimiter = ',' and decimal separator = '.'). Use option --standard_format for the latter
- The first column has to contain a purely numeric (int) id, followed by an arbitrary number of columns containing int or float values
- Empty data fields will be set to 0

## Usage
python3 csv_merger.py directory/containing/csvs (-f/--filename outputfilename) (-a/--average) (--no_header) (--standard_format)
