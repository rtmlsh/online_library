# Парсер сайта tululu.org
Скрипт парсит и скачивает книги и их обложки с сайта [https://tululu.org/](https://tululu.org/).

## Как установить
На компьютере должен быть уже установлен Python3. Для запуска скрипта установите виртуальное окружение:

```
python3 -m venv venv
```

Затем активируйте виртуальное окружение (вариант для Windows):

```
venv\Scripts\activate
```

Затем активируйте виртуальное окружение (вариант для Mac OS):

```
source venv/bin/activate
```

Используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Запуск скрипта

Для запуска скрипта необходимо обязательные аргументы start_id и end_id.

start_id — id книги, с которой начать парсить сайт;

end_id — id, на котором закончить парсинг.

Запуск скрипта осуществляется в командной строке:

```
python main.py start_id end_id
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org/modules/).
