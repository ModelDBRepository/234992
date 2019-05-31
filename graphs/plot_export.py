import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import string, datetime

# SPECIAL PYTHON PACKAGES FOR:
import svgutils.compose as sg # SVG
import fpdf # PDF
from PIL import Image # BITMAP (png, jpg, ...)

def put_list_of_figs_to_svg_fig(FIGS, CAP_SIZE=14,\
                                fig_name="fig.svg", visualize=True,\
                                transparent=True, correc_factor=70.):
    """ take a list of figures and make a multi panel plot"""
    
    label = list(string.ascii_uppercase)[:len(FIGS)]

    SIZE = []
    for fig in FIGS:
        SIZE.append(fig.get_size_inches())
    width = np.max([s[0] for s in SIZE])
    height = np.max([s[1] for s in SIZE])

    LABELS, XCOORD, YCOORD = [], [], []
    # saving as svg
    for i in range(len(FIGS)):
        ff = 'f.svg'
        FIGS[i].savefig('/tmp/'+str(i)+'.svg', format='svg',
                        transparent=transparent)
        LABELS.append(label[i])
        XCOORD.append((i%3)*width*correc_factor)
        YCOORD.append(int(i/3)*height*correc_factor)

    PANELS = []
    for i in range(len(FIGS)):
        PANELS.append(sg.Panel(\
            sg.SVG('/tmp/'+str(i)+'.svg').move(XCOORD[i],YCOORD[i]),\
            sg.Text(LABELS[i], 25, 20, size=12, weight='bold').move(\
                                                XCOORD[i],YCOORD[i]))\
        )
    sg.Figure(str(.3*3.*width)+"cm", str(.3*height*int(len(FIGS)/3))+"cm",\
              *PANELS).save(fig_name)

    if visualize:
        _ = True

def put_list_of_figs_to_multipage_pdf(FIGS,
                                      pdf_name='figures.pdf',
                                      pdf_title=''):
    """
    adapted from:
    http://matplotlib.org/examples/pylab_examples/multipage_pdf.html
    """
    
    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    with PdfPages(pdf_name) as pdf:
        
        for fig in FIGS:
            pdf.savefig(fig)  # saves the current figure into a pdf page

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = u'Y. Zerlaut'
        # d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime(2009, 11, 13)
        d['ModDate'] = datetime.datetime.today()


def concatenate_pngs(PNG_LIST, ordering='vertically', figname='fig.png'):
    
    images = map(Image.open, PNG_LIST)
    widths, heights = zip(*(i.size for i in images))

    if ordering=='vertically':
        total_height = sum(heights)
        max_width = max(widths)
        new_im = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for fig in PNG_LIST:
            im = Image.open(fig)
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

    new_im.save(figname)


if __name__=='__main__':

    from my_graph import *
    fig1, _ = plt.subplots(figsize=(2,2))
    add_errorbar(plt.gca(), [0], [1], [.2])
    set_plot(plt.gca())
    fig2, _ = plt.subplots(figsize=(2,2))
    add_errorbar(plt.gca(), [0], [1], [.2])
    set_plot(plt.gca())
    put_list_of_figs_to_multipage_pdf([fig1, fig2])
        
