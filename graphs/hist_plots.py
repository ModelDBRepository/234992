import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.my_graph import set_plot, show
import matplotlib.pylab as plt
import numpy as np

def hist(x, bins=20, ax=None,
         edgecolor='k', facecolor='b'):
    
    hist, be = np.histogram(x, bins=bins)
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(5,3))
        plt.subplots_adjust(bottom=.2, left=.2)
    ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], lw=2,\
           edgecolor=edgecolor, facecolor=facecolor)
    return ax
    
def gghist(x, bins=20, ax=None, label=''):

    hist, be = np.histogram(x, bins=bins)
    
    with plt.style.context(('ggplot')):
        if ax is None:
            fig, ax = plt.subplots(figsize=(4,3))
            plt.subplots_adjust(bottom=.2, left=.2)
        ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], label=label)
        
    return ax

def multiple_gghists(X, bins=20, ax=None, LABELS=None):

    if LABELS is None:
        LABELS = ['' for i in range(len(X))]
        
    ax = gghist(X[0], bins=bins, ax=ax, label=LABELS[0])
    for x, label in zip(X[1:], LABELS[1:]):
        hist, be = np.histogram(x, bins=bins)
        ax.bar(.5*(be[1:]+be[:-1]), hist, width=be[1]-be[0], label=label)
    return ax

if __name__=='__main__':

    import numpy as np
    ax = multiple_gghists([np.random.randn(100), np.random.randn(100)],\
                     LABELS=['Data 1', 'Data 2'])
    ax.legend()
    show(plt)

