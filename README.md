# time-series-basics
Using pandas data frames to manipulate and bin patient data according to the time/date the data was recorded.

## pandas_import:
The pandas_import.py file takes all .csv files in the smallData folder and imports them as pandas dataframes.  From there, the data is combined into a data frame that keeps all the data values that are given at the times listed in the 'cgm_small.csv' file.  Then the data is binned into time intervals of 5 and 15 minutes.  This binned data is printed to the files '5min_binned_data.csv' and '15min_binned_data.csv' respectively.

### Input Files
The pandas_import.py script is dependent specifically on the contents of the smallData folder.

### Output Files
As mentioned above, the two output files are: (1) '5min_binned_data.csv' and (2) '15min_binned_data.csv'

### Example
To run this script, use the command
```
python pandas_import.py
```

## Benchmarking:
### Note to the grader:
I skipped assignment 5 so I cannont compare my benchmarking results to that assignment.  Taisa said not to take points off for this :P
### Benchmarking Result
When I ran gnu time on my program, it showed that the program took *5.28 seconds* to run and used *65580 KB* of memory.  Not too shabby.