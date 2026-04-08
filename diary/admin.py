from django.contrib import admin
from .models import FoodDiary, NutritionGoal



# 註冊model到admin後台管理
admin.site.register(FoodDiary)
admin.site.register(NutritionGoal)
