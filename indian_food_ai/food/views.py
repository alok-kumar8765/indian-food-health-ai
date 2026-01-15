from rest_framework.views import APIView
from rest_framework.response import Response
import base64, cv2, numpy as np
from food.ml import FoodModel
from food.portion import grams_per_box
from django.shortcuts import render
model = FoodModel()



def home(request):
    return render(request, 'food/home.html')

class PredictAPI(APIView):
    def post(self, request):
        img_bytes = base64.b64decode(request.data['image'])
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)[...,::-1]
        boxes, names = model.predict(img)
        grams = [grams_per_box(b, img.shape) for b in boxes]
        macros = model.macros(names, grams)
        return Response({'objects': [{'name': n, 'grams': round(g, 1)}
                                     for n, g in zip(names, grams)],
                         'macros': macros})