from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FoodDiary(models.Model):
    """飲食紀錄日記"""

    MEAL_TYPE_CHOICES = [
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
        ('snack', '宵夜'),
        ('other', '其他'),
    ]

    # 食物資訊
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_diaries', verbose_name='使用者')
    food_name = models.CharField(verbose_name='食物名稱')
    food_image = models.ImageField(upload_to='food_photos/%Y/%m/%d/', blank=True, null=True, verbose_name='食物圖片')

    # 營養和份量資訊
    quantity =  models.DecimalField(verbose_name='份量', max_digits=6, decimal_places=2, help_text='請輸入食物份量，單位為1')
    quantity_unit = models.CharField(verbose_name='單位', max_length=20, default='g', help_text='克(g)或毫升(ml)')
    calories = models.IntegerField(verbose_name='卡路里(kcal)', blank=True, null=True)

    # 進食時間
    meal_type = models.CharField(verbose_name='進食時段', max_length=20, choices=MEAL_TYPE_CHOICES)
    time_end = models.DateTimeField(verbose_name='進食時間')
    remark = models.TextField(verbose_name='備註', blank=True, help_text='備註')

    created_at = models.DateTimeField(verbose_name='建立時間', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新時間', auto_now=True)

    class Meta:
        db_table = 'diary_food_diary'
        ordering = ['-created_at']
        verbose_name  = '飲食紀錄日記'
        verbose_name_plural = '飲食紀錄日記'
        indexes = [
            models.Index(fields=['user', '-time_end']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"{self.food_name} - {self.time_end.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_meal_type_display_cn(self):
        """獲得中文顯示"""
        return dict(self.MEAL_TYPE_CHOICES).get(self.meal_type, '其他')
    
class NutritionGoal(models.Model):
    """營養目標"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutrition_goal', verbose_name='使用者')
    daily_calorie_goal = models.IntegerField(verbose_name='每日卡路里目標', default=2000)
    created_at = models.DateTimeField(verbose_name='建立時間', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新時間', auto_now=True)

    class Meta:
        db_table = 'diary_nutrition_goal'
        verbose_name = '營養目標'
        verbose_name_plural = '營養目標'

    def __str__(self):
        return f"{self.user.username} - {self.daily_calorie_goal} kcal/day"

