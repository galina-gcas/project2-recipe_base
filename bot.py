import telebot
from telebot import types
import os
from config import BOT_TOKEN
from api_client import TheMealDBClient, RecipeFormatter
from database import db

# Инициализация бота и API клиента
bot = telebot.TeleBot(BOT_TOKEN)
meal_api = TheMealDBClient()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start - показывает приветствие и главное меню"""
    welcome_text = (
        "🍽️ Добро пожаловать в Recipe Bot!\n\n"
        "Я помогу вам найти вкусные рецепты блюд со всего мира "
        "и сохранить понравившиеся в избранное.\n\n"
        "Выберите действие:"
    )
    
    # Создаем главное меню
    main_menu = create_main_menu()
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu)


def create_main_menu():
    """Создает главное меню с основными кнопками"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Кнопка поиска рецептов
    search_btn = types.InlineKeyboardButton(
        "🔍 Поиск рецептов", 
        callback_data="search_recipes"
    )
    
    # Кнопка избранных рецептов
    favorites_btn = types.InlineKeyboardButton(
        "⭐ Мои рецепты", 
        callback_data="my_recipes"
    )
    
    markup.add(search_btn)
    markup.add(favorites_btn)
    
    return markup


# Обработчик inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    """Обработчик нажатий на inline кнопки"""
    chat_id = call.message.chat.id
    
    if call.data == "search_recipes":
        handle_search_recipes(chat_id)
    elif call.data == "my_recipes":
        handle_my_recipes(chat_id)
    elif call.data == "back_to_main":
        send_main_menu(chat_id)
    elif call.data == "search_random":
        handle_random_recipe(chat_id)
    elif call.data == "search_by_name":
        handle_search_by_name_start(chat_id)
    elif call.data == "search_by_ingredient":
        handle_search_by_ingredient_start(chat_id)
    elif call.data == "search_by_category":
        handle_search_by_category_start(chat_id)
    elif call.data.startswith("save_recipe_"):
        recipe_id = call.data.replace("save_recipe_", "")
        handle_save_recipe(chat_id, recipe_id)
    elif call.data.startswith("view_recipe_"):
        recipe_id = call.data.replace("view_recipe_", "")
        handle_view_recipe(chat_id, recipe_id)
    elif call.data.startswith("recipe_details_"):
        recipe_id = call.data.replace("recipe_details_", "")
        handle_recipe_details(chat_id, recipe_id)
    elif call.data.startswith("category_"):
        category = call.data.replace("category_", "")
        handle_category_search(chat_id, category)
    elif call.data.startswith("fav_details_"):
        recipe_id = call.data.replace("fav_details_", "")
        handle_favorite_details(chat_id, recipe_id)
    elif call.data.startswith("remove_fav_"):
        recipe_id = call.data.replace("remove_fav_", "")
        handle_remove_favorite(chat_id, recipe_id)
    elif call.data.startswith("rate_recipe_"):
        recipe_id = call.data.replace("rate_recipe_", "")
        handle_rate_recipe(chat_id, recipe_id)
    elif call.data == "view_list":
        user_view_preferences[chat_id] = 'list'
        handle_my_recipes(chat_id)
    elif call.data == "view_cards":
        user_view_preferences[chat_id] = 'cards'
        handle_my_recipes(chat_id)
    elif call.data.startswith("set_rating_"):
        # Формат: set_rating_recipe_id_rating
        parts = call.data.split("_")
        if len(parts) >= 4:
            recipe_id = parts[2]
            rating = int(parts[3])
            handle_set_rating(chat_id, recipe_id, rating)
    elif call.data == "show_more_favorites":
        handle_show_more_favorites(chat_id)
    elif call.data == "back_to_main":
        send_main_menu(chat_id)
    
    # Убираем "часики" с кнопки
    bot.answer_callback_query(call.id)


