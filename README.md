
# API Wallet

API приложение, построенное с использованием фреймворка FastAPI. Выполнено в качестве тестового задания. Задача: REST приложение для работы с объетами кошелька с возможностью просмотра баланса, пополнением и снятием средств. Требования:
- приложение должно работать в конкурентной среде (1000 RPS по одному кошельку)
- корректные ответы от приложения при заведомо неверных запросов
- приложение должно запускаться в докер контейнере совместно с базой данных
- необходима возможность настройки различных параметров приложения и базы данных
- эндпоинты должны быть покрыты тестами


## Основные инструменты

 - Python
 - [FastApi](https://fastapi.tiangolo.com/) фреймворк для разработки веб-приложений на языке python
 - [PostgreSQL](https://www.postgresql.org/) система управления реляционными базами данных
 - [SQLAlchemy](https://www.sqlalchemy.org/) мощный инструмент для работы с реляционными базами данных на языке python
 - [Alembic](https://alembic.sqlalchemy.org/en/latest/) инструмент миграция для sqlalchemy
 - [Pytest](https://docs.pytest.org/en/stable/) фреймворк для написания тестов


## Установка приложения
Клонировать гит репозиторий на свою машину:
```
git clone https://github.com/GrigoriyKuzevanov/wallet_test.git
```
В директории проекта создать файл .env, в которм необходимо указать следующие переменные:
```
DB_USER=<Your db user name>
DB_PASSWORD=<Your db password>
DB_NAME=<Your db name>
DB_HOST=db
DB_PORT=5432

TEST_DB_NAME=<Your test db user name>
TEST_DB_HOST=db-test
TEST_DB_PORT=5432

ECHO_SQL=<True or False>
```
Запустить контейнеры с приложением и базами данных:
```
docker compose up
```

## Переменные окружения

Для запуска проекта необходимы следующие переменные в файле .env:

`DB_USER` имя пользователя, используется для основной и тестовой БД

`DB_PASSWORD` пароль пользователя, используется для основной и тестовой БД

`DB_NAME` название основной БД

`DB_HOST=db` адрес хоста основной БД, значение `db`

`DB_PORT=5432` адрес хоста основной БД, значение `5432`

`TEST_DB_NAME` название тестовой БД

`TEST_DB_HOST=db-test` адрес хоста тестовой БД, значение `db-test`

`TEST_DB_PORT=5432` адрес хоста тестовой БД, значение `5432`

`ECHO_SQL` при значении `True` - вывод в консоль sql запросов, формируемых приложением при обращении в БД, `False` - вывод отключен
## Docker Compose
При запуске в docker compose создается 3 docker контейнера:
- `db` - основная база данных postgres, используемая приложением. Данные базы сохраняются на локальной машине в volume wallet-db. Доступ к базе данных можно получить обращаясь на порт 5431
- `db-test` - тестовая база данных, используемая при запуске тестов. Доступ к базе данных можно получить обращаясь на порт 5430
- `app` - веб-приложение, при старте контейнера запускет тесты командой `pytest -v -p no:warnings `, затем запускает сервер uvicorn на хосте `0.0.0.0:8080`. Доступ к приложению можно получить при обращении к локальному хосту на порт `8080`



## API
После запуска, приложение ожидает http запросы для следующих операций

`BASE_URL=http://localhost:8080/api/v1`

- #### Создание кошелька с начальным балансом

```http
  POST {{BASE_URL}}/wallets/
```
Тело запроса
```json
{
    "balance": <int>
}
```
Тело ответа
```json
{
    "id": <uuid>
    "balance": <int>
}
```
`id` - уникальный идентификатор кошелька, используемый для операций пополнения, снятия и просмотра баланса

- #### Просмотр кошелька

```http
  GET {{BASE_URL}}/wallets/{uuid}
```
Ответ
```json
{
    "id": <uuid>
    "balance": <int>
}
```

- #### Изменение баланса

```http
  GET {{URL}}/wallets/{uuid}/operation
```
Тело запроса
```json
{
    "operationType": <operation_type>,
    "amount": <amount>
}
```
в поле `operationType` необходимо передать либо `DEPOSIT` либо `WITHDRAW`.

`amount` сумма операции

В случае типа `DEPOSIT` - баланс кошелька с идентификатором `{uuid}` будет увеличен на сумму из поля `amount`

В случае типа `WITHDRAW` - баланс кошелька с идентификатором `{uuid}` будет уменьшен на сумму из поля `amount` при условии что средств на балансе достаточно

Ответ
```json
{
    "id": <uuid>,
    "balance": <int>
}
```

- #### Возможные неверные запросы

Кошелька с переданным uuid не существует

```json
{
    "detail": "Wallet with given uuid does not exist"
}
```

Недостаточно средств на балансе
```json
{
    {
    "detail": "Your balance is too low: <your balance>"
}
}
```

Пропущено необходимое поле в теле запросе
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "amount"
            ],
            "msg": "Field required",
            "input": {
                "operationType": "WITHDRAW"
            }
        }
    ]
}
```

## Тестирование

При запуске приложения в docker compose запускаются тесты api эндпоинтов. Их результат можно увидеть в консоли при запуске не в detached mode:
```bash
app-1      | ============================= test session starts ==============================
app-1      | platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0 -- /usr/local/bin/python3.12
app-1      | cachedir: .pytest_cache
app-1      | rootdir: /usr/src/wallet_app
app-1      | plugins: asyncio-0.24.0, anyio-4.4.0
app-1      | asyncio: mode=Mode.STRICT, default_loop_scope=None
app-1      | collecting ... collected 5 items
app-1      | 
app-1      | app/tests/test_api/test_wallets.py::test_get_wallet PASSED
app-1      | app/tests/test_api/test_wallets.py::test_update_wallet_deposit PASSED
app-1      | app/tests/test_api/test_wallets.py::test_update_wallet_withdraw PASSED
app-1      | app/tests/test_api/test_wallets.py::test_update_wallet_withdraw_too_low_balance PASSED
app-1      | app/tests/test_api/test_wallets.py::test_update_wallet_not_exists PASSED
app-1      | 
app-1      | ============================== 5 passed in 1.25s ===============================
```

При необходимости, возможно запустить тестирование из контейнера приложения
```bash
docker exec -it <container_id> bash
root@0595910cb58f:/usr/src/wallet_app# pytest
```

