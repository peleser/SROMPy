# Copyright 2018 United States Government as represented by the Administrator of
# the National Aeronautics and Space Administration. No copyright is claimed in
# the United States under Title 17, U.S. Code. All Other Rights Reserved.

# The Stochastic Reduced Order Models with Python (SROMPy) platform is licensed
# under the Apache License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import numpy as np
from collections import OrderedDict

from SROMPy.target import SampleRandomVector
from SROMPy.srom import SROM, SROMSurrogate
from SROMPy.postprocess import Postprocessor

'''
Compare piecewise constant SROM approximations to the EOL for m=5,10,20
Produces Figure 5(a) in the paper
'''

#Target Monte Carlo input samples for comparison
targetsamples = "mc_data/eol_samples_MC.txt"

#SElect 3 SROM sizes
sromsizes = [5,10,20]
srom_dir = "srom_data"

#Plotting specs:
varz = [r'EOL (Cycles)']
xlimits = [[1.0e6, 2.0e6]]
ylimits = [[-0.01, 1.1]]
xticks = [[r'$1.0 \times 10^6$','',r'$1.4 \times 10^6$','',
           r'$1.8 \times 10^6$','']]
xaxispadding = 5
axisfontsize = 24
labelfontsize = 20
legendfontsize = 20
showplot = False
cdfylabel = True        #Label y axis as "CDF"
plot_dir = "plots"
plot_suffix = "SROM_pwconst_eol_CDF_m"
for m in sromsizes:
    plot_suffix += "_" + str(m)

#Load / initialize target random variable from samples:
samples = np.genfromtxt(targetsamples)
target = SampleRandomVector(samples)

#Set x limits for each variable based on target:
#xlimits = [[np.min(samples), np.max(samples)]]

#Build up sromsize-to-SROM object map for plotting routine
sroms = OrderedDict()

for sromsize in sromsizes:

    #Generate input SROM from file:
    srom = SROM(sromsize, target._dim)
    sromfile = "srom_m" + str(sromsize) + ".txt"
    sromfile = os.path.join(srom_dir, sromfile)
    srom.load_params(sromfile)
        
    #Generate SROM surrogate for output from EOLs & input srom:
    eolfile = "srom_eol_m" + str(sromsize) + ".txt"
    eolfile = os.path.join(srom_dir, eolfile)
    eols = np.genfromtxt(eolfile)

    sroms[sromsize] = SROMSurrogate(srom, eols)
 
Postprocessor.compare_srom_CDFs(sroms, target, plotdir="plots",
                                plotsuffix=plot_suffix, variablenames=varz,                                     xlimits=xlimits, ylimits=ylimits, xticks=xticks,
                                cdfylabel=True, xaxispadding=xaxispadding,
                                axisfontsize=axisfontsize, 
                                labelfontsize=labelfontsize,
                                legendfontsize=legendfontsize)

