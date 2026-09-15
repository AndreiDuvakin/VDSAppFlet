MONTH_NAMES = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

PLANS = {
    "small": "512 МБ RAM, 1 CPU, 20 ГБ SSD",
    "medium": "1 ГБ RAM, 1 CPU, 30 ГБ SSD",
    "large": "2 ГБ RAM, 2 CPU, 40 ГБ SSD",
    "huge": "4 ГБ RAM, 2 CPU, 60 ГБ SSD",
    "monster": "8 ГБ RAM, 4 CPU, 80 ГБ SSD",
}

SERVER_STATUSES = {
    "started": "Запущен",
    "stopped": "Остановлен",
    "billing": "Заблокирован",
}


MARKDOWN_README = """# Selectel VDS Client Flet

## О проекте

Неофициальный мобильный клиент для управления серверами
[Selectel VDS](https://vds.selectel.ru).

Приложение разработано на Python с использованием библиотеки Flet и
предназначено для работы с арендованными серверами Selectel с мобильного
устройства.

Проект создан в учебных целях для изучения библиотеки Flet, разработки
кроссплатформенных приложений и практики взаимодействия с REST API.

## Цель создания

Личный некоммерческий проект для практики разработки кроссплатформенных
приложений на языке Python, а также для удобного доступа автора к своим
серверам Selectel.

Проект не является коммерческим продуктом, не предоставляет услуги
хостинга и не предназначен для перепродажи услуг Selectel.

Я просто буду рад если вам оно пригодится. Т.к. мне давно не хватало
мобильного клиента VDS Selectel. Вот я и решил облегчить себе жизнь :)

## Неофициальный статус

Данный проект не является официальным продуктом Selectel, не разработан,
не поддерживается и не одобрен компанией Selectel.

Название Selectel, название Selectel VDS, а также соответствующие логотипы
и товарные знаки принадлежат их правообладателям и используются только для
описания совместимости и назначения приложения.

Автор проекта не связан с компанией Selectel и не представляет её интересы.
Упоминание Selectel не означает наличия партнёрских, лицензионных,
агентских или иных деловых отношений между автором проекта и Selectel.

## Отказ от гарантий и ответственности

Приложение распространяется по принципу «как есть» (`AS IS`) и без каких-либо
явных или подразумеваемых гарантий.

Автор не гарантирует:

- корректную и бесперебойную работу приложения;
- совместимость приложения с текущей или будущими версиями API Selectel;
- сохранность данных, настроек и состояния серверов;
- доступность серверов или сервисов Selectel;
- отсутствие ошибок, уязвимостей и потери данных.

Использование приложения осуществляется исключительно на страх и риск
конечного пользователя. Пользователь самостоятельно отвечает за последствия
использования приложения, включая операции с виртуальными серверами,
сетевыми настройками, ключами доступа, данными и другой инфраструктурой.

Перед выполнением потенциально опасных операций рекомендуется создавать
резервные копии и проверять результат операции через официальную панель
управления Selectel.

Автор не несёт ответственности за прямые или косвенные убытки, простой
серверов, потерю данных, нарушение доступности сервисов или иные последствия,
возникшие в результате использования либо невозможности использования
приложения.

Я просто буду рад если приложение принесет кому-то пользу.

## Контакты

По любым вопросам вы можете написать мне:  
Email:   
* [andrei@duvakin.ru](mailto:andrei@duvakin.ru)
* [andreiduvakin@gmail.com](mailto:andreiduvakin@gmail.com)  

Сайт:
[https://andrei.numerum.team/](https://andrei.numerum.team/)

## Лицензия

Проект распространяется под лицензией MIT.

Лицензия MIT также предусматривает предоставление программного обеспечения
«как есть», без гарантий.

MIT License

Copyright (c) 2026 Andrei Duvakin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""