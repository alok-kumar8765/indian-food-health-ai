# food/ml.py
import torch
from pathlib import Path
import pandas as pd
from ultralytics import YOLO
import logging
logger = logging.getLogger(__name__)

# safe, local patch – no recursion
orig_load = torch.load
torch.load = lambda *a, **k: orig_load(*a, **{**k, "weights_only": False})

CSV = Path(__file__).resolve().parent.parent / 'calories.csv'
CAL = pd.read_csv(CSV).set_index('class')

class FoodModel:
    def __init__(self, weights='weights/yolov8n.pt'):
        self.model = YOLO(weights)   # now uses the patched loader once


    def predict(self, image_rgb):
        res = self.model(image_rgb, conf=0.25)[0]
        boxes = res.boxes.xyxy.cpu().numpy()
        names = [self.model.names[int(c)] for c in res.boxes.cls.cpu().numpy()]
        return boxes, names

    # def macros(self, names, grams):
    #     # 1. drop anything not in the calorie table
    #     mask = [n in CAL.index for n in names]
    #     names, grams = [n for n, m in zip(names, mask) if m], \
    #                 [g for g, m in zip(grams, mask) if m]
    #     if not names:          # nothing recognised
    #         return {'kcal': 0, 'protein': 0, 'carb': 0, 'fat': 0}

    #     df = CAL.loc[names]
    #     kcal = (df.kcal_per_100g * grams / 100).sum()
    #     p    = (df.protein    * grams / 100).sum()
    #     c    = (df.carb       * grams / 100).sum()
    #     f    = (df.fat        * grams / 100).sum()
    #     return {'kcal': round(kcal, 1), 'protein': round(p, 1),
    #             'carb': round(c, 1), 'fat': round(f, 1)}
    def macros(self, names, grams):
        # keep only items that exist in the calorie table
        mask = [n in CAL.index for n in names]
        dropped = [n for n, m in zip(names, mask) if not m]
        if dropped:
            logger.info("No calorie data for %s", dropped)   # <- log once per call

        names, grams = [n for n, m in zip(names, mask) if m], \
                       [g for g, m in zip(grams, mask) if m]
        if not names:          # nothing recognised
            return {'kcal': 0, 'protein': 0, 'carb': 0, 'fat': 0}

        df = CAL.loc[names]
        kcal = (df.kcal_per_100g * grams / 100).sum()
        p    = (df.protein    * grams / 100).sum()
        c    = (df.carb       * grams / 100).sum()
        f    = (df.fat        * grams / 100).sum()
        return {'kcal': round(kcal, 1), 'protein': round(p, 1),
                'carb': round(c, 1), 'fat': round(f, 1)}