-- Скрипт инициализации базы данных для Humanology Bot

-- Создание базы данных (если не существует)
-- CREATE DATABASE humanology_bot;

-- Подключение к базе данных
-- \c humanology_bot;

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для telegram_id
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);

-- Таблица логов действий пользователей
CREATE TABLE IF NOT EXISTS user_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(200) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для user_id в логах
CREATE INDEX IF NOT EXISTS idx_user_logs_user_id ON user_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_user_logs_timestamp ON user_logs(timestamp);

-- Таблица результатов тестов
CREATE TABLE IF NOT EXISTS test_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    test_type VARCHAR(50) NOT NULL,
    result_data TEXT NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для user_id в результатах тестов
CREATE INDEX IF NOT EXISTS idx_test_results_user_id ON test_results(user_id);
CREATE INDEX IF NOT EXISTS idx_test_results_test_type ON test_results(test_type);

-- Таблица премиум доступа
CREATE TABLE IF NOT EXISTS premium_access (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    access_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    remaining_uses INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для user_id в премиум доступе
CREATE INDEX IF NOT EXISTS idx_premium_access_user_id ON premium_access(user_id);
CREATE INDEX IF NOT EXISTS idx_premium_access_type ON premium_access(access_type);
CREATE INDEX IF NOT EXISTS idx_premium_access_active ON premium_access(is_active);

-- Таблица консультаций
CREATE TABLE IF NOT EXISTS consultations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_count INTEGER DEFAULT 0,
    last_message_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для user_id в консультациях
CREATE INDEX IF NOT EXISTS idx_consultations_user_id ON consultations(user_id);

-- Таблица результатов ИИ-анализа
CREATE TABLE IF NOT EXISTS ai_analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    media_type VARCHAR(20) NOT NULL,
    file_id VARCHAR(200) NOT NULL,
    analysis_result TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для user_id в ИИ-анализе
CREATE INDEX IF NOT EXISTS idx_ai_analyses_user_id ON ai_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_analyses_media_type ON ai_analyses(media_type);

-- Создание триггера для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Применение триггера к таблицам
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_premium_access_updated_at BEFORE UPDATE ON premium_access
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Создание представления для статистики пользователей
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id,
    u.telegram_id,
    u.username,
    u.first_name,
    u.last_name,
    u.created_at,
    COUNT(ul.id) as total_actions,
    COUNT(tr.id) as total_tests,
    COUNT(pa.id) as total_premium_access,
    COUNT(c.id) as total_consultations,
    COUNT(aa.id) as total_ai_analyses
FROM users u
LEFT JOIN user_logs ul ON u.id = ul.user_id
LEFT JOIN test_results tr ON u.id = tr.user_id
LEFT JOIN premium_access pa ON u.id = pa.user_id
LEFT JOIN consultations c ON u.id = c.user_id
LEFT JOIN ai_analyses aa ON u.id = aa.user_id
GROUP BY u.id, u.telegram_id, u.username, u.first_name, u.last_name, u.created_at;

-- Создание представления для активных подписок
CREATE OR REPLACE VIEW active_subscriptions AS
SELECT 
    u.telegram_id,
    u.username,
    pa.access_type,
    pa.expires_at,
    pa.remaining_uses,
    pa.created_at
FROM premium_access pa
JOIN users u ON pa.user_id = u.id
WHERE pa.is_active = TRUE
AND (pa.expires_at IS NULL OR pa.expires_at > CURRENT_TIMESTAMP);

-- Вставка тестовых данных (опционально)
-- INSERT INTO users (telegram_id, username, first_name) VALUES 
--     (123456789, 'test_user', 'Test User');

-- Создание пользователя для бота (если нужно)
-- INSERT INTO users (telegram_id, username, first_name) VALUES 
--     (0, 'bot', 'Humanology Bot');

-- Комментарии к таблицам
COMMENT ON TABLE users IS 'Пользователи бота';
COMMENT ON TABLE user_logs IS 'Логи действий пользователей';
COMMENT ON TABLE test_results IS 'Результаты тестов';
COMMENT ON TABLE premium_access IS 'Премиум доступ пользователей';
COMMENT ON TABLE consultations IS 'Консультации с ИИ';
COMMENT ON TABLE ai_analyses IS 'Результаты ИИ-анализа';

-- Проверка создания таблиц
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
