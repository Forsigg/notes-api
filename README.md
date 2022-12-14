# Notes API
[![Coverage Status](https://coveralls.io/repos/github/Forsigg/notes-api/badge.svg)](https://coveralls.io/github/Forsigg/notes-api)
## Описание проекта
API для добавления, удаления, получения и изменения заметок (Note). Заметки хранятся в 
базе данных. Для совершения указанных операций необходима авторизация пользователя.

### API endpoints
#### Token
*POST*:
/api/token/ - Получение токена для авторизации (в body передается username и password)
/api/token/refresh/ - Получение нового токена доступа и токена для обновления (body 
как и выше)

#### Notes
*GET*:

/api/v1/notes/ - Получение списка всех заметок

/api/v1/notes/<int:pk>/ - Получение информации о конкретной заметке (по pk)

/api/v1/notes/users/<int:pk>/ - Получение списка заметок отдельного пользователя (по 
его pk)


*POST*:

/api/v1/notes/ - Создание новой заметки (в body передаются поля заметки, обязательные 
только author, text)


*PUT*:

/api/v1/notes/<int:pk>/ - Изменение данных заметки (в body передаются новые данные 
заметки)


*DELETE*:

/api/v1/notes/<int:pk>/ - Удаление отдельной заметки

#### Users
*POST*:

/api/v1/auth/register/ - Добавление нового пользователя (в body передаются поля 
пользователя - username, password)

*DELETE*:

/api/v1/auth/users/<int:pk>/ - Удаление пользователя по id(pk)


## Стек технологий
В данном проекте использованы следующие технологии: 
- Django
- Django Rest Framework (для построения API)
- Postgresql (хранение всех данных)
- PyJWT (для работы с токенами и последующей авторизации по ним)
- Docker и docker-compose 

## Запуск 
Для запуска приложения необходимо наличие Docker и docker-compose. Запуск производится 
командой `docker-compose up`.
Для конфигурации базы данных используются переменные окружения, определенные в 
docker-compose.yml и/или файл config.yml