def send_main_menu(chat_id):
    """Отправляет главное меню"""
    menu_text = "🍽️ Главное меню\n\nВыберите действие:"
    main_menu = create_main_menu()
    bot.send_message(chat_id, menu_text, reply_markup=main_menu)


def handle_search_recipes(chat_id):
    """Обработчик поиска рецептов - показывает меню типов поиска"""
    search_text = (
        "🔍 Поиск рецептов\n\n"
        "Выберите способ поиска:"
    )
    
    # Создаем меню типов поиска
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Кнопки типов поиска
    random_btn = types.InlineKeyboardButton("🎲 Случайный рецепт", callback_data="search_random")
    name_btn = types.InlineKeyboardButton("📝 Поиск по названию", callback_data="search_by_name")
    ingredient_btn = types.InlineKeyboardButton("🥕 Поиск по ингредиенту", callback_data="search_by_ingredient")
    category_btn = types.InlineKeyboardButton("📂 Поиск по категории", callback_data="search_by_category")
    
    # Кнопка возврата
    back_btn = types.InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")
    
    markup.add(random_btn)
    markup.add(name_btn)
    markup.add(ingredient_btn)
    markup.add(category_btn)
    markup.add(back_btn)
    
    bot.send_message(chat_id, search_text, reply_markup=markup)


def handle_my_recipes(chat_id):
    """Обработчик просмотра избранных рецептов"""
    favorites = db.get_user_favorites(chat_id, limit=20)
    
    if not favorites:
        favorites_text = (
            "⭐ Мои рецепты\n\n"
            "Ваш список избранных рецептов пуст.\n"
            "Найдите интересные рецепты через поиск "
            "и добавьте их в избранное!"
        )
        
        # Кнопка возврата в главное меню
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton("◀️ Назад в меню", callback_data="back_to_main")
        markup.add(back_btn)
        
        bot.send_message(chat_id, favorites_text, reply_markup=markup)
        return
    
    # Получаем предпочтение отображения пользователя
    view_mode = user_view_preferences.get(chat_id, 'cards')  # По умолчанию карточки
    
    # Отправляем заголовок с кнопками переключения
    total_count = len(favorites)
    header_text = f"⭐ Мои рецепты ({total_count})\n\n"
    if view_mode == 'cards':
        header_text += "📱 Режим: Карточки с фото"
    else:
        header_text += "📋 Режим: Список"
    
    # Отправляем только заголовок без кнопок
    bot.send_message(chat_id, header_text)
    
    # Показываем рецепты в выбранном режиме
    if view_mode == 'cards':
        show_favorites_as_cards(chat_id, favorites[:10])
    else:
        show_favorites_as_list(chat_id, favorites[:10])
    
    # Информация о результатах с кнопками навигации
    info_markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Кнопки переключения вида
    if view_mode == 'cards':
        list_btn = types.InlineKeyboardButton("📋 Список", callback_data="view_list")
        info_markup.add(list_btn)
    else:
        cards_btn = types.InlineKeyboardButton("📱 Карточки", callback_data="view_cards")
        info_markup.add(cards_btn)
    
    # Кнопка показа больше рецептов (если есть)
    if total_count > 10:
        more_btn = types.InlineKeyboardButton(
            f"📋 Показано {min(10, total_count)} из {total_count}", 
            callback_data="show_more_favorites"
        )
        info_markup.add(more_btn)
    
    # Кнопка возврата в главное меню
    back_btn = types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    info_markup.add(back_btn)
    
    bot.send_message(chat_id, "✅ Все избранные рецепты", reply_markup=info_markup)


