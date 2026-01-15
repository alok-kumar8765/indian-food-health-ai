PLATE_DIAM_CM = 25
PLATE_DIAM_PIX = 350
CM2_PER_PIX = (PLATE_DIAM_CM/PLATE_DIAM_PIX)**2
DENSITY = 0.85

def grams_per_box(box, img_shape):
    h = box[3]-box[1]; w = box[2]-box[0]
    area_cm2 = w*h*CM2_PER_PIX
    return area_cm2 * DENSITY * 1.1