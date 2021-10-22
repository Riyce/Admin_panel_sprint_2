# ADMIN PANEL

В данном репозитории представлена панель администрирования, написанная с помощью фреймворка Django.

## Используемые технологии

- **Python** 3.9
- **Django** 3.2.8
- **PostgreSQL** 13
- **Nginx** 1.19.3

## Основные компоненты системы

1. **Cервер WSGI/ASGI** — сервер с запущенным приложением.
2. **Nginx** — прокси-сервер, который является точкой входа для web-приложения.
3. **PostgreSQL** — реляционное хранилище данных. 

## Для запуска проекта с использованием docker-compose используйте следующие команды
- **Для начала склонируйте проект командой https://github.com/Riyce/Admin_panel_sprint_2.git**
<br> Далее в директории с проектом выполните следующие команды.
- **sudo docker-compose up -d --build**
- **sudo docker-compose exec web bash**
- **python3 manage.py migrate**
- **python3 manage.py collectstatic --noinput**
- **python3 manage.py createsuperuser**
<br> Укажите свои данные.
- **exit**

## Для заполнения базы данных в докере из базы SQLite выполните следующие команды
- **cd sqlite_to_postgres/**
- **python3 load_data.py**
