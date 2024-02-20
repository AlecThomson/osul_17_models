#=============================================================================#
#                          MODEL DEFINITION FILE                              #
#=============================================================================#
import numpy as np
import bilby
import numpy as np
from bilby.core.prior import Constraint, PriorDict
from functools import partial


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
            (sinc(pDict[f"Delta_{i}_RM"] * lamSqArr_m2)) * \
            np.exp(-2 * pDict[f"sigma_{i}_RM"]**2 * lamSqArr_m2**2)

    return quArr


# -----------------------------------------------------------------------------#
# Priors for the above model.                                                 #
# See https://lscsoft.docs.ligo.org/bilby/prior.html for details.             #
#                                                                             #
# -----------------------------------------------------------------------------#
def converter(parameters, nterms):
    """
    Function to convert between sampled parameters and constraint parameter.

    Parameters
    ----------
    parameters: dict
        Dictionary containing sampled parameter values, 'RM1_radm2', 'RM1_radm2',
        'fracPol1', 'fracPol2'

    Returns
    -------
    dict: Dictionary with constraint parameter 'delta_RM1_RM2_radm2' and 'sum_p1_p2' added.
    """
    converted_parameters = parameters.copy()
    for i in range(nterms-1):
        converted_parameters[f"delta_RM{i}_{i+1}_radm2"] = (
            parameters[f"RM_{i}_radm2"] - parameters[f"RM_{i+1}_radm2"]
        )
    converted_parameters["sum_p"+"_".join([f"{i}" for i in range(nterms)])] = np.sum([parameters[f"fracPol_{i}"] for i in range(nterms)])
    return converted_parameters

terms = 3
priors = PriorDict(conversion_function=partial(converter, nterms=terms))
for i in range(terms):
    priors[f"fracPol{i+1}"] = bilby.prior.Uniform(
        minimum=0.0,
        maximum=1.0,
        name=f"fracPol{i+1}",
        latex_label=r"$p_1$",
    )
    priors[f"psi0{i+1}_deg"] = bilby.prior.Uniform(
        minimum=0,
        maximum=180.0,
        name=f"psi0{i+1}_deg",
        latex_label=fr"$\psi_{{0,{i+1}}}$ (deg)",
        boundary="periodic",
    )

    priors[f"RM{i+1}_radm2"] = bilby.prior.Uniform(
        minimum=-1100.0,
        maximum=1100.0,
        name=f"RM{i+1}_radm2",
        latex_label=fr"$\phi_{i+1}$ (rad m$^{{-2}}$)",
    )
    priors[f"sigma_{i}_RM"] = bilby.prior.Uniform(
        minimum=0,
        maximum=1100.0,
        name=f"sigma_{i}_RM",
        latex_label=fr"$\sigma_{{\phi,{i}}}$ (rad m$^{{-2}}$)",
    )
    priors[f"Delta_{i}_RM"] = bilby.prior.Uniform(
        minimum=0,
        maximum=1100.0,
        name=f"Delta_{i}_RM",
        latex_label=fr"$\Delta\phi_{i}$ (rad m$^{{-2}}$)",
    )

if terms > 1:
    for i in range(terms-1):
        priors[f"delta_RM{i}_{i+1}_radm2"] = Constraint(
            minimum=0,
            maximum=1100.0/terms,
            name=f"delta_RM{i}_{i+1}_radm2",
            latex_label=fr"$\Delta\phi_{i,i+1}$ (rad m$^{{-2}}$)",
        )
    priors["sum_p"+"_".join([f"{i}" for i in range(terms)])] = Constraint(
        minimum=0.0,
        maximum=1.0,
        name="sum_p"+"_".join([f"{i}" for i in range(terms)]),
        latex_label=r"$p" + r"p_".join([fr"{i}+" for i in range(terms)]) + r"$",
    )