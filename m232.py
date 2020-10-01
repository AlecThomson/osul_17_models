#=============================================================================#
#                          MODEL DEFINITION FILE                              #
#=============================================================================#
import numpy as np


#-----------------------------------------------------------------------------#
# Function defining the model.                                                #
#                                                                             #
#  pDict       = Dictionary of parameters, created by parsing inParms, below. #
#  lamSqArr_m2 = Array of lambda-squared values                               #
#  quArr       = Complex array containing the Re and Im spectra.              #
#-----------------------------------------------------------------------------#
def sinc(x):
    return np.sinc(x / np.pi)
def model(pDict, lamSqArr_m2):
    """O'Sullivan 2017 model"""
    terms = 3
    # Calculate the complex fractional q and u spectra
    quArr = 0 + 0j
    for i in range(terms):
        pArr = pDict[f"fracPol_{i}"] * np.ones_like(lamSqArr_m2)
        quArr += pArr * \
            np.exp(2j * (np.radians(pDict[f"psi0_{i}_deg"]) + pDict[f"RM_{i}_radm2"] * lamSqArr_m2)) * \
            (sinc(pDict[f"delta_{i}_RM"] * lamSqArr_m2)) * \
            np.exp(-2 * pDict[f"sigma_{i}_RM"]**2 * lamSqArr_m2**2)

    return quArr


#-----------------------------------------------------------------------------#
# Parameters for the above model.                                             #
#                                                                             #
# Each parameter is defined by a dictionary with the following keywords:      #
#   parname    ...   parameter name used in the model function above          #
#   label      ...   latex style label used by plotting functions             #
#   value      ...   value of the parameter if priortype = "fixed"            #
#   bounds     ...   [low, high] limits of the prior                          #
#   priortype  ...   "uniform", "normal", "log" or "fixed"                    #
#   wrap       ...   set > 0 for periodic parameters (e.g., for an angle)     #
#-----------------------------------------------------------------------------#
terms = 3
inParms = []
for i in range(terms):
    inParms += [
    {"parname":   f"fracPol_{i}",
     "label":     f"$p_{{0,{i}}}$",
     "value":     0.1+np.random.rand()*10,
     "bounds":    [0.001, 1.0],
     "priortype": "uniform",
     "wrap":      0},

    {"parname":   f"psi0_{i}_deg",
     "label":     f"$\psi_{{0,{i}}}$ ($^\circ$)",
     "value":     0.0+np.random.rand()*10,
     "bounds":    [0.0, 180.0],
     "priortype": "uniform",
     "wrap":      1},

    {"parname":   f"RM_{i}_radm2",
     "label":     f"$\phi_{{0,{i}}}$ (rad m$^{{-2}}$)",
     "value":     0.0+np.random.rand()*10,
     "bounds":    [-1000.0, 1000.0],
     "priortype": "uniform",
     "wrap":      0},

    {"parname":   f"delta_{i}_RM",
     "label":     f"$\Delta\phi_{i}$ (rad m$^{{-2}}$)",
     "value":     10.0+np.random.rand()*10,
     "bounds":    [0, 1100.0],
     "priortype": "uniform",
     "wrap":      0},

    {"parname":   f"sigma_{i}_RM",
     "label":     f"$\sigma_{{\phi,{i}}}$ (rad m$^{{-2}}$)",
     "value":     100.0+np.random.rand()*10,
     "bounds":    [0, 1100.0],
     "priortype": "uniform",
     "wrap":      0},
    ]


#-----------------------------------------------------------------------------#
# Arguments controlling the Nested Sampling algorithm                         #
#-----------------------------------------------------------------------------#
nestArgsDict = {"n_live_points": 1000,
                "verbose": False}
