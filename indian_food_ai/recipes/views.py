from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Profile
from recipes.models import Recipe, RecipeItem

def daily_kcal(profile):
    bmr = 10*profile.weight + 6.25*profile.height - 5*30 + 5
    activity = 1.55
    mult = {'M': 1, 'C': 0.8, 'B': 1.2}[profile.goal]
    return int(bmr*activity*mult)

class SuggestAPI(APIView):
    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        detected = set(request.data['detected'])  # ['potato','atta']
        meal_kcal = daily_kcal(profile) / 3
        # recipes that contain at least one detected ingredient
        rec_ids = RecipeItem.objects.filter(
            ingr__in=detected).values_list('recipe', flat=True).distinct()
        recipes = Recipe.objects.filter(id__in=rec_ids)
        out = []
        for r in recipes:
            servings = max(1, round(meal_kcal / r.kcal))
            out.append({'name': r.name,
                        'servings': servings,
                        'macros': {'kcal': round(r.kcal*servings, 1),
                                   'protein': round(r.protein*servings, 1),
                                   'carb': round(r.carb*servings, 1),
                                   'fat': round(r.fat*servings, 1)}})
        return Response({'recipes': out})