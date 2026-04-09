from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q, Sum
from datetime import timedelta, datetime
from django.core.paginator import Paginator
from ..models import FoodDiary, NutritionGoal
from ..forms import FoodEntryForm

# FBV版本的CRUD功能，可以自定義更多的邏輯和功能
@login_required
def food_entry_create(request):
    """建立新的食物日誌"""
    """使用者須登入，才可以進入這個建立食物日誌的地方"""
    if request.method == 'POST':
        form = FoodEntryForm(request.POST, request.FILES)
        # 驗證表單
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save() # 儲存資料
            messages.success(request, '食物日誌建立成功!')
            return redirect('diary:entry_detail', pk=entry.pk)
    else:
        form = FoodEntryForm()
    
    context = {
        'form': form,
        'title': '新增食物日誌',
        'is_create': True,
    }

    return render(request, 'diary/food_entry_form.html', context) 

@login_required
def food_entry_edit(request, pk):
    """編輯食物日誌"""
    # 如果找不到回到404頁面
    # user=request.user 只找自己的資料
    entry = get_object_or_404(FoodDiary, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FoodEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, '食物日誌更新成功!')
            return redirect('diary:entry_detail', pk=entry.pk)
    else:
        form = FoodEntryForm(instance=entry)

    context = {
        'form': form,
        'entry': entry,
        'title': '編輯食物日誌',
        'is_create': False,
    }
    return render(request, 'diary/food_entry_form.html', context)

@login_required
def food_entry_delete(request, pk):
    """刪除食物日誌"""
    entry = get_object_or_404(FoodDiary, pk=pk, user=request.user)

    if request.method == 'POST':
        entry.delete()
        messages.success(request, '食物日誌刪除成功!')
        return render(request, 'diary/entry_list.html', context)
    
    context = {
        'entry': entry,
    }

    return render(request, 'diary/food_entry_delete.html', context)

@login_required
def food_entry_list(request):
    """食物日誌列表"""
    # 取得該使用者的所有食物日誌
    entries = FoodDiary.objects.filter(user=request.user)

    # 取得查詢條件前端URL來的參數
    search_query = request.GET.get('search', '')
    meal_type = request.GET.get('meal_type', '')
    date_filter = request.GET.get('date', '')

    # 根據查詢條的關鍵字搜尋功能
    if search_query:
        entries = entries.filter(Q(food_name__icontains=search_query) | Q(notes__icontains=search_query))
    
    if meal_type:
        entries = entries.filter(meal_type=meal_type)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            entries = entries.filter(eaten_time__date=filter_date)
        except ValueError:
            pass

    # 分頁功能
    paginator = Paginator(entries, 10) # 每頁顯示10筆資料
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 計算總熱量
    today = timezone.now().date()
    today_entries = entries.filter(eaten_time__date=today)
    today_calories = today_entries.aggregate(total=Sum('calories'))['total'] or 0

  
    context = {
        'entries': page_obj, # 取得分頁
        'today_entries': today_entries,
        'today_calories': today_calories,
        'search_query': search_query,
        'meal_type': meal_type,
        'date_filter': date_filter,
    }

    return render(request, 'diary/food_entry_list.html', context)

@login_required
def food_entry_detail(request, pk):
    """食物日誌明細"""

    entry = get_object_or_404(FoodDiary, pk=pk, user=request.user)
    context = {
        'entry': entry,
    }

    return render(request, 'diary/food_entry_detail.html', context)

@login_required
def daily_summary(request, date_str=None):
    """每日摘要"""

    #　取的該日期的資料
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.now().date()
    else:
        date = timezone.now().date()

    # 取得日期的所有食物日誌資料
    entries = FoodDiary.objects.filter(user=request.user, eaten_time__date=date).order_by('eaten_time')

    # 計算總熱量
    total_calories = entries.aggregate(total=Sum('calories'))['total'] or 0

    # 取得使用者的營養目標，沒有的話預設2000大卡
    try:
        nutrition_goal = request.user.nutrition_goal
    except NutritionGoal.DoesNotExist:
        nutrition_goal = NutritionGoal.objects.create(user=request.user, daily_calorie_goal=2000)

    # 計算剩餘熱量
    remaining_calories = nutrition_goal.daily_calorie_goal - total_calories

    # 根據早 午 晚 點心的進食時間分類
    breakfast = entries.filter(meal_type='breakfast')
    lunch = entries.filter(meal_type='lunch')
    dinner = entries.filter(meal_type='dinner')
    snack = entries.filter(meal_type='snack')

    context = {
        'date': date,
        'entries': entries,
        'total_calories': total_calories,
        'nutrition_calories': nutrition_goal,
        'remaining_calories': remaining_calories,
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snack': snack,
    }

    return render(request, 'diary/daily_summary.html', context)

# CBV版本的CRUD功能，使用Django內建的類別檢視，簡化程式碼，不靈活
class FoodEntryListView(LoginRequiredMixin, ListView):
    """食物日至列表檢視"""

    model = FoodDiary
    template_name = 'diary/food_entry_list.html'
    context_object_name = 'entries'
    paginate_by = 20

    def get_queryset(self):
        return FoodDiary.objects.filter(user=self.request.user)
    
class FoodEntryDetailView(LoginRequiredMixin, DetailView):
    """食物日至明細檢視"""
    model = FoodDiary
    template_name = 'diary/food_entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return FoodDiary.objects.filter(user=self.request.user)
    
class FoodEntryCreateView(LoginRequiredMixin, CreateView):
    """建立食物日誌檢視"""

    model = FoodDiary
    form_class = FoodEntryForm
    template_name = 'diary/food_entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '食物日誌建立成功!')
        return super().form_valid(form)
    
class FoodEntryUpdateView(LoginRequiredMixin, UpdateView):
    """更新食物日誌檢視"""

    model = FoodDiary
    form_class = FoodEntryForm
    template_name = 'diary/food_entry_form.html'
    success_url = reverse_lazy('diary:entry_list')

    def get_queryset(self):
        return FoodDiary.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, '食物日誌更新成功!')
        return super().form_valid(form)
    
class FoodEntryDeleteView(LoginRequiredMixin, DeleteView):
    """刪除食物日至檢視"""

    model = FoodDiary
    template_name = 'diary/food_entry_delete.html'
    success_url = reverse_lazy('diary:entry_list')

    def get_queryset(self):
        return FoodDiary.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '食物日誌刪除成功!')
        return super().delete(request, *args, **kwargs)
