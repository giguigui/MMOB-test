# Created to .py by Meritxell Pacheco
# 01.11.2017

from biogeme import *
from headers import *
from loglikelihood import *
from statistics import *

#Parameters to be estimated
# Arguments:
#   1  Name for report. Typically, the same as the variable
#   2  Starting value
#   3  Lower bound
#   4  Upper bound
#   5  0: estimate the parameter, 1: keep it fixed
ASC_CAR = Beta('ASC_CAR',0,-10,10,0)
BETA_TIME_RAIL = Beta('BETA_TIME_RAIL',0,-10,10,0)
BETA_TIME_CAR = Beta('BETA_TIME_CAR',0,-10,10,0)
BETA_COST_AGE1 = Beta('BETA_COST_AGE1',0,-10,10,0)
BETA_COST_AGE2 = Beta('BETA_COST_AGE2',0,-10,10,0)
BETA_FEMALE = Beta('BETA_FEMALE',0,-10,10,0)
BETA_FIXED_ARRIVAL_TIME = Beta('BETA_FIXED_ARRIVAL_TIME',0,-10,10,0)

# Define here arithmetic expressions for name that are not directly available from the dataxpressions for name that are not directly available from the data
one  = DefineVariable('one',1)
TravelTimeRail  = DefineVariable('TravelTimeRail',rail_ivtt + rail_acc_time + rail_egr_time)
TravelTimeCar = DefineVariable('TravelTimeCar',car_ivtt + car_walk_time)
rate_G2E = DefineVariable('rate_G2E', 0.44378022) #from Guilders to euros
CostCarEuro = DefineVariable('CostCarEuro', car_cost * rate_G2E)
CostRailEuro = DefineVariable('CostRailEuro', rail_cost * rate_G2E)
Age1 = DefineVariable('Age1',(age == 0)) #40 years or younger
Age2 = DefineVariable('Age2',(age == 1)) #41 years or older
Employed = DefineVariable('Employed',(employ_status == 0))
theWeight = DefineVariable('theWeight' ,1)


# Utilities
V_CAR = ASC_CAR + BETA_TIME_CAR * TravelTimeCar + BETA_COST_AGE1 * CostCarEuro * Age1 + BETA_COST_AGE2 * CostCarEuro * Age2
V_RAIL = BETA_TIME_RAIL * TravelTimeRail + BETA_COST_AGE1 * CostRailEuro * Age1 + BETA_COST_AGE2 * CostRailEuro * Age2 + BETA_FEMALE * gender + BETA_FIXED_ARRIVAL_TIME * arrival_time

# Associate utility functions with the numbering of alternatives
V = {0: V_CAR, 1: V_RAIL}
av = {0: one,1: one}

# MNL (Multinomial Logit model), with availability conditions
logprob = bioLogLogit(V,av,choice)

# Defines an itertor on the data
rowIterator('obsIter') 

# Define the likelihood function for the estimation
BIOGEME_OBJECT.ESTIMATE = Sum(logprob,'obsIter')
BIOGEME_OBJECT.WEIGHT = theWeight

# The following parameters are imported from bison biogeme. You may want to remove them and prefer the default value provided by pythonbiogeme.
BIOGEME_OBJECT.PARAMETERS['optimizationAlgorithm'] = "BIO"
BIOGEME_OBJECT.PARAMETERS['stopFileName'] = "STOP"
