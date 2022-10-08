# Notes API

## Описание проекта
API для добавления, удаления, получения и изменения заметок (Note). Заметки хранятся в 
базе данных. Для совершения указанных операций необходима авторизация пользователя.

## Стек технологий
В данном проекте использованы следующие технологии: 
- Django
- Django Rest Framework (для построения API)
- Postgresql (хранение всех данных)
- PyJWT (для работы с токенами и последующей авторизации по ним)
- Docker и docker-compose 

## Запуск 
Для запуска приложения необходимо наличие Docker и docker-compose. Запуск производится 
командной `docker-compose run`.
Для конфигурации базы данных используются переменные окружения, определенные в 
docker-compose.yml и/или файл config.yml