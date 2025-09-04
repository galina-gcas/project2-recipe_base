#!/usr/bin/env python3
"""
Скрипт для проверки и исправления базы данных рецептов
"""

import sqlite3
import os
from config import DATABASE_NAME

def check_and_fix_database():
    """Проверяет и исправляет структуру базы данных"""
    
    if not os.path.exists(DATABASE_NAME):
        print(f"📁 База данных {DATABASE_NAME} не найдена. Она будет создана при первом запуске бота.")
        return
    
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Проверяем структуру таблицы
            cursor.execute("PRAGMA table_info(favorites)")
            columns = {column[1]: column[2] for column in cursor.fetchall()}
            
            print("🔍 Проверка структуры базы данных...")
            print(f"Найденные колонки: {list(columns.keys())}")
            
            # Проверяем наличие необходимых колонок
            required_columns = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'user_id': 'INTEGER NOT NULL',
                'recipe_id': 'TEXT NOT NULL',
                'recipe_name': 'TEXT NOT NULL',
                'recipe_data': 'TEXT NOT NULL',
                'image_url': 'TEXT',
                'category': 'TEXT',
                'area': 'TEXT',
                'rating': 'INTEGER DEFAULT 0',
                'saved_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            }
            
            missing_columns = []
            for col_name, col_type in required_columns.items():
                if col_name not in columns:
                    missing_columns.append((col_name, col_type))
            
            if missing_columns:
                print(f"⚠️ Найдены отсутствующие колонки: {[col[0] for col in missing_columns]}")
                
                # Добавляем отсутствующие колонки
                for col_name, col_type in missing_columns:
                    try:
                        cursor.execute(f'ALTER TABLE favorites ADD COLUMN {col_name} {col_type}')
                        print(f"✅ Добавлена колонка: {col_name}")
                    except sqlite3.Error as e:
                        print(f"❌ Ошибка добавления колонки {col_name}: {e}")
                
                conn.commit()
                print("🔧 База данных обновлена!")
            else:
                print("✅ Структура базы данных корректна!")
            
            # Проверяем количество записей
            cursor.execute("SELECT COUNT(*) FROM favorites")
            count = cursor.fetchone()[0]
            print(f"📊 Количество сохраненных рецептов: {count}")
            
            # Проверяем рейтинги
            cursor.execute("SELECT COUNT(*) FROM favorites WHERE rating > 0")
            rated_count = cursor.fetchone()[0]
            print(f"⭐ Рецептов с рейтингом: {rated_count}")
            
    except sqlite3.Error as e:
        print(f"❌ Ошибка проверки базы данных: {e}")

if __name__ == "__main__":
    print("🔧 Проверка и исправление базы данных рецептов...")
    check_and_fix_database()
    print("✅ Проверка завершена!")

