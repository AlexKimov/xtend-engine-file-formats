# Описание  
Форматы файлов и инструменты для игр Burut CT на движке xtend. Описание форматов в виде шаблонов для 16ричного редактора.  

## Краткое введение в форматы файлов  

#### Игровые ресурсы  
Основные игровые файлы находятся в архиве .pak. Сжатие в архиве не используется.

#### Форматы для моделей и текстур  
Модели оружия, персонажей, монстров хранятся в файлах .skn, анимации моделей находятся в файлах .san. Для текстур используются .bmp, .tga, .dds.

## Вопросы/Ответы  
0. Как распаковать архивы игры .pak?  
  Использовать скрипт для Quickbms ([ссылка](#quickBms)).  
  Использовать скрипт для Noesis ([ссылка](#noesis)).  
1. Как достать модели из игры Kreed?   
  Распаковать архив игры. Для моделей использовать плагины для Noesis ([ссылка](#noesis)).    

## Форматы  

#### Kreed/Kreed Battle for Savitar (2003/2004)  

| №   | Формат | Шаблон (010 Editor) | Прогресс | Описание |
| :-- | :-------- | :------ | :------- | :--   |
| 1 | .pak        | [PAK.bt](templates/010editor/PAK.bt)        | **100%**      |   игровой архив |
| 2 | .skn        | [SKN.bt](templates/010editor/SKN.bt)        | **85%**      |   модели |
| 3 | .san        | [SAN.bt](templates/010editor/SAN.bt)        | **85%**      |  анимации |

    Для чего нужны шаблоны
    Отображение структуры файла в удобном для изучения и редактирования виде, другими словами - описание формата файла.

    Как использовать шаблоны 010Editor
    0. Установить 010Editor.
    1. Открыть нужный файл игры.
    2. Применить шаблон через меню Templates-Run template.   

## Инструменты

### QuickBms
| №	| Скрипт	| Описание| 
| :-- | :-------- | :------ |
| 1	| [unpack_pak.bms](scripts/qbms/unpack_pak.bms)| Распаковка архивов игры|

    Как использовать quickbms скрипты
    1. Нужен quickbms https://aluigi.altervista.org/quickbms.htm
    2. Для запуска в репозитории лежит bat файл с настройками, нужно открыть его и задать свои пути: до места, где находится quickbms, папки с игрой и места куда нужно сохранить результат.
    3. Запустить процесс через bat файл или вручную (задав свои параметры для запуска quickbms, документация на английском есть здесь https://aluigi.altervista.org/papers/quickbms.txt ). 

### noesis
| №	| Плагин	| Описание	| 
| :-- | :-------- | :------ |
| 1	| [fmt_krd_pak.py](plugins/noesis/fmt_krd_pak.py)| Распаковка архивов игры .pak|
| 2	| [fmt_krd_skn.py](plugins/noesis/fmt_krd_skn.py)| Просмотр моделей .skn|

    Как использовать Noesis плагины
    1. Скачать и распаковать Noesis https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91 .
    2. Скопировать нужный вам скрипт в папку ПапкасNoesis/plugins/python.
    3. Запустить Noesis.
    4. Открыть файл через File-Open.
    5. В случае плагина для моделей на экране отобразиться модель, если используется плагин для распаковки архивов, то вы увидите меню с выбором параметров распаковки.
    6. Если файл с нужным вам расширением отсутствует в меню, то или вы поместили файл плагина в другую папку или произошла ошибка при загрузке плагина.

---

# About
X-tend game engine: file formats and tools.

## Templates and scripts (wip)

**1. The Kreed (2004)**

****Templates****

| № | Format       | Template name     | Progress     | Specs | Description |
| :--- | :--------- | :----------- | :---------- | :---------- | :---------- |
| 1 | .pak        | [PAK.bt](https://github.com/AlexKimov/xtend-engine-file-formats/tree/master/templates/010editor/PAK.bt)        | **100%**      |          |  game archive |
| 2 | .skn        | [SKN.bt](https://github.com/AlexKimov/xtend-engine-file-formats/tree/master/templates/010editor/SKN.bt)        | **85%**      |          |  models |
| 3 | .san        | [SAN.bt](https://github.com/AlexKimov/xtend-engine-file-formats/tree/master/templates/010editor/SAN.bt)        | **85%**      |          |  animations |

****Scripts****

Noesis plugins
* [fmt_krd_skn.py](https://github.com/AlexKimov/xtend-engine-file-formats/tree/master/plugins/noesis/fmt_krd_skn.py)
* [fmt_krd_pak.py](https://github.com/AlexKimov/xtend-engine-file-formats/tree/master/plugins/noesis/fmt_krd_pak.py)
