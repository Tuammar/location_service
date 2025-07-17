# CompasVigodnikhProdazh

IoT проект для сбора данных с Bluetooth устройств через MQTT и сохранения в Redis.

## Архитектура

```
Scanner/Beacon → MQTT Broker → Subscriber → Redis → API
```

## Быстрый старт

### 1. Запуск с Docker Compose

```bash
# Клонируйте репозиторий и перейдите в папку
cd CompasVigodnikhProdazh

# Запустите все сервисы
docker-compose up -d

# Посмотрите логи
docker-compose logs -f subscriber
```

### 2. Проверка работы

```bash
# Проверьте что Redis работает
docker exec compas_redis redis-cli ping

# Посмотрите данные в Redis
docker exec compas_redis redis-cli LRANGE "data:ble/p-queue" 0 10
docker exec compas_redis redis-cli HGETALL "latest_data"
```

### 3. Остановка

```bash
docker-compose down
```

## Сервисы

### Redis
- **Порт**: 6379
- **Контейнер**: compas_redis
- **Данные**: Сохраняются в volume `redis_data`

### Subscriber
- **Контейнер**: compas_subscriber  
- **Функция**: Слушает MQTT топик `ble/p-queue` и сохраняет в Redis
- **Restart policy**: unless-stopped

## Структуры данных в Redis

### 1. История сообщений по топикам
```
data:ble/p-queue → список последних 1000 сообщений
```

### 2. Последние данные по топикам
```
latest_data → hash с последними данными по каждому топику
```

## Переменные окружения

```bash
# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# MQTT
MQTT_BROKER=31.56.196.111
MQTT_PORT=1883
MQTT_TOPIC=ble/p-queue
MQTT_USERNAME=scanner
MQTT_PASSWORD=ble-scanner-very-strong-passwd
```

## Разработка

### Локальный запуск subscriber

```bash
cd app

# Установите зависимости
poetry install

# Запустите Redis локально
docker run -d -p 6379:6379 redis:7-alpine

# Запустите subscriber
poetry run python subscriber.py
```

## API (TODO)

В будущем планируется добавить API сервис для получения данных из Redis. 