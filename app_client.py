import requests
import json
from config import MEAL_DB_BASE_URL

class TheMealDBClient:
    """Клиент для работы с TheMealDB API"""
    
    def __init__(self):
        self.base_url = MEAL_DB_BASE_URL
    
    def search_meal_by_name(self, name):
        """Поиск рецепта по названию"""
        try:
            url = f"{self.base_url}/search.php"
            params = {"s": name}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("meals", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при поиске по названию: {e}")
            return []
    
    def get_random_meal(self):
        """Получить случайный рецепт"""
        try:
            url = f"{self.base_url}/random.php"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            meals = data.get("meals", [])
            return meals[0] if meals else None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении случайного рецепта: {e}")
            return None
    
    def search_by_ingredient(self, ingredient):
        """Поиск рецептов по ингредиенту"""
        try:
            url = f"{self.base_url}/filter.php"
            params = {"i": ingredient}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("meals", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при поиске по ингредиенту: {e}")
            return []
    
    def get_meal_details(self, meal_id):
        """Получить детальную информацию о рецепте по ID"""
        try:
            url = f"{self.base_url}/lookup.php"
            params = {"i": meal_id}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            meals = data.get("meals", [])
            return meals[0] if meals else None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении деталей рецепта: {e}")
            return None
    
    def get_categories(self):
        """Получить список категорий блюд"""
        try:
            url = f"{self.base_url}/categories.php"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("categories", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении категорий: {e}")
            return []
    
    def filter_by_category(self, category):
        """Поиск рецептов по категории"""
        try:
            url = f"{self.base_url}/filter.php"
            params = {"c": category}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("meals", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при поиске по категории: {e}")
            return []

class RecipeFormatter:
    """Класс для форматирования рецептов"""
    
    @staticmethod
    def format_recipe_card(meal):
        """Форматирует рецепт для отображения в виде карточки"""
        if not meal:
            return "❌ Рецепт не найден"
        
        # Основная информация
        name = meal.get('strMeal', 'Неизвестное блюдо')
        category = meal.get('strCategory', 'Без категории')
        area = meal.get('strArea', 'Неизвестная кухня')
        image = meal.get('strMealThumb', '')
        video_url = meal.get('strYoutube', '')
        
        # Формируем текст
        text = f"🍽️ **{name}**\n\n"
        text += f"📂 Категория: {category}\n"
        text += f"🌍 Кухня: {area}\n\n"
        
        # Ингредиенты
        ingredients = RecipeFormatter.extract_ingredients(meal)
        if ingredients:
            text += "📋 **Ингредиенты:**\n"
            for ingredient in ingredients[:8]:  # Показываем первые 8 ингредиентов
                text += f"• {ingredient}\n"
            
            if len(ingredients) > 8:
                text += f"• ... и еще {len(ingredients) - 8} ингредиентов\n"
        
        # Видеорецепт (только если есть)
        if video_url and video_url.strip():
            text += "\n🎥 **Видеорецепт:**\n"
            text += f"📺 {video_url}"
        
        return text, image
    
    @staticmethod
    def format_full_recipe(meal):
        """Форматирует полный рецепт с инструкциями"""
        if not meal:
            return "❌ Рецепт не найден"
        
        name = meal.get('strMeal', 'Неизвестное блюдо')
        category = meal.get('strCategory', 'Без категории')
        area = meal.get('strArea', 'Неизвестная кухня')
        instructions = meal.get('strInstructions', 'Инструкции недоступны')
        video_url = meal.get('strYoutube', '')
        
        text = f"🍽️ **{name}**\n\n"
        text += f"📂 Категория: {category}\n"
        text += f"🌍 Кухня: {area}\n\n"
        
        # Ингредиенты
        ingredients = RecipeFormatter.extract_ingredients(meal)
        if ingredients:
            text += "📋 **Ингредиенты:**\n"
            for ingredient in ingredients:
                text += f"• {ingredient}\n"
            text += "\n"
        
        # Инструкции (ограничиваем длину)
        text += "👨‍🍳 **Приготовление:**\n"
        if len(instructions) > 800:
            text += instructions[:800] + "...\n\n"
            text += "📖 *Полные инструкции слишком длинные для отображения*"
        else:
            text += instructions
        
        # Видеорецепт
        if video_url and video_url.strip():
            text += "\n\n🎥 **Видеорецепт:**\n"
            text += f"📺 {video_url}"
        
        return text
    
    @staticmethod
    def extract_ingredients(meal):
        """Извлекает список ингредиентов из рецепта"""
        ingredients = []
        
        for i in range(1, 21):  # API возвращает до 20 ингредиентов
            ingredient_key = f'strIngredient{i}'
            measure_key = f'strMeasure{i}'
            
            ingredient = meal.get(ingredient_key, '')
            measure = meal.get(measure_key, '')
            
            # Проверяем, что значения не None и не пустые
            if ingredient and ingredient.strip():
                ingredient = ingredient.strip()
                if measure and measure.strip():
                    measure = measure.strip()
                    ingredients.append(f"{measure} {ingredient}")
                else:
                    ingredients.append(ingredient)
        
        return ingredients
    
    @staticmethod
    def format_recipe_list(meals, title="🔍 Результаты поиска"):
        """Форматирует список рецептов"""
        if not meals:
            return "❌ Рецепты не найдены"
        
        text = f"{title}\n\n"
        
        for i, meal in enumerate(meals[:10], 1):  # Показываем до 10 рецептов
            name = meal.get('strMeal', 'Неизвестное блюдо')
            category = meal.get('strCategory', '')
            
            text += f"{i}. **{name}**"
            if category:
                text += f" ({category})"
            text += "\n"
        
        if len(meals) > 10:
            text += f"\n... и еще {len(meals) - 10} рецептов"
        
        return text

