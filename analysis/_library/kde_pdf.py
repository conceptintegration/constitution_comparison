
#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2022, Roy Gardner and Sally Gardner'

from packages import *


def get_density(samples,covariance_factor=0.4):
    density = stats.gaussian_kde(samples)
    xmin = min(samples)
    xmax = max(samples)
    x = np.linspace(xmin, xmax)
    density.covariance_factor = lambda:covariance_factor
    density._compute_covariance()
    return density,x
    

def plot_pdfs(samples_list,labels_list,xlim=[0.4,0.9]):
    twenty_distinct_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0',\
                            '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324',\
                            '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff',\
                            '#000000', '#fffac8']
    f = plt.figure(figsize=(12,9))
    for i,samples in enumerate(samples_list):
        density,x = get_density(samples)
        plt.plot(x,density(x),alpha=0.8,label=labels_list[i],color=twenty_distinct_colors[i])
    plt.xlim(xlim)
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')
    plt.xlabel('Similarity',fontsize='large')
    plt.ylabel('Density',fontsize='large')
    plt.legend(fontsize='large')
    plt.show()

def plot_pdf(samples,xlim=[0.4,0.9]):
    f = plt.figure(figsize=(12,9))
    density,x = get_density(samples)
    plt.plot(x,density(x),alpha=0.8)

    plt.xlim(xlim)
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')
    plt.xlabel('Similarity',fontsize='large')
    plt.ylabel('Density',fontsize='large')
    plt.show()

def integrate_pdf(samples,limits,sample_size=2):
    if len(samples) < sample_size:
        return 0
    density,x = get_density(samples)
    upper = limits[1]
    if upper > max(samples):
        upper =  max(samples)
    area = density.integrate_box_1d(limits[0],upper)
    if area < 0:
        area = 0
    return area

def get_pdf_integrals(samples,limits,sample_size=2):
    integrals = [integrate_pdf(s,limits,sample_size=sample_size) for _,s in enumerate(samples)]
    return integrals

def plot_pdf_integrals(integrals,yticklabels,limits,xlabel,ylabel,title_suffix='',figsize=(10,24)):
    f = plt.figure(figsize=figsize)
    plt.barh(range(0,len(integrals)),integrals,alpha=0.6)
    
    plt.xlim([0,max(integrals)])    
    xticks = [0,max(integrals)]
    xticklabels = ['Low','High']
    plt.xticks(xticks,xticklabels,fontsize='large')
    
    plt.yticks(range(0,len(integrals)),yticklabels,fontsize='large')
    plt.ylabel(ylabel,fontsize='large')
    plt.xlabel(xlabel,fontsize='large')
    plt.gca().invert_yaxis()    
    title = 'Range of similarities ' + str(limits)
    if len(title_suffix) > 0:
        title += ' - ' + title_suffix
    plt.title(title,fontsize='large')
    plt.show()