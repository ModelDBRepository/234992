import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
from graphs.my_graph import *
import matplotlib.pylab as plt
from scipy.stats.stats import pearsonr

def cross_correl_plot(data, FIGSIZE=(7,7), wspace=.5, hspace=.5, right=0.98, left=0.1,\
                      many_data=False):
    """
    'data' should be an array of dictionaries with keys 'vec' and labels 'label'
    """

    fig, AX = plt.subplots(len(data)-1, len(data)-1, figsize=FIGSIZE)
    plt.subplots_adjust(wspace=wspace, hspace=hspace, right=right, left=left)

    mymap = get_linear_colormap(color1='white', color2='gray')

    significance = np.array([1e-3, 2e-2, 1e-1, 1])
    
    for i in range(len(data)-1):
        for j in range(i+1, len(data)):
            AX[j-1,i].plot(data[i]['vec'], data[j]['vec'], 'ko')
            if not many_data:
                set_plot(AX[j-1,i], xlabel=data[i]['label'], ylabel=data[j]['label'],
                                    num_xticks=4, num_yticks=3)
            else:
                if ((i==0) and (j==len(data)-1)):
                    set_plot(AX[j-1,i], xlabel=data[i]['label'], ylabel=data[j]['label'],
                                    num_xticks=4, num_yticks=3)

                elif (j==len(data)-1):
                    set_plot(AX[j-1,i], xlabel=data[i]['label'], yticks_labels=[],
                                    num_xticks=4, num_yticks=3)
                elif (i==0):
                    set_plot(AX[j-1,i], ylabel=data[j]['label'], xticks_labels=[],
                                    num_xticks=4, num_yticks=3)
                else:
                    set_plot(AX[j-1,i], xticks_labels=[], yticks_labels=[],
                                    num_xticks=4, num_yticks=3)

            cc, pp = pearsonr(data[i]['vec'], data[j]['vec'])
            
            x = np.linspace(data[i]['vec'].min(), data[i]['vec'].max())
            AX[j-1, i].plot(x,\
                np.polyval(np.polyfit(np.array(data[i]['vec'], dtype='f8'),\
                                      np.array(data[j]['vec'], dtype='f8'), 1), x),\
                                      'k--', lw=.5)

            ii = np.arange(len(significance))[significance-pp>=0][0]
            color = -1.*(ii-len(significance)+1)/(len(significance)-1)
            xmin, xmax = AX[j-1, i].get_xaxis().get_view_interval()
            ymin, ymax = AX[j-1, i].get_yaxis().get_view_interval()
            AX[j-1, i].add_patch(plt.Rectangle((xmin, ymin),\
                                               xmax-xmin, ymax-ymin, color=mymap(1.*color,1)))

    ax = plt.axes([.7,.7,.02,.2])
    build_bar_legend(np.arange(len(significance)+1),\
                     ax, mymap,\
                     ticks_labels=['n.s.', '$<$0.1', '$<$0.02', '$<$0.001'],
                     label='Significance \n \n (p, Pearson correl.)')
                 
    for ax in AX.flatten():
        if ax.get_xaxis().get_view_interval()[1]==1.:
            ax.axis('off')

    return fig

if __name__=='__main__':

    data = []

    import numpy as np

    for i in range(5):
        data.append({'vec':np.random.randn(10), 'label':'label'+str(i+1)})

    cross_correl_plot(data, many_data=True)
    plt.show()
