#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import math

data=pd.read_csv('aerosol-modeling-master/data/final/HYY.csv')

data['month']=[data['date'][x][5:7] for x in range(len(data['date']))]
#The month is extracted from date and added to data as a new column. These can be used
#as qualitative predictors in the model. However, they seemed not to be very useful.

data['month_value']=[math.cos((2*math.pi/12)*int(x)+math.pi/6) for x in data['month']]
#Every month is given a value with a cos function. The values are placed into 'month_value'
#column. math.pi/6 is an adjustment term that defines which months get the maximum and
#minimum values. Neither this improved significantly models I tried.

#Taking the observation time into account seems not to improve model significantly.
#You may try these predictors, but probably you will find them quite useless.



#data.to_csv('hyy.csv')