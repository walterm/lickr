from PIL import Image
import scipy
import scipy.misc
import scipy.cluster


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

    # HEX Codes
    return [''.join(chr(c) for c in code).encode('hex') for code in codes]
