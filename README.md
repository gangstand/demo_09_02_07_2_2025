### Проект Кульпинова Н.А. ИС-42

**Учет сырья и расчёт выхода продукции**
PyQt5 + SQLAlchemy + PostgreSQL

---

## Ссылка на github - https://github.com/gangstand/demo_09_02_07_2_2025

---

#### Быстрый старт (Windows)

1. **Создание окружения**

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Установка зависимостей**

```bash
pip install -r requirements.txt
```

3. **Настройка базы данных**
   Создайте `.env` в корне проекта:

```
APP_DATABASE_URL=postgresql+psycopg2://postgres:toor@localhost:5432/kulpinov
APP_DEBUG=0
```

Примените миграции:

```bash
alembic upgrade head
```

4. **Запуск приложения**

```bash
python .\main.py
```

---

#### Возможности

* **Материалы**
  Добавление, редактирование, расчёт минимальной партии.

* **Справочники**
  Типы материала и единицы измерения — добавляются на лету через `+`.

* **Поставщики**
  Отдельное окно: можно указать рейтинг, дату начала, привязку к материалам.

* **Расчёт выхода продукции**
  Выбор типа продукции и сырья, расчёт готовых изделий с учётом потерь.
  Возможность создания новых типов продукции.

---

#### Структура проекта (по слоям)

* `app/infrastructure/database` — SQLAlchemy модели, сессии, миграции
* `app/application/service` — бизнес-логика
* `app/presentation/ui` — основное GUI
* `app/resources` - Файлы и скрипты базы данных, прочие графические файлы (ERD)
* `main.py` — точка входа

---

![ERD](/app/resources/database/ERD.png)