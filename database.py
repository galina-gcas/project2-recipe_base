import sqlite3
import json
from datetime import datetime
from config import DATABASE_NAME

class RecipeDatabase:
    """Класс для работы с базой данных избранных рецептов"""
    
    def __init__(self):
        self.db_name = DATABASE_NAME
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Создаем таблицу для избранных рецептов
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS favorites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        recipe_id TEXT NOT NULL,
                        recipe_name TEXT NOT NULL,
                        recipe_data TEXT NOT NULL,
                        image_url TEXT,
                        category TEXT,
                        area TEXT,
                        rating INTEGER DEFAULT 0,
                        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, recipe_id)
                    )
                ''')
                
                # Создаем индекс для быстрого поиска по пользователю
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_user_id 
                    ON favorites(user_id)
                ''')
                
                # Проверяем, есть ли колонка rating в существующей таблице
                cursor.execute("PRAGMA table_info(favorites)")
                columns = [column[1] for column in cursor.fetchall()]
                
                # Если колонки rating нет, добавляем её
                if 'rating' not in columns:
                    cursor.execute('ALTER TABLE favorites ADD COLUMN rating INTEGER DEFAULT 0')
                    print("🔧 Добавлена колонка rating к существующей таблице")
                
                conn.commit()
                print("🗄️ База данных инициализирована")
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка инициализации базы данных: {e}")
    
    def add_favorite(self, user_id, recipe_data):
        """Добавить рецепт в избранное"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                recipe_id = recipe_data.get('idMeal')
                recipe_name = recipe_data.get('strMeal', 'Неизвестное блюдо')
                image_url = recipe_data.get('strMealThumb', '')
                category = recipe_data.get('strCategory', '')
                area = recipe_data.get('strArea', '')
                
                # Сохраняем полные данные рецепта в JSON
                recipe_json = json.dumps(recipe_data, ensure_ascii=False)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO favorites 
                    (user_id, recipe_id, recipe_name, recipe_data, image_url, category, area, rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                ''', (user_id, recipe_id, recipe_name, recipe_json, image_url, category, area))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка добавления в избранное: {e}")
            return False
    
    def remove_favorite(self, user_id, recipe_id):
        """Удалить рецепт из избранного"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM favorites 
                    WHERE user_id = ? AND recipe_id = ?
                ''', (user_id, recipe_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка удаления из избранного: {e}")
            return False
    
    def get_user_favorites(self, user_id, limit=50):
        """Получить все избранные рецепты пользователя"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT recipe_id, recipe_name, recipe_data, image_url, 
                           category, area, rating, saved_at
                    FROM favorites 
                    WHERE user_id = ? 
                    ORDER BY rating DESC, saved_at DESC 
                    LIMIT ?
                ''', (user_id, limit))
                
                favorites = []
                for row in cursor.fetchall():
                    recipe_id, recipe_name, recipe_data, image_url, category, area, rating, saved_at = row
                    
                    # Восстанавливаем данные рецепта из JSON
                    try:
                        recipe_json = json.loads(recipe_data)
                    except json.JSONDecodeError:
                        recipe_json = {}
                    
                    favorites.append({
                        'recipe_id': recipe_id,
                        'recipe_name': recipe_name,
                        'recipe_data': recipe_json,
                        'image_url': image_url,
                        'category': category,
                        'area': area,
                        'rating': rating,
                        'saved_at': saved_at
                    })
                
                return favorites
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения избранного: {e}")
            return []
    
    def is_favorite(self, user_id, recipe_id):
        """Проверить, есть ли рецепт в избранном у пользователя"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT 1 FROM favorites 
                    WHERE user_id = ? AND recipe_id = ?
                ''', (user_id, recipe_id))
                
                return cursor.fetchone() is not None
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка проверки избранного: {e}")
            return False
    
    def get_favorites_count(self, user_id):
        """Получить количество избранных рецептов пользователя"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT COUNT(*) FROM favorites WHERE user_id = ?
                ''', (user_id,))
                
                result = cursor.fetchone()
                return result[0] if result else 0
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка подсчета избранного: {e}")
            return 0
    
    def get_favorite_by_id(self, user_id, recipe_id):
        """Получить конкретный избранный рецепт"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT recipe_data, rating FROM favorites 
                    WHERE user_id = ? AND recipe_id = ?
                ''', (user_id, recipe_id))
                
                result = cursor.fetchone()
                if result:
                    try:
                        recipe_data = json.loads(result[0])
                        recipe_data['rating'] = result[1]  # Добавляем рейтинг к данным рецепта
                        return recipe_data
                    except json.JSONDecodeError:
                        return None
                return None
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка получения рецепта: {e}")
            return None
    
    def update_rating(self, user_id, recipe_id, rating):
        """Обновить рейтинг рецепта"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE favorites 
                    SET rating = ? 
                    WHERE user_id = ? AND recipe_id = ?
                ''', (rating, user_id, recipe_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка обновления рейтинга: {e}")
            return False
    
    def cleanup_old_favorites(self, days=365):
        """Очистка старых избранных рецептов (старше указанного количества дней)"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM favorites 
                    WHERE saved_at < datetime('now', '-{} days')
                '''.format(days))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                if deleted_count > 0:
                    print(f"🧹 Удалено {deleted_count} старых избранных рецептов")
                
                return deleted_count
                
        except sqlite3.Error as e:
            print(f"❌ Ошибка очистки базы данных: {e}")
            return 0

# Глобальный экземпляр базы данных
db = RecipeDatabase()

