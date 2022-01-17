# Program to merge multiple .csv files into one
Created to combine measurements stored in multiple files for further analysis.
Optional: Calculate the average (-a/--average) if there are multiple values for one id and return file with only one value per id

## Current state:
- header = True => first line of file will be excluded
- delimiter = ;
- id, value, value

## Usage
python csv_merger.py -d directory/containing/csvs -f outputfilename (-a)
