
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import os


class Postprocessor:
    '''
    Class for comparing an SROM vs the target random vector it is modeling. 
    Capabilities for plotting CDFs/pdfs and tabulating errors in moments, 
    correlations, etc. 
    '''


    def __init__(self, srom, targetrv):
        '''
        Initialize class with previously initialized srom & targetrv objects.
        '''

        #TODO - check to make sure srom/targetrv are initialized & have the 
        #needed functions implemented (compute_moments/cdfs/ etc.)

        self._SROM = srom
        self._target = targetrv

    def compare_CDFs(self, variable="x", plotdir='.', plotsuffix="CDFcompare", 
                     showFig=True, saveFig=True, variablenames=None):
        '''
        Generates plots comparing the srom & target cdfs for each dimension
        of the random vector.

        inputs:
            variable, str, name of variable being plotted
            plotsuffix, str, name for saving plot (will append dim & .pdf)
            plotdir, str, name of directory to store plots
            showFig, bool, show or not show generated plot
            saveFig, bool, save or not save generated plot
            variablenames, list of strings, names of variable in each dimension
                optional. Used for x axes labels if provided. 
        '''

        xgrids = self.generate_cdf_grids()
        sromCDFs = self._SROM.compute_CDF(xgrids)
        targetCDFs = self._target.compute_CDF(xgrids)

        #Start plot name string if it's being stored
        if saveFig:
            plotname = os.path.join(plotdir, plotsuffix)
        else:
            plotname = None

        #Get variable names:
        if variablenames is not None:
            if len(variablenames) != self._SROM._dim:
                raise ValueError("Wrong number of variable names provided")
        else:
            variablenames = []
            for i in range(self._SROM._dim):
                if self._SROM._dim==1:
                    variablenames.append(variable)
                else:
                    variablenames.append(variable + "_" + str(i+1))

        for i in range(self._SROM._dim):

            variable = variablenames[i]
            plotname_ = plotname + "_" + variable + ".pdf"
            ylabel = "F(" + variable + ")"
            #Remove latex math symbol from plot name
            plotname_ = plotname_.translate(None, "$")
            self.plot_cdfs(xgrids[:,i], sromCDFs[:,i], targetCDFs[:,i], 
                           variable, ylabel, plotname_, showFig)


    def plot_cdfs(self, xgrid, sromcdf, targetcdf, xlabel="x", ylabel="F(x)", 
                  plotname=None, showFig=True, xlimits=None):
        '''
        Plotting routine for comparing a single srom/target cdf
        '''
        
        #Text formatting for plot
        title_font = {'fontname':'Arial', 'size':22, 'weight':'bold',
                                    'verticalalignment':'bottom'}
        axis_font = {'fontname':'Arial', 'size':26, 'weight':'normal'}
        labelFont = 'Arial'
        labelSize =  20      
        legendFont = 22
    
        #Plot CDFs
        fig,ax = plt.subplots(1)
        ax.plot(xgrid, sromcdf, 'r--', linewidth=4.5, label = 'SROM')
        ax.plot(xgrid, targetcdf, 'k-', linewidth=2.5, label = 'Target')
        ax.legend(loc='best', prop={'size': legendFont})

        #Labels/limits    
        y_limz = ax.get_ylim()
        x_limz = ax.get_xlim()
        ax.axis([min(xgrid), max(xgrid), 0, 1.1])
        if(xlimits is not None):
            ax.axis([xlimits[0], xlimits[1], 0, 1.1])
        ax.set_xlabel(xlabel, **axis_font)
        ax.set_ylabel(ylabel, **axis_font)

        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(labelFont)
            label.set_fontsize(labelSize)

        plt.tight_layout()

        if plotname is not None:
            plt.savefig(plotname)
        if showFig:
            plt.show()    


    def generate_cdf_grids(self, cdf_grid_pts=1000):
        '''
        Generate numerical grids for plotting CDFs based on the 
        range of the target random vector. Return  x_grid variable with
        cdf_grid_pts along each dimension of the random vector.
        '''

        x_grid = np.zeros((cdf_grid_pts, self._target._dim))

        for i in range(self._target._dim):
            grid = np.linspace(self._target._mins[i],
                               self._target._maxs[i],
                               cdf_grid_pts)
            x_grid[:,i] = grid

        return x_grid


