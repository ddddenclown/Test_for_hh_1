````markdown
# Test_for_hh_1

Пример проекта с FastAPI + PostgreSQL + Alembic + Docker

---

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ddddenclown/Test_for_hh_1
````

2. Перейдите в папку с проектом:

   ```bash
   cd Test_for_hh_1
   ```

3. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate    # Windows
   ```

4. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

5. Отредактируйте файл `.env`, чтобы указать правильный адрес базы данных (не забудьте изменить URL в seed.py):

- Для запуска без Docker: укажите в `DATABASE_URL` адрес вашей локальной базы (например, `postgresql://user:password@localhost:5432/dbname`).
- Для запуска с Docker: замените в `.env` переменную `POSTGRES_SERVER` на `db`, а `DATABASE_URL` скорректируйте соответственно (например, `postgresql://user:password@db:5432/dbname`).


6. Выполните миграции базы данных:

   ```bash
   alembic upgrade head
   ```

7. Заполните базу тестовыми данными:

   ```bash
   python -m app.seed
   ```

8. Запустите сервер для разработки (например, в PyCharm):

   ```bash
   uvicorn app.main:app --reload
   ```

---

## Запуск с Docker

1. Соберите Docker-образ и поднимите контейнеры:

   ```bash
   docker-compose build
   docker-compose up --force-recreate
   ```

---

## Готово!

* База данных заполнена
* Все работает
* API ключ: `SUPERSECRET`
* Документация API доступна по адресу:
  [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Примечание

Все необходимые файлы (включая `.env`) добавлены специально для удобства.

---

## Дополнительно

Все выполнено строго по ТЗ, основной функционал работает, но могут быть мелкие недочёты (описания, пути). Сам пару раз на всякий случай всё полностью протестировал.
PUT и DELETE не реализованы, так как в ТЗ не было задачи. При необходимости могу дописать.
Проект написан с нуля менее чем за 2 дня (почти без сна). Всё сделано, чтобы быть быстрее других и получить шанс работать именно со мной.

Для связи: [t.me/chto\_eto\_takoee](https://t.me/chto_eto_takoee)
