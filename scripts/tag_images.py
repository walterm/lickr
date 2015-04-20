from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import numpy as np
from numpy.linalg import norm
import sys

HEX_RED = 'ff0000'
HEX_ORANGE = 'ffa500'
HEX_YELLOW = 'ffff00'
HEX_GREEN = '008000'
HEX_BLUE = '0000ff'
HEX_PURPLE = '800080'
TARGETS = [HEX_RED, HEX_ORANGE, HEX]

def compute_colors(image_path):
    CLUSTERS = 4
    image = Image.open(image_path)
    image = image.resize((150, 150))
    ar = scipy.misc.fromimage(image)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])

    # Clustering
    codes, dist = scipy.cluster.vq.kmeans(ar, CLUSTERS)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    print counts, bins

    # HEX Codes
    return [''.join(chr(c) for c in code).encode('hex') for code in codes]

def compute_closest(hex_code):
    '''L2 norm.'''

    def compute_norm(c1, c2):
        a = np.array(c1)
        b = np.array(c2)
        return norm(a-b)

    def compute_rgb(hex_code):
        return (
            int(hex_code[0:2].encode('hex')),
            int(hex_code[2:4].encode('hex')),
            int(hex_code[4:].encode('hex'))
        )

    rgb = compute_rgb(hex_code)
    c = compute_rgb(TARGETS[0])

    similiar = compute_norm(rgb, c)
    index = 0

    for i in range(1, len(TARGETS)):
        c = compute_rgb(TARGETS[i])
        if compute_norm(rgb, c) < similiar: # The smaller, the more similar
            similiar = compute_norm(rgb, c)
            index = i
    return TARGETS[i]