#Need to make this whole class static
#----------------Gross down here, don't look -----------------------
    @staticmethod
    def compare_srom_CDFs(size2srom, target, variable="x", plotdir=".",
                            plotsuffix="CDFscompare", showFig=True, 
                            saveFig = True, variablenames=None,
                            xlimits=None):
        '''
        Generates plots comparing CDFs from sroms of different sizes versus 
        the target variable for each dimension of the vector.

        inputs:
            size2srom, dict, key=size of SROM (int), value = srom object
            target, TargetRV, target random variable object
            variable, str, name of variable being plotted
            plotsuffix, str, name for saving plot (will append dim & .pdf)
            plotdir, str, name of directory to store plots
            showFig, bool, show or not show generated plot
            saveFig, bool, save or not save generated plot
            variablenames, list of strings, names of variable in each dimension
                optional. Used for x axes labels if provided. 
        '''

        #Make x grids for plotting
        cdf_grid_pts=1000
        xgrids = np.zeros((cdf_grid_pts, target._dim))

        for i in range(target._dim):
            grid = np.linspace(target._mins[i],
                               target._maxs[i],
                               cdf_grid_pts)
            xgrids[:,i] = grid

        #Get CDFs for each size SROM
        sromCDFs = OrderedDict()
        for m,srom in size2srom.iteritems():
            sromCDFs[m] = srom.compute_CDF(xgrids)

        targetCDFs = target.compute_CDF(xgrids)

        #Start plot name string if it's being stored
        if saveFig:
            plotname = os.path.join(plotdir, plotsuffix)
        else:
            plotname = None

        #Get variable names:
        if variablenames is not None:
            if len(variablenames) != target._dim:
                raise ValueError("Wrong number of variable names provided")
        else:
            variablenames = []
            for i in range(target._dim):
                if target._dim==1:
                    variablenames.append(variable)
                else:
                    variablenames.append(variable + "_" + str(i+1))

        for i in range(target._dim):

            variable = variablenames[i]
            plotname_ = plotname + "_" + variable + ".pdf"
            ylabel = r'$F($' + variable + r'$)$'
            #Remove latex math symbol from plot name
            plotname_ = plotname_.translate(None, "$")

            #---------------------------------------------
            #PLOT THIS DIMENSION:
            #Text formatting for plot
            title_font = {'fontname':'Arial', 'size':22, 'weight':'bold',
                                    'verticalalignment':'bottom'}
            axis_font = {'fontname':'Arial', 'size':26, 'weight':'normal'}
            labelFont = 'Arial'
            labelSize =  20
            legendFont = 22
       
            xgrid=xgrids[:,i]
            targetcdf = targetCDFs[:,i]

            linez = ['g-','r:','b--']
            widthz = [2.5, 4, 3.5]
            #Plot CDFs
            fig,ax = plt.subplots(1)
            ax.plot(xgrid, targetcdf, 'k-', linewidth=2.5, label = 'Target')
            for j,m in enumerate(sromCDFs.keys()):
                #label = "SROM (m=" + str(m) + ")"
                label = "m = " + str(m) 
                sromcdf = sromCDFs[m][:,i]
                ax.plot(xgrid, sromcdf, linez[j], linewidth=widthz[j], label=label)
            ax.legend(loc='best', prop={'size': legendFont})

            #Labels/limits    
            y_limz = ax.get_ylim()
            x_limz = ax.get_xlim()
            ax.axis([min(xgrid), max(xgrid), 0, 1.1])
            if(xlimits is not None):
                ax.axis([xlimits[i][0], xlimits[i][1], 0, 1.1])
            ax.set_xlabel(variable, **axis_font)
            ax.set_ylabel(ylabel, **axis_font)

            for label in (ax.get_xticklabels() + ax.get_yticklabels()):
                label.set_fontname(labelFont)
                label.set_fontsize(labelSize)

            plt.tight_layout()

            if plotname_ is not None:
                plt.savefig(plotname_)
            if showFig:
                plt.show()