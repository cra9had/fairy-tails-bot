# Fairy Tales Bot

## Настройка и запуск бота

### Настройка бота:
1. Переименовать файл `.example_env` в `.env`
2. В файле `.env` указать BOT_TOKEN тг-бота и прочие необходимые настройки (по завершении работы - указать, какие) 
3. Файл `bot_example.service` из каталога `systemd` переименовать и перенести в
`/etc/systemd/system/`

### Запуск:
1. `systemctl enable bot_example --now`

## Для разработчика

### Логи работы
1. `systemctl status bot_example.service`
2. Логи системного журнала за последние N минут: `journalctl -u bot --since "Nm ago"`

### Перезапуск сервиса
1. `systemctl daemon-reload`
2. `systemctl restart bot`


## Краткое описание

Бот для создания персонализированных аудио сказок в виде сериала. 
Сериал состоит из сезонов. 
Каждый сезон состоит из эпизодов в каждом эпизоде по 5 серий.



### Тех. задание

Бот для создания персонализированных аудио сказок в виде сериала. Сериал состоит из сезонов. Каждый сезон состоит из эпизодов в каждом эпизоде по 5 серий.
Пользователь вводит данные ребенка и его интересы. Нейронка генерирует план 1-сезона и отправляет пользователю (текстовый план+картинка к нему. Затем генерируется первая серия, озвучивается, пользователю выдается готовый аудиофайл, текст сказки и картинка к серии. 
В этой версии бота не будет дополнительной работы с аудиофайлом (вставки джинга и фоновой музыки) но нужно будет предусмотреть возможность в будущем добавления такого функционала. 




Меню
Пол ребенка
Имя
Возраст (3,4,5,6,7,8)
Интересы
Космос и фантастика
Супергерои
Волшебство и магия
Современный мир
Пираты и море
Подводный мир
Кнопка. “Отправить данные” 
(при нажатии на кнопку данные подставляются в запрос и отправляются нейронке. Нейронка формирует текстовый план сезона.  Сезон состоит из 2-х эпизодов по 5 серий. Этот план выдаем пользователю в виде текста и картинке к ней) 
* Нужно подумать как генерировать картинку к плану и выдавать пользователю и узнать стоимость генерации картинки.
Кнопка “Получить сказку”
При нажатии нейронке отправляется запрос на генерацию 1-й серии. Этот текст отправляется на озвучку в сервис Апихост. Готовый аудио файл отправляется пользователю. 
(В идеале нужно, чтобы пользователю отправлялся текст сказки и картинка к нему, нужно подумать как реализовать)
Кнопка “Следующая серия”
Здесь начинается монетизация (если тариф не оплачен, то предлагается оплатить. Будет несколько тарифных планов завязанных на количестве сезонов в месяц, которые пользователи смогут генерировать Ели тариф оплачен, то нейронке отправляется запрос на генерацию следующей сказки, дальше как в предыдущем пункте)


После того как будут сгенерированы все серии сезона, пользователю предлагается кнопка следующий сезон. При нажатии генерируется план следующего сезона. Остальное как с первым сезоном. Единственное здесь не будет первой бесплатной сказки. Если тариф не оплачен, предлагается оплатить.

## ***Структура проекта***
[Excalidraw](https://excalidraw.com/#json=sDYx2uA4efMjlSY_gvH0O,lespTIxnXIkvAViSXPzyYw)
