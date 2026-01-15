from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    # per-serving macros stored for speed
    kcal = models.FloatField()
    protein = models.FloatField()
    carb = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name

class RecipeItem(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingr = models.CharField(max_length=60)  # must match CSV class
    grams = models.FloatField()