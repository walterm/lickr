from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import numpy as np
from numpy.linalg import norm
import struct

HEX_RED = 'ff0000'
HEX_ORANGE = 'ffa500'
HEX_YELLOW = 'ffff00'
HEX_GREEN = '008000'
HEX_BLUE = '0000ff'
HEX_PURPLE = '800080'
TARGETS = [HEX_RED, HEX_ORANGE, HEX_YELLOW, HEX_GREEN, HEX_BLUE, HEX_PURPLE]


def compute_rgb(hex_code):
    return struct.unpack('BBB', hex_code.decode('hex'))

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def palette_cluster(hex_codes):
    rgb_colors = [compute_rgb(code) for code in hex_codes]
    color_matrix = np.zeros((len(rgb_colors), 3))
    for i in range(len(rgb_colors)):
        color_matrix[i, :] = rgb_colors[i]
    centers, dist = scipy.cluster.vq.kmeans(color_matrix, 4)
    centers = centers.astype(int)
    return [''.join(chr(c) for c in center).encode('hex') for center in centers]


def random_palette(hex_codes):
    def partition(lst, n): 
        division = len(lst) / float(n) 
        return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n) ]

    from random import shuffle

    rgb_colors = [compute_rgb(code) for code in hex_codes]
    shuffle(rgb_colors)
    splits = partition(rgb_colors, 4)
    averages = []
    for split in splits:
        avg = [sum(c) / len(c) for c in zip(*split)]
        avg = tuple(avg)
        averages.append(avg)
    averages = [rgb_to_hex(avg) for avg in averages]
    return averages


def random_images(imgs):
    from random import sample
    ids = imgs.distinct('_id')
    selected = choice(ids, 4)
    return list(imgs.find({'_id':{'$in':selected}}))


def average(top_colors):
    colors = [compute_rgb(code) for code in top_colors]
    avg = [sum(c) / len(c) for c in zip(*colors)]
    avg = rgb_to_hex(tuple(avg))
    return avg


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

    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    colour = ''.join(chr(c) for c in peak).encode('hex')

    # HEX Codes
    return ([''.join(chr(c) for c in code).encode('hex') for code in codes], colour)


def compute_closest(hex_code):
    '''L2 norm.'''

    def compute_norm(c1, c2):
        a = np.array(c1)
        b = np.array(c2)
        return norm(a-b)

    rgb = compute_rgb(hex_code)
    c = compute_rgb(TARGETS[0])

    similiar = compute_norm(rgb, c)
    index = 0

    for i in range(1, len(TARGETS)):
        c = compute_rgb(TARGETS[i])
        if compute_norm(rgb, c) < similiar:  # The smaller, the more similar
            similiar = compute_norm(rgb, c)
            index = i
    return TARGETS[index]


def compute_confidence(conf_dict, hex_codes):
    updated = {key: False for key in conf_dict.keys()}

    for code in hex_codes:
        if code not in conf_dict:
            conf_dict[code] = 0.5
        else:
            updated[code] = True
            conf_dict[code] *= 1.5

    not_updated = [key for key in updated.keys() if not updated[key]]
    for code in not_updated:
        conf_dict[code] *= 0.5

    factor = 1.0 / sum(conf_dict.itervalues())
    for k in conf_dict:
        conf_dict[k] = conf_dict[k] * factor
    return conf_dict


def compute_top_colors(conf_dict):
    codes = sorted(conf_dict.keys(), key=conf_dict.get, reverse=True)[:4]
    return codes


def compute_conf_img_similarity(conf_dict, img):
    def compute_norm(c1, c2):
        a = np.array(c1)
        b = np.array(c2)
        return norm(a-b)
    codes = compute_top_colors(conf_dict)
    similarity = 0.
    for i in range(len(codes)):
        try:
            code = compute_rgb(codes[i])
            color = compute_rgb(img['top_colors'][i])
            similarity += (compute_norm(code, color)) * conf_dict[codes[i]]
        except:
            continue
    return similarity
