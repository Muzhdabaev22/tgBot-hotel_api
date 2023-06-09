Важно! Этот бот уже не работает корректно. В api изменили систему, поэтому нужно переписывать некоторые функции, связанные с api 

# Поиск отелей в Telegram

Этот бот позволяет быстро подбирать отели прямо в мессенджере Telegram по различным критериям поиска.

## Особенности

Данный бот позволяет:
* подбирать отели по самой низкой или высокой цене;
* подбирать отели по лучшему соотношению цена/расстояние от центра города;
* задавать количество выводимых отелей;
* задавать диапазон цен.

## Логирование

В скрипте этого бота используется модуль loguru для логирования
```
from loguru import logger
logger.add("info.log", format="{time} | {level} | {message}", level="DEBUG", rotation="5 MB")
```

## Команды бота

* /start - запуск бота, выполняется автоматически при подключении к боту.
* /help - список команд и их описание
* /lowprice - топ дешевых отелей
* /highprice - топ дорогих отелей
* /bestdeal - лучшие предложения

## Как работать с ботом

### Топ дешевых отелей
   1. Введите команду /lowprice. Бот запросит место действия.
   2. После ввода бот запросит город, в котором будет проводиться поиск.
   3. Введите название населенного пункта. Бот выполнит запрос к hotels api и выведет список локаций, названия которых похожи на введенный   город.       Если бот не найдет ни одну локацию, то необходимо ввести команду заново, т.к. вы можете ввести ошибку или не существующий город.
   4. Выберите один из предложенных вариантов, наиболее подходящих вашему запросу.
   5. После этого бот запросит дать согласие на вывод отелей с фотографиями. Введите да/нет или yes/no.
   6. Бот запросит количество отелей, которые вы хотите вывести в качестве результата. Введите количество отелей.
   7. Бот выполнит следующий запрос к hotels api и выведет список отелей с указанием названия, цены, адреса и сайта с подробной информацией.

### Топ дорогих отелей
   1. Для получения списка самых дорогих отелей введите команду /highprice и выполните пункты 2 - 5 из инструкции выше для топа дешевых отелей

### Лучшие предложения
   1. Введите команду /bestdeal. Бот запросит место действия.
   2. После ввода бот запросит город, в котором будет проводиться поиск.
   3. Введите название населенного пункта. Бот выполнит запрос к hotels api и выведет список локаций, названия которых похожи на введенный   город.       Если бот не найдет ни одну локацию, то необходимо ввести команду заново, т.к. вы можете ввести ошибку или не существующий город.
   4. Выберите один из предложенных вариантов, наиболее подходящих вашему запросу.
   5. После этого бот запросит дать согласие на вывод отелей с фотографиями. Введите да/нет или yes/no.
   6. Бот запросит диапазон цен на отели. Введите два числа через тире, где первое число это минимальная стоимость отеля, а второе — максимальная.
   7. Бот запросит диапазон расстояния до центра. Введите два числа через тире, где первое число это минимальная стоимость отеля, а второе — максимальная.
   8. Бот запросит количество отелей, которые вы хотите вывести в качестве результата. Введите количество отелей.
   9. Бот выполнит следующий запрос к hotels api и выведет список отелей с указанием названия, цены, адреса и расстояния от центра, а также сайт с подробной информацией
