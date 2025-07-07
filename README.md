# Новостной портал

## 🚀 Установка и запуск проекта

### 1. Клонирование репозитория
Выполните в терминале:

Через SSH (рекомендуется)
```bash
git clone git@github.com:SaitBakhteev/News_portal_D9.5.4.git
```
Или через HTTPS
```bash
git clone https://github.com/SaitBakhteev/News_portal_D9.5.4.git
```
Перейдите в директория проекта
```bash
cd djangoProject_News_Portal
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

#### Активация окружения
Windows:
```bash
venv\Scripts\activate
```
Linux/Mac:
```bash
source venv/bin/activate
```
#### Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Создайте в поддиректории <i>djangoProject_News_Portal</i> проекта файл .env и пропишите следующие данные:
```ini
SECRET_KEY=<ваш ключ django>

# данные для почты
EMAIL_HOST_USER=<адрес хоста почты>
DEFAULT_FROM_EMAIL=<адрес почты для рассылки>
EMAIL_HOST_PASSWORD=<спец пароль для использования почты>

# данные для oauth yandex
YANDEX_CLIENT_ID=<ваш id пользователя API Яндекс>
YANDEX_SECRET=<ваш ключ для API Яндекс>

```


### 4. Настройка БД и запуск (по умолчанию SQLite)

#### Если у вас БД Postgres до выполните следующие действия:
- Откройте проект с помощью IDE и в файле <i>djangoProject/settings.py</i> закомментируйте строки, связанные с настройками SQLite и активируйте строки по Postgres:
 
```python
        # Настройки при использовании Sqlite
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite',

        # Настройки при использовании Postgres
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'NAME': os.getenv('DB_NAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
```
- добавьте в .env следующие данные:

```ini
DB_HOST=localhost  # или другой адрес, если не на локальном сервере
DB_PORT=5432  # или другой порт
DB_USER=<имя пользователя postgres>
DB_NAME=<название вашей базы данных>
DB_PASSWORD=<пароль базы данных>
```

#### Осуществите миграции и запустите сервер
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Сервер запустится по адресу: http://localhost:8000<br>

## 🔐 Первые шаги
1. Откройте <a href="http://localhost:8000">главную страницу</a>
2. Зарегистрируйтесь (кнопка "Регистрация") или через Яндекс
3. Авторизуйтесь под своими данными
4. Начните работу с платформой

## ✨ Основные возможности
### 📰 Работа с новостями
- <b>Просмотр</b> всех новостей с пагинацией
- <b>Создание</b> новых новостей
- <b>Редактирование/удаление</b> своих новостей
- <b>Фильтрация</b> по авторам, названию и дате
