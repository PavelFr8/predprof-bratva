# Django-приложение

## Требования

- Python версии 3.9+
- Установленный Git
- Установленные зависимости из `requirements.txt`

---

## Туториал по запуску приложения

### Клонирование репозитория

```bash
git clone https://github.com/PavelFr8/predprof-bratva
cd predprof-bratva
```

### Создание виртуальной среды

```bash
python3 -m venv venv
```

### Запуск виртуальной среды

Для Linux/Mac:

```bash
source venv/bin/activate
```

Для Windows:

```bash
venv\Scripts\activate
```

### Загрузка библиотек

```bash
pip install -r requirements.txt
```

### Задание переменных окружения

Скопируйте файл с примером переменных окружения:

Для Linux/Mac:

```bash
cp example.env .env
```

Для Windows:

```bash
copy example.env .env
```

**Примечание:** Не забудьте изменить значения переменных в `.env` в соответствии с вашими настройками.

### Перенос миграций

Перенесите миграции в базу данных:

```bash
cd predprof
python3 manage.py migrate
```

По желанию вы можете добавить в БД тестовые данные от разработчика:

```bash
python3 manage.py loaddata fixtures/data.json
```

### Тестирование

Для проверки правильности настройки приложения вы можете запустить тестирование

```bash
python3 manage.py test
```

### Запуск сервера

```bash
python3 manage.py runserver
```