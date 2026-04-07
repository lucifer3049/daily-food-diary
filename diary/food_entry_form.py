from django import forms
from django.utils import timezone
from .food_diary_models import FoodEntry


class FoodEntryForm(forms.ModelForm):
    """飲食紀錄表單"""

    eaten_time = forms.DateTimeField(label='進食時間', widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), initial=timezone.now)

    food_image = forms.ImageField(label='食物圖片', required=False, widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}), help_text='請上傳食物圖片，支持jpg、png等格式')

    class Meta:
        model = FoodEntry
        fields = ['food_name', 'food_image', 'quantity', 'quantity_unit', 'calories', 'meal_type', 'eaten_time', 'remark']

        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入食物名稱', 'maxlength': 100}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '請輸入食物份量', 'step': '0.01', 'min': '0'}),
            'quantity_unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入單位，如g或ml', 'list': 'quantity-units'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '請輸入卡路里', 'min': '0'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '請輸入備註', 'rows': 3}),
        }

        labels = {
            'food_name': '食物名稱',
            'food_image': '食物圖片',
            'quantity': '份量',
            'quantity_unit': '單位',
            'calories': '卡路里(kcal)',
            'meal_type': '進食時段',
            'eaten_time': '進食時間',
            'remark': '備註',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.initial.get('eaten_time'):
            self.fields['eaten_time'].initial = timezone.now()

    def clean(self):
        cleaned_data = super().clean()
        food_name = cleaned_data.get('food_name')
        food_image = cleaned_data.get('food_image')

        if not food_name and not food_image:
            raise forms.ValidationError('請輸入食物名稱或食物圖片')
        
        return cleaned_data