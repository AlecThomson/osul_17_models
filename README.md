# osul_17_models
Model files matching [O'Sullivan+ 2017](https://ui.adsabs.harvard.edu/abs/2017MNRAS.469.4034O/abstract). For use with [RM-tools](https://github.com/CIRADA-Tools/RM-Tools/).

$$ P_j = Q_j + iU_j = p_{0,j} \, I\, e^{2 i (\psi_{0_j}+{\rm RM}_j \lambda^2)}  \frac{\sin \Delta {\rm RM}_j \lambda^2}{\Delta {\rm RM}_j \lambda^2} e^{-2\sigma^2_{{\rm RM}_j} \lambda^4} $$

$$ P = \sum_{i=0}^{N} P_j, N \in [1,2,3]$$

This model has three terms: 
- RM x internal dispersions x external dispersion. 

More complex models can be produced by the sum of these terms.

Name of files corresponds to the type of model with three digits:
- First digit: Always 2, dummy number
- Second digit:
    * 0 - RM only
    * 1 - RM and internal dispersion
    * 2 - RM and external dispersion
    * 3 - RM, internal, and external dispersion
- Third digit:
    * 0 - One component
    * 1 - Two components
    * 2 - Three components
