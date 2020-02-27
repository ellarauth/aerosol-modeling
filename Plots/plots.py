#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 22:25:13 2020

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import binned_statistic,binned_statistic_2d

datadir="aerosol-modeling-master/data/final"

data=pd.DataFrame()

for fname in os.listdir(datadir):
    df=pd.read_csv(os.path.join(datadir,fname))
    data=pd.concat([data,df])


tmin,tmax=data["t"].min(),data["t"].max()
bins=np.linspace(tmin,tmax,num=20)

means,_,_=binned_statistic(data["t"],data["concentration"],statistic="mean",bins=bins)
medians,_,_=binned_statistic(data["t"],data["concentration"],statistic="median",bins=bins)
bin_centres,_,_=binned_statistic(bins,bins,statistic="mean",bins=bins)
plt.semilogy(data["t"], data["concentration"],'.',bin_centres,medians,'r-')
plt.xlabel("t")
plt.ylabel("concentration")
plt.savefig("plotti.pdf")


cmin,cmax=data["co"].min(),data["co"].max()
cbins=np.linspace(cmin,cmax,num=20)

means,_,_=binned_statistic(data["co"],data["concentration"],statistic="mean",bins=bins)
medians,_,_=binned_statistic(data["co"],data["concentration"],statistic="median",bins=bins)
bin_centres,_,_=binned_statistic(bins,bins,statistic="mean",bins=bins)
plt.plot(data["co"], data["concentration"],'.',bin_centres,means,'r-')
plt.xlabel("co")
plt.ylabel("concentration")
plt.savefig("plotti2.pdf")


z,x,y,_=binned_statistic_2d(data["t"],data["co"],data["concentration"],statistic="mean",bins=40)
plt.pcolormesh(x,y,z)
plt.savefig("heatmap.pdf")