def show_favorites_as_cards(chat_id, favorites):
    """Показать избранные рецепты в виде карточек с фото"""
    for favorite in favorites:
        recipe_data = favorite['recipe_data']
        if recipe_data:
            text, image_url = RecipeFormatter.format_recipe_card(recipe_data)
            
            # Добавляем рейтинг и дату сохранения
            rating = favorite.get('rating', 0)
            saved_date = favorite['saved_at'][:10]
            
            # Формируем звезды рейтинга
            stars = "⭐" * rating + "☆" * (5 - rating) if rating > 0 else "☆☆☆☆☆"
            text += f"\n⭐ Рейтинг: {stars} ({rating}/5)"
            text += f"\n📅 Сохранено: {saved_date}"
            
            # Создаем кнопки для избранного рецепта
            markup = types.InlineKeyboardMarkup(row_width=2)
            details_btn = types.InlineKeyboardButton(
                "📖 Подробнее", 
                callback_data=f"fav_details_{favorite['recipe_id']}"
            )
            rate_btn = types.InlineKeyboardButton(
                "⭐ Оценить", 
                callback_data=f"rate_recipe_{favorite['recipe_id']}"
            )
            remove_btn = types.InlineKeyboardButton(
                "🗑️ Удалить", 
                callback_data=f"remove_fav_{favorite['recipe_id']}"
            )
            
            markup.add(details_btn, rate_btn)
            markup.add(remove_btn)
            
            try:
                if image_url:
                    bot.send_photo(chat_id, image_url, caption=text, reply_markup=markup, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
            except Exception as e:
                print(f"Ошибка отправки избранного рецепта: {e}")
                bot.send_message(chat_id, text, reply_markup=markup)

def show_favorites_as_list(chat_id, favorites):
    """Показать избранные рецепты в виде списка"""
    list_text = "📋 **Ваши избранные рецепты:**\n\n"
    
    for i, favorite in enumerate(favorites, 1):
        recipe_name = favorite['recipe_name']
        category = favorite.get('category', '')
        area = favorite.get('area', '')
        rating = favorite.get('rating', 0)
        saved_date = favorite['saved_at'][:10]
        
        # Формируем звезды рейтинга
        stars = "⭐" * rating + "☆" * (5 - rating) if rating > 0 else "☆☆☆☆☆"
        
        list_text += f"{i}. **{recipe_name}**\n"
        if category:
            list_text += f"   📂 {category}"
        if area:
            list_text += f" | 🌍 {area}"
        list_text += f"\n   ⭐ {stars} ({rating}/5)"
        list_text += f"\n   📅 {saved_date}\n"
        
        # Добавляем кнопки управления прямо под каждым рецептом
        recipe_id = favorite['recipe_id']
        current_rating = favorite.get('rating', 0)
        
        # Создаем отдельную клавиатуру для каждого рецепта
        recipe_markup = types.InlineKeyboardMarkup(row_width=3)
        
        details_btn = types.InlineKeyboardButton(
            "📖", 
            callback_data=f"fav_details_{recipe_id}"
        )
        rate_btn = types.InlineKeyboardButton(
            f"⭐ {current_rating}/5", 
            callback_data=f"rate_recipe_{recipe_id}"
        )
        remove_btn = types.InlineKeyboardButton(
            "🗑️", 
            callback_data=f"remove_fav_{recipe_id}"
        )
        
        recipe_markup.add(details_btn, rate_btn, remove_btn)
        
        # Отправляем каждый рецепт с его кнопками отдельным сообщением
        bot.send_message(chat_id, list_text, reply_markup=recipe_markup, parse_mode='Markdown')
        
        # Очищаем текст для следующего рецепта
        list_text = ""
        
        # Добавляем разделитель между рецептами
        if i < len(favorites):
            bot.send_message(chat_id, "─" * 40)

def handle_save_recipe(chat_id, recipe_id):
    """Обработчик сохранения рецепта в избранное"""
    # Проверяем, не добавлен ли уже рецепт в избранное
    if db.is_favorite(chat_id, recipe_id):
        bot.send_message(
            chat_id,
            "⚠️ Этот рецепт уже есть в вашем избранном!\n\n"
            "Найти его можно в разделе 'Мои рецепты'."
        )
        return
    
    # Получаем полную информацию о рецепте из API
    meal_data = meal_api.get_meal_details(recipe_id)
    
    if meal_data:
        # Сохраняем в базу данных
        if db.add_favorite(chat_id, meal_data):
            recipe_name = meal_data.get('strMeal', 'Неизвестное блюдо')
            favorites_count = db.get_favorites_count(chat_id)
            
            bot.send_message(
                chat_id, 
                f"✅ Рецепт '{recipe_name}' добавлен в избранное!\n\n"
                f"📊 У вас сохранено рецептов: {favorites_count}\n"
                f"💡 Найти все избранные можно в разделе 'Мои рецепты'."
            )
        else:
            bot.send_message(
                chat_id,
                "❌ Не удалось сохранить рецепт. Попробуйте позже."
            )
    else:
        bot.send_message(
            chat_id,
            "❌ Не удалось получить данные рецепта. Попробуйте позже."
        )


def handle_view_recipe(chat_id, recipe_id):
    """Обработчик просмотра детальной информации о рецепте"""
    # TODO: Здесь будет логика получения полной информации о рецепте из API
    
    bot.send_message(
        chat_id,
        "📖 Просмотр рецепта...\n\n"
        "Функция просмотра детальной информации о рецепте "
        "будет реализована позже."
    )


# Словари для хранения состояний и настроек пользователей
user_states = {}
user_view_preferences = {}  # 'list' или 'cards'

def handle_random_recipe(chat_id):
    """Обработчик получения случайного рецепта"""
    bot.send_message(chat_id, "🎲 Ищу случайный рецепт...")
    
    meal = meal_api.get_random_meal()
    if meal:
        text, image_url = RecipeFormatter.format_recipe_card(meal)
        
        # Создаем кнопки для рецепта
        markup = types.InlineKeyboardMarkup(row_width=2)
        details_btn = types.InlineKeyboardButton("📖 Подробнее", callback_data=f"recipe_details_{meal['idMeal']}")
        save_btn = types.InlineKeyboardButton("⭐ Сохранить", callback_data=f"save_recipe_{meal['idMeal']}")
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        
        markup.add(details_btn, save_btn)
        markup.add(back_btn, menu_btn)
        
        if image_url:
            bot.send_photo(chat_id, image_url, caption=text, reply_markup=markup, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        bot.send_message(chat_id, "❌ Не удалось получить случайный рецепт. Попробуйте позже.", reply_markup=markup)

def handle_search_by_name_start(chat_id):
    """Начало поиска по названию"""
    user_states[chat_id] = "waiting_for_name"
    
    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("◀️ Отмена", callback_data="search_recipes")
    markup.add(back_btn)
    
    bot.send_message(
        chat_id, 
        "📝 Введите название блюда для поиска:\n\n"
        "Например: *Chicken*, *Pasta*, *Pizza*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def handle_search_by_ingredient_start(chat_id):
    """Начало поиска по ингредиенту"""
    user_states[chat_id] = "waiting_for_ingredient"
    
    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("◀️ Отмена", callback_data="search_recipes")
    markup.add(back_btn)
    
    bot.send_message(
        chat_id,
        "🥕 Введите название ингредиента:\n\n"
        "Например: *chicken*, *tomato*, *cheese*",
        reply_markup=markup,
        parse_mode='Markdown'
    )

def handle_search_by_category_start(chat_id):
    """Показ категорий для выбора"""
    bot.send_message(chat_id, "📂 Загружаю категории...")
    
    categories = meal_api.get_categories()
    if categories:
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Добавляем популярные категории
        popular_categories = ['Beef', 'Chicken', 'Dessert', 'Pasta', 'Seafood', 'Vegetarian']
        
        for category in categories[:12]:  # Показываем первые 12 категорий
            category_name = category.get('strCategory', '')
            if category_name:
                btn = types.InlineKeyboardButton(
                    f"{'⭐ ' if category_name in popular_categories else ''}{category_name}",
                    callback_data=f"category_{category_name}"
                )
                markup.add(btn)
        
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        markup.add(back_btn)
        
        bot.send_message(chat_id, "📂 Выберите категорию:", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        bot.send_message(chat_id, "❌ Не удалось загрузить категории.", reply_markup=markup)

def handle_recipe_details(chat_id, recipe_id):
    """Показ детальной информации о рецепте"""
    bot.send_message(chat_id, "📖 Загружаю полный рецепт...")
    
    meal = meal_api.get_meal_details(recipe_id)
    if meal:
        text = RecipeFormatter.format_full_recipe(meal)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        save_btn = types.InlineKeyboardButton("⭐ Сохранить", callback_data=f"save_recipe_{recipe_id}")
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        
        markup.add(save_btn)
        markup.add(back_btn, menu_btn)
        
        # Отправляем длинный текст частями, если необходимо
        if len(text) > 4000:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Последняя часть
                    bot.send_message(chat_id, part, reply_markup=markup, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, part, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        bot.send_message(chat_id, "❌ Не удалось загрузить рецепт.", reply_markup=markup)

def perform_search(chat_id, query, search_type):
    """Выполняет поиск и отображает результаты"""
    bot.send_message(chat_id, f"🔍 Ищу рецепты...")
    
    meals = []
    if search_type == "name":
        meals = meal_api.search_meal_by_name(query)
    elif search_type == "ingredient":
        meals = meal_api.search_by_ingredient(query)
    
    if meals:
        # Показываем первые несколько рецептов
        for i, meal in enumerate(meals[:5]):  # Показываем первые 5
            text, image_url = RecipeFormatter.format_recipe_card(meal)
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            details_btn = types.InlineKeyboardButton("📖 Подробнее", callback_data=f"recipe_details_{meal['idMeal']}")
            save_btn = types.InlineKeyboardButton("⭐ Сохранить", callback_data=f"save_recipe_{meal['idMeal']}")
            
            markup.add(details_btn, save_btn)
            
            try:
                if image_url:
                    bot.send_photo(chat_id, image_url, caption=text, reply_markup=markup, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
            except Exception as e:
                print(f"Ошибка отправки рецепта: {e}")
                bot.send_message(chat_id, text, reply_markup=markup)
        
        # Кнопки навигации
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        
        if len(meals) > 5:
            bot.send_message(
                chat_id, 
                f"📋 Показано {min(5, len(meals))} из {len(meals)} найденных рецептов",
                reply_markup=markup
            )
        else:
            bot.send_message(chat_id, "✅ Поиск завершен", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        
        bot.send_message(
            chat_id, 
            f"❌ Рецепты по запросу '{query}' не найдены.\nПопробуйте другой запрос.",
            reply_markup=markup
        )

def handle_category_search(chat_id, category):
    """Обработчик поиска по категории"""
    bot.send_message(chat_id, f"📂 Ищу рецепты в категории {category}...")
    
    meals = meal_api.filter_by_category(category)
    if meals:
        # Показываем первые 5 рецептов из категории
        for i, meal in enumerate(meals[:5]):
            text, image_url = RecipeFormatter.format_recipe_card(meal)
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            details_btn = types.InlineKeyboardButton("📖 Подробнее", callback_data=f"recipe_details_{meal['idMeal']}")
            save_btn = types.InlineKeyboardButton("⭐ Сохранить", callback_data=f"save_recipe_{meal['idMeal']}")
            
            markup.add(details_btn, save_btn)
            
            try:
                if image_url:
                    bot.send_photo(chat_id, image_url, caption=text, reply_markup=markup, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
            except Exception as e:
                print(f"Ошибка отправки рецепта: {e}")
                bot.send_message(chat_id, text, reply_markup=markup)
        
        # Информация о результатах
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        
        if len(meals) > 5:
            bot.send_message(
                chat_id,
                f"📋 Показано 5 из {len(meals)} рецептов в категории {category}",
                reply_markup=markup
            )
        else:
            bot.send_message(chat_id, f"✅ Все рецепты в категории {category}", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ Назад к поиску", callback_data="search_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        bot.send_message(chat_id, f"❌ Рецепты в категории {category} не найдены.", reply_markup=markup)

def handle_favorite_details(chat_id, recipe_id):
    """Показ детальной информации об избранном рецепте"""
    # Сначала проверяем в избранном пользователя
    favorite_recipe = db.get_favorite_by_id(chat_id, recipe_id)
    
    if favorite_recipe:
        text = RecipeFormatter.format_full_recipe(favorite_recipe)
        
        # Добавляем информацию о рейтинге
        rating = favorite_recipe.get('rating', 0)
        stars = "⭐" * rating + "☆" * (5 - rating) if rating > 0 else "☆☆☆☆☆"
        text += f"\n\n⭐ **Рейтинг:** {stars} ({rating}/5)"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        rate_btn = types.InlineKeyboardButton("⭐ Оценить", callback_data=f"rate_recipe_{recipe_id}")
        remove_btn = types.InlineKeyboardButton("🗑️ Удалить из избранного", callback_data=f"remove_fav_{recipe_id}")
        back_btn = types.InlineKeyboardButton("◀️ К моим рецептам", callback_data="my_recipes")
        
        markup.add(rate_btn, remove_btn)
        markup.add(back_btn)
        
        # Отправляем длинный текст частями, если необходимо
        if len(text) > 4000:
            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            for i, part in enumerate(parts):
                if i == len(parts) - 1:  # Последняя часть
                    bot.send_message(chat_id, part, reply_markup=markup, parse_mode='Markdown')
                else:
                    bot.send_message(chat_id, part, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    else:
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton("◀️ К моим рецептам", callback_data="my_recipes")
        markup.add(back_btn)
        bot.send_message(chat_id, "❌ Рецепт не найден в избранном.", reply_markup=markup)

def handle_remove_favorite(chat_id, recipe_id):
    """Удаление рецепта из избранного"""
    if db.remove_favorite(chat_id, recipe_id):
        favorites_count = db.get_favorites_count(chat_id)
        bot.send_message(
            chat_id,
            f"✅ Рецепт удален из избранного!\n\n"
            f"📊 У вас осталось рецептов: {favorites_count}"
        )
        
        # Автоматически показываем обновленный список избранного
        handle_my_recipes(chat_id)
    else:
        bot.send_message(
            chat_id,
            "❌ Не удалось удалить рецепт из избранного."
        )

def handle_rate_recipe(chat_id, recipe_id):
    """Показать меню для оценки рецепта"""
    # Получаем информацию о рецепте
    favorite_recipe = db.get_favorite_by_id(chat_id, recipe_id)
    
    if not favorite_recipe:
        bot.send_message(chat_id, "❌ Рецепт не найден в избранном.")
        return
    
    recipe_name = favorite_recipe.get('strMeal', 'Неизвестное блюдо')
    current_rating = favorite_recipe.get('rating', 0)
    
    # Формируем звезды текущего рейтинга
    current_stars = "⭐" * current_rating + "☆" * (5 - current_rating) if current_rating > 0 else "☆☆☆☆☆"
    
    text = f"⭐ **Оценка рецепта:** {recipe_name}\n\n"
    text += f"Текущий рейтинг: {current_stars} ({current_rating}/5)\n\n"
    text += "Выберите новую оценку:"
    
    # Создаем кнопки рейтинга
    markup = types.InlineKeyboardMarkup(row_width=5)
    
    rating_buttons = []
    for i in range(1, 6):
        stars = "⭐" * i + "☆" * (5 - i)
        btn = types.InlineKeyboardButton(
            f"{i} {stars}", 
            callback_data=f"set_rating_{recipe_id}_{i}"
        )
        rating_buttons.append(btn)
    
    markup.add(*rating_buttons)
    
    # Кнопка отмены
    cancel_btn = types.InlineKeyboardButton("❌ Отмена", callback_data="my_recipes")
    markup.add(cancel_btn)
    
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')

def handle_set_rating(chat_id, recipe_id, rating):
    """Установить рейтинг для рецепта"""
    if db.update_rating(chat_id, recipe_id, rating):
        # Получаем обновленную информацию о рецепте
        favorite_recipe = db.get_favorite_by_id(chat_id, recipe_id)
        recipe_name = favorite_recipe.get('strMeal', 'Неизвестное блюдо') if favorite_recipe else 'Рецепт'
        
        # Формируем звезды нового рейтинга
        stars = "⭐" * rating + "☆" * (5 - rating)
        
        # Создаем кнопки навигации
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ К моим рецептам", callback_data="my_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        
        bot.send_message(
            chat_id,
            f"✅ Рейтинг обновлен!\n\n"
            f"**{recipe_name}**\n"
            f"⭐ Новый рейтинг: {stars} ({rating}/5)",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_btn = types.InlineKeyboardButton("◀️ К моим рецептам", callback_data="my_recipes")
        menu_btn = types.InlineKeyboardButton("🏠 В меню", callback_data="back_to_main")
        markup.add(back_btn, menu_btn)
        
        bot.send_message(
            chat_id,
            "❌ Не удалось обновить рейтинг. Попробуйте позже.",
            reply_markup=markup
        )

def handle_show_more_favorites(chat_id):
    """Показать больше избранных рецептов"""
    favorites = db.get_user_favorites(chat_id, limit=50)  # Получаем больше рецептов
    
    if not favorites:
        bot.send_message(chat_id, "❌ Нет больше рецептов для показа.")
        return
    
    view_mode = user_view_preferences.get(chat_id, 'cards')
    
    # Показываем следующие 10 рецептов (с 10 по 20)
    next_favorites = favorites[10:20]
    
    if not next_favorites:
        bot.send_message(chat_id, "✅ Все рецепты уже показаны!")
        return
    
    # Показываем рецепты в выбранном режиме
    if view_mode == 'cards':
        show_favorites_as_cards(chat_id, next_favorites)
    else:
        show_favorites_as_list(chat_id, next_favorites)
    
    # Информация о результатах с кнопками навигации
    total_count = len(favorites)
    shown_count = min(20, total_count)
    
    info_markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Кнопки переключения вида
    if view_mode == 'cards':
        list_btn = types.InlineKeyboardButton("📋 Список", callback_data="view_list")
        info_markup.add(list_btn)
    else:
        cards_btn = types.InlineKeyboardButton("📱 Карточки", callback_data="view_cards")
        info_markup.add(cards_btn)
    
    # Кнопка показа больше рецептов (если есть)
    if total_count > 20:
        more_btn = types.InlineKeyboardButton(
            f"📋 Показано {shown_count} из {total_count}", 
            callback_data="show_more_favorites"
        )
        info_markup.add(more_btn)
    
    # Кнопка возврата в главное меню
    back_btn = types.InlineKeyboardButton("◀️ В главное меню", callback_data="back_to_main")
    info_markup.add(back_btn)
    
    bot.send_message(chat_id, f"📋 Показано {shown_count} из {total_count} рецептов", reply_markup=info_markup)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    """Обработчик всех текстовых сообщений"""
    chat_id = message.chat.id
    text = message.text.strip()
    
    # Проверяем состояние пользователя
    if chat_id in user_states:
        state = user_states[chat_id]
        
        if state == "waiting_for_name":
            del user_states[chat_id]
            perform_search(chat_id, text, "name")
            return
        elif state == "waiting_for_ingredient":
            del user_states[chat_id]
            perform_search(chat_id, text, "ingredient")
            return
    
    # Если нет активного состояния, показываем главное меню
    send_main_menu(chat_id)

if __name__ == '__main__':
    print("🤖 Бот запущен...")
    bot.infinity_polling()
