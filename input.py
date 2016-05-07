# Name of the output file; make it a .csv, You will be able to open it in Excel.
outputfile = "20160504-Output.csv"

# The code uses the number of replicates to calculate average and standard deviation
# Number of replicates and number of groups must be consistent with the number of samples the script reads.
# It will throw an error if this is not the case.
# Here I provided groups for a full 96 well plate. You can have less.
replicates = 3
grouping = ["1", "2", "3", "4", "5", "6", "7", "8",
            "9", "10", "11", "12", "13", "14", "15", "16",
            "17", "18", "19", "20", "21", "22", "23", "24",
            "25", "26", "27", "28", "29", "30", "31", "32",]



# FlowCal automatically identifies the region with the highest density of event
# and calculates how big it should be to capture a certain percentage of the total event count;
# set the % here e.g. 0.5 = 50%
percent = 0.5

# Set it to false if you don't want the script to tell you what it's doing.
verbose = True
