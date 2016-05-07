##### Do not edit below this line #######

from input import *

import FlowCal
import matplotlib.pyplot as plt
import glob
import numpy as np


# Reading files
fcs_read = []
for i in glob.glob("*.fcs") :
    fcs_read.append(FlowCal.io.FCSData(i))
    if verbose: print "Reading", i

if len(fcs_read)/replicates <> len(grouping):
    print "The groups you specified do not match with the number of samples and replicates. Check and run again."
    from sys import exit
    exit(0)

# Converting to a.u.
if verbose: print "Converting data to arbitrary units."
data_au = []
for j in fcs_read:
    #converts each sample's fluorescence to a.u./rfi
    data_au.append(FlowCal.transform.to_rfi(j, channels=['FSC-A', 'FSC-H', 'SSC-A', 'SSC-H', 'B1-A']))
    #if verbose: print ".."
if verbose: print "Converted to arbitrary units."


# Gating
if verbose: print "Gating FSC-A and SSC-A using percentage parameter", percent, ". Depending on the number of samples, this can take some time."
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
while k+1 < len(medians_au_gated) :
    avg.append(np.average(medians_au_gated[k:k+2]))
    std.append(np.std(medians_au_gated[k:k+2]))
    k+=3

if verbose: print "Generating ouputfile", outputfile, "in the current folder."
output = np.column_stack((np.asarray(grouping).flatten(),np.asarray(avg).flatten(),np.asarray(std).flatten()))
header = ["Groups", "Average median fluorescence", "Standard Deviation"]
output = np.vstack((header,output))
np.savetxt(outputfile, output, delimiter=",", fmt='%s')
print "Complete."
