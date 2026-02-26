## Telegram Bot for viewing content with subscription mechanism
Стек: Aiogram, SQLAlchemy(ORM), Alembic(Миграции), Poetry(Управление зависимостями)  
База данных: PostgreSQL (В процессе разработки находится в отдельном docker контейнере)  
Планируется упаковка в Docker контейнеры(Docker Compose)  
Чувствительные переменные для проекта вынесены в environment variables  
Примеры файлов - env.*.example


### Функционал
- Выдача контента по кнопке;
- Ограничение выдачи контента на сутки для пользователя;
- Загрузка медиа файлов от пользователей;
- Оплата подписок (реализовано через yookassa);
- Подписки для пользователя с расширением лимита контента в день на разный срок;


### Для локального запуска
- Installing Dependencies for the project  
`poetry install`  


- Activation of virtual environment  
`$(poetry env activate)`


- Перед применением миграций подключить базу данных любым удобным способом  
Apply Migrations to a database  
`alembic head upgrade`


- Run the bot    
`python3 main.py`