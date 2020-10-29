# ShopAPI
Приложение на основе фреймворка Django, зволяющее создать категорию и товар через REST API.

## В проекте реализованы:
### Cущности:
- Категории (Category)
- Товар (Product)

Товар и Категория связаны между собой [Many-to-many relationships](https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/)

Таблица связи Категоря-Товар создана автоматически силами [Django](https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ManyToManyField)
 
### API:
Запросы к API начинаются с `/api/`

### Категории (Category)
**Создание категорий**

`POST: /api/categories/`

playload:
```
{
  "name": "string",
}
```
**Удаление категорий** (возвращается ошибка, если категория прикреплена к товару)

`DELETE: /api/categories/{category_id}`

### Товар (Product)
**Создание товаров** (у каждого товара может быть от 2х до 10 категорий)

`POST: /api/products/`

playload:
```
{
  "name": "string",
  "price": int,
  "categories": 
    [
        int,
        int
    ],
}
```

**Редактирование Товаров**
`PUT / PATCH: /api/products/{product_id}`

playload:
```
{
  "name": "string",
  "price": int,
  "categories": 
    [
        int,
        int
    ],
}
```
**Удаление товаров** (товар помечается как удаленный)

`DELETE: /api/products/{product_id}`

**Получение товара** 

`GET: /api/products/{product_id}`

**Получение списка товаров**: 

`GET: /api/products/`

**Фильтрация товаров**

`GET: /api/products/`

- Имя / по совпадению с  именем:
```
{
  "name": "string",
}
```

- Название категории  / по совпадению с  названием категории 
```
{
  "categories": "string",
}
```

- Цена от - до
```
{
  "price_from": int,
  "price_to": int,
}
```
- Опубликованные да / нет
```
{
  "published": bool,
}
```

**Выводятся только не удаленные товары**

### Код покрыт тестами.

## Установка
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

**Перед тем, как начать:**
Если вы не пользуетесь `Python 3`, вам нужно будет установить инструмент `virtualenv` при помощи `pip install virtualenv`.
Если вы используете `Python 3`, у вас уже должен быть модуль [venv](https://docs.python.org/3/library/venv.html), установленный в стандартной библиотеке.

### Запуск проекта (на примере Linux)
- Создайте на своем компьютере папку проекта `mkdir api_shop` и перейдите в нее `cd api_shop`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/SergePogorelov/api_shop.git .`
- Создайте виртуальное окружение `python3 -m venv venv`
- Активируйте виртуальное окружение `source venv/bin/activate`
- Установите зависимости `pip install -r requirements.txt`
- Накатите миграции `python manage.py migrate`
- Создайте суперпользователя Django `python manage.py createsuperuser --username admin --email 'admin@example.com'`
- Запустите сервер разработки Django `python manage.py runserver`

### Локальное тестирование

Для запуска тестов выполните команду `python manage.py test`

## В разработке использованы

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Django-filter](https://django-filter.readthedocs.io/en/latest/index.html)
