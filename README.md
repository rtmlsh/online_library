# Онлайн-библиотеки 

В репозитории представлен проект веб-версии [онлайн-библиотеки](https://rtmlsh.github.io/online_library/pages/), с использованием скрипта для парсинга сайта и формированием базы данных в формате json. В качестве объекта для парсинга данных выступает сайт [https://tululu.org/](https://tululu.org/). Репозиторий можно скачать и работать с веб-версией проекта оффлайн.

## Парсер сайта tululu.org

Скрипт main.py парсит и скачивает книги и их обложки с сайта [https://tululu.org/](https://tululu.org/).

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

Для запуска скрипта необходимо задать необязательные аргументы (есть значения по умолчанию):

start_page — номер страницы, с которой начать парсить сайт;

last_page — номер страницы, на которой закончить парсинг;

dest_folder — папка, в которую положить результаты парсинга;

json_path — папка, в которую положить json файл парсинга;

skip_imgs — параметр, с помощью которого можно не скачивать картинки;

skip_txt — параметр, с помощью которого можно не скачивать текстовые файлы;

Запуск скрипта осуществляется в командной строке:

```
python main.py start_id end_id
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org/modules/).

