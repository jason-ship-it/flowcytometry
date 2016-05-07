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








##### Do not edit below this line #######

import FlowCal
import matplotlib.pyplot as plt
import glob
import numpy as np


# Reading files
fcs_read = []
for i in glob.glob("*.fcs") :
    fcs_read.append(FlowCal.io.FCSData(i))
    if verbose: print "Reading", i


# Converting to a.u.
if verbose: print "Converting data to arbitrary units."
data_au = []
for j in fcs_read:
    #converts each sample's fluorescence to a.u./rfi
    data_au.append(FlowCal.transform.to_rfi(j, channels=['FSC-A', 'FSC-H', 'SSC-A', 'SSC-H', 'B1-A']))
    #if verbose: print ".."
if verbose: print "Converted to arbitrary units"


# Gating
if verbose: print "Gating FSC-A and SSC-A using percentage parameter", percent
data_au_gated = []
for i in data_au:
    data_au_gated.append(
        FlowCal.gate.density2d(
            i,
            channels=['FSC-A', 'SSC-A'],
            gate_fraction=percent,
            bins=[np.logspace(0, 5.42, 1024),
                  np.logspace(0, 5.42, 1024)]
                                )
                            )
    #if verbose: print "Still working.."
if verbose: print "Gating complete."


# Extracting medians
if verbose: print "Extracting medians."
medians_au_gated = []
for i in data_au_gated :
    medians_au_gated.append(
        np.round(np.median(i[:,"B1-A"]), decimals=2 ))


# Creating output file
if verbose: print "Computing average medians and standard deviations."
avg = []
std = []
k=0
if len(medians_au_gated)/replicates == len(grouping):
    while k+1 < len(medians_au_gated) :
        avg.append(np.average(medians_au_gated[k:k+2]))
        std.append(np.std(medians_au_gated[k:k+2]))
        k+=3
else:
    print "The groups you specified do not match with the number of samples and replicates. Check."

if verbose: print "Generating ouputfile", outputfile, "in the current folder."
output = np.column_stack((np.asarray(grouping).flatten(),np.asarray(avg).flatten(),np.asarray(std).flatten()))
header = ["Groups", "Average median fluorescence", "Standard Deviation"]
output = np.vstack((header,output))
np.savetxt(outputfile, output, delimiter=",", fmt='%s')
