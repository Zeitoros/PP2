-- Создание таблицы контактов
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL
);

-- Создание таблицы групп
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


-- Обновление таблицы контактов
ALTER TABLE contacts
    ADD COLUMN email VARCHAR(100),
    ADD COLUMN birthday DATE,
    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN group_id INTEGER REFERENCES groups(id);


-- Таблица для нескольких номеров телефонов
CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);