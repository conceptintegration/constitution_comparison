
#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2022, Roy Gardner'

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
    f = plt.figure(figsize=(12,9))
    for i,samples in enumerate(samples_list):
        density,x = get_density(samples)
        plt.plot(x,density(x),alpha=0.8,label=labels_list[i])
    plt.xlim(xlim)
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    plt.xlabel('Similarity',fontsize='xx-large')
    plt.ylabel('Density',fontsize='xx-large')
    plt.legend(fontsize='large')
    plt.show()

def plot_pdf(samples,xlim=[0.4,0.9]):
    f = plt.figure(figsize=(12,9))
    density,x = get_density(samples)
    plt.plot(x,density(x),alpha=0.8)

    plt.xlim(xlim)
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    plt.xlabel('Similarity',fontsize='xx-large')
    plt.ylabel('Density',fontsize='xx-large')
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
    plt.xticks(xticks,xticklabels,fontsize='xx-large')
    
    plt.yticks(range(0,len(integrals)),yticklabels,fontsize='xx-large')
    plt.ylabel(ylabel,fontsize='xx-large')
    plt.xlabel(xlabel,fontsize='xx-large')
    plt.gca().invert_yaxis()    
    title = 'Range of similarities ' + str(limits)
    if len(title_suffix) > 0:
        title += ' - ' + title_suffix
    plt.title(title,fontsize='xx-large')
    plt.show()

def do_pdf_integrals_with_polarity(integrals_neg,integrals_pos,topic_labels):
        
    maxs = [] 
    maxs.append(max(integrals_neg))
    maxs.append(max(integrals_pos))
    max_x = int(max(maxs))+1
    
    color_red = '#fd625e'
    color_blue = '#01b8aa'
    index = list(range(0,len(topic_labels)))

    fig, axes = plt.subplots(figsize=(10,24), ncols=2, sharey=False)
    fig.tight_layout()
    
    axes[0].barh(index, integrals_neg, align='center', color=color_red, zorder=10)
    axes[1].barh(index, integrals_pos, align='center', color=color_blue, zorder=10)

    axes[0].invert_xaxis() 
    axes[0].invert_yaxis() 
    axes[1].invert_yaxis() 

    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)

    #axes[0].set_xticks(list(range(0,max_x+1,20)))
    #axes[1].set_xticks(list(range(0,max_x+1,20)))
    axes[0].set_xticks([])
    axes[1].set_xticks([])

    axes[1].set_yticks([])
    axes[0].set_yticks(range(0,len(integrals_neg)))

    axes[0].set_yticklabels(topic_labels)

    axes[0].tick_params(labelsize='xx-large')
    axes[1].tick_params(labelsize='xx-large')
    #axes[0].set_ylabel('Ranked topics',fontsize='xx-large')
    axes[0].set_xlabel('Probability of similar',fontsize='xx-large',)
    axes[1].set_xlabel('Probability of similar',fontsize='xx-large',)
    
    axes[0].set_title('Negative polarity',fontsize='xx-large',)
    axes[1].set_title('Zero or positive polarity',fontsize='xx-large',)
    #axes[0].xaxis.set_label_coords(1.025, -0.055)
    plt.show()
