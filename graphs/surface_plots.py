import numpy as np
from matplotlib import cm

def twoD_plot(ax, x, y, z, alpha=1., cmap=cm.viridis, interpolation='none',):
    """
    surface plots for x, y and z 1 dimensional data
    """
    x, y = np.array(x), np.array(y)
    Z = np.ones((len(np.unique(y)), len(np.unique(x))))*np.nan
    for i, yy in enumerate(np.unique(y)):
        cond1 = y==yy
        for j, xx in enumerate(np.unique(x[cond1])):
            # Z.append(z[cond1][x[cond1]==xx])
            Z[i,j] = z[cond1][x[cond1]==xx]
    z1 = np.array(Z).reshape(len(np.unique(y)), len(np.unique(x)))
    z1 = Z
    return ax.imshow(z1, interpolation=interpolation,
                     extent = (x.min(), x.max(), y.min(), y.max()),
                     alpha=alpha, cmap=cmap, origin='lower', aspect='auto')
    

if __name__=='__main__':
    from my_graph import *
    x, y = np.meshgrid(np.arange(10), np.arange(20))
    z = x*y
    x, y, z = np.array(x).flatten(), np.array(y).flatten(), np.array(z).flatten()
    index = np.arange(len(x))
    np.random.shuffle(index)
    x, y, z = x[index], y[index], z[index]
    # x, y, z = x[z>20], y[z>20], z[z>20]
    ax = twoD_plot(plt.gca(), x[x<y], y[x<y], z[x<y]*0.+1, cmap=cm.Greys)
    ax = twoD_plot(plt.gca(), x, y, z, interpolation='bilinear')
    plt.gca().set_xticks(np.arange(6)*2)
    plt.colorbar(ax)
    plt.savefig('/Users/yzerlaut/Desktop/1.svg')
    show()
