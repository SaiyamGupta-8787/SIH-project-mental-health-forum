-- USE mental_health;
-- CREATING TABLES
-- USERS
-- CREATE TABLE users(
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- name VARCHAR(150) NOT NULL,
-- email VARCHAR(250) NOT NULL UNIQUE,
-- password_hash VARCHAR(250) NOT NULL,
-- role ENUM('Student','Counselor','Admin') NOT NULL DEFAULT 'Student',
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- last_login TIMESTAMP NULL,
-- is_active TINYINT DEFAULT 1,
-- INDEX idx_users_role (role)
-- )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
-- COLLATE=utf8mb4_unicode_ci;
-- SELECT*FROM users;
-- ALTER TABLE users
-- ADD COLUMN anonymous TINYINT NOT NULL DEFAULT 0;

-- THREADS
-- CREATE TABLE threads(
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- title VARCHAR(500) NOT NULL,
-- creator_id INT NULL,
-- is_pinned TINYINT DEFAULT 0,
-- is_closed TINYINT DEFAULT 0,
-- created_at timestamp default current_timestamp,
-- FOREIGN KEY (creator_id) REFERENCES
--  users(id) ON DELETE SET NULL,
--    INDEX idx_threads_created_at(created_at)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
-- COLLATE=utf8mb4_unicode_ci;
-- SELECT*FROM threads;

-- POSTS
-- CREATE TABLE posts(
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- thread_id INT NOT NULL,
-- author_id INT NULL,
-- content TEXT NOT NULL,
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- is_hidden TINYINT DEFAULT 0, -- for moderation
-- FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
-- FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE SET NULL,
-- INDEX idx_posts_thread_id (thread_id),
-- INDEX idx_posts_created_at (created_at)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
-- COLLATE=utf8mb4_unicode_ci;

-- Resources(article/photo/video)
-- CREATE TABLE resources(
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- title VARCHAR(500) NOT NULL,
-- type
-- ENUM('article','audio','video','other')
-- DEFAULT 'article',
-- url VARCHAR(1000) NOT NULL,
-- language VARCHAR(50) DEFAULT 'en',
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- INDEX idx_resources_type (type)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
-- COLLATE=utf8mb4_unicode_ci;

-- MOODS
-- CREATE TABLE moods(
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- user_id INT NOT NULL,
-- mood VARCHAR(250) NOT NULL,
-- mood_type ENUM('happy','sad','anxious','angry','scared', 'energetic','tired','meh','lonely','guilty','insecure','great')
-- DEFAULT 'great',
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
-- INDEX idx_mood_type (mood_type)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
-- COLLATE=utf8mb4_unicode_ci;

-- User profile(optional) 
-- CREATE TABLE user_profiles (
-- user_id INT PRIMARY KEY,
-- college VARCHAR(255),
-- year_of_study VARCHAR(50),
-- prefers_anonymous TINYINT DEFAULT 1,
-- language_pref VARCHAR(50) DEFAULT 'en',
-- FOREIGN KEY (user_id) REFERENCES
-- users(id) ON DELETE CASCADE
-- );

-- Media/Attachment
-- CREATE TABLE media (
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- owner_type ENUM('post','resource','user') NOT NULL,
-- owner_id INT NOT NULL,
-- file_name VARCHAR(500),
-- url VARCHAR(1000),
-- mime VARCHAR(100),
-- size_bytes BIGINT,
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- INDEX idx_media_owner (owner_type,owner_id)
-- );

-- tags and post tags(topic)
-- CREATE TABLE tags (
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- name VARCHAR(100) UNIQUE NOT NULL
-- );
-- CREATE TABLE post_tags (
-- post_id INT NOT NULL,
-- tag_id INT NOT NULL,
-- PRIMARY KEY (post_id,tag_id),
-- FOREIGN KEY (post_id) REFERENCES
-- posts(id) ON DELETE CASCADE,
-- FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
-- );

-- Reactions(likes,dislikes,etc.)
-- CREATE TABLE reactions (
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- post_id INT NOT NULL,
-- user_id INT NULL,
-- type ENUM('like','viewed','dislike')
-- DEFAULT 'viewed',
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
-- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
-- UNIQUE KEY uq_user_post_reaction(post_id, user_id, type)
-- );

-- Reports for moderation
-- CREATE TABLE reports(
-- id INT AUTO_INCREMENT PRIMARY KEY,
-- reporter_id INT NULL,
-- target_type ENUM('post','comment','user') NOT NULL,
-- target_id INT NOT NULL,
-- reason VARCHAR(500),
-- status ENUM('open','reviewed','closed') DEFAULT 'open',
-- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE SET NULL
-- );

-- Searching
-- ALTER TABLE posts ADD FULLTEXT INDEX
-- ft_posts_content (content);
-- ALTER TABLE threads ADD FULLTEXT INDEX
-- ft_threads_title (title);

-- SHOW INDEXES FROM posts;
-- SHOW INDEXES FROM threads;

-- Search threads - titles

-- SET @q = 'stress';  -- replace with the usersearched word

-- SELECT t.id, t.title, u.name AS creator,
--        MATCH(t.title) AGAINST(@q IN NATURAL LANGUAGE MODE) AS relevance,
--        t.created_at
-- FROM threads t
-- LEFT JOIN users u ON t.creator_id = u.id
-- WHERE MATCH(t.title) AGAINST(@q IN NATURAL LANGUAGE MODE)
-- ORDER BY relevance DESC, t.created_at DESC
-- LIMIT 50;

-- SET @q = 'stress';  -- same veriable can also be used again

-- SELECT p.id, p.content, t.title AS thread_title, u.name AS author,
--        MATCH(p.content) AGAINST(@q IN NATURAL LANGUAGE MODE) AS relevance,
--        p.created_at
-- FROM posts p
-- JOIN threads t ON p.thread_id = t.id
-- LEFT JOIN users u ON p.author_id = u.id
-- WHERE MATCH(p.content) AGAINST(@q IN NATURAL LANGUAGE MODE)
-- ORDER BY relevance DESC, p.created_at DESC
-- LIMIT 50;

-- INSERT INTO users (`name`, email, password_hash, `role`)
-- VALUES ('user01','user01@example.com','hash123','student'),
--        ('user02','user02@example.com','hash456','counselor');

-- INSERT INTO threads (title, creator_id)
-- VALUES ('Feeling anxious before exams', 1);

-- INSERT INTO posts (thread_id, author_id, content)
-- VALUES (1,1,'So much pressure, exams are near, any advice?');

-- INSERT INTO resources (title, `type`, url)
-- VALUES ('Relaxation Audio', 'audio', 'https://example.com/exam-stress.mp3'),
--        ('Dealing with exams is EASY','article','https://example.com/exam-stress');

-- SHOW TABLES;
-- USE mental_health;
-- DELETE FROM users;
-- SELECT*FROM threads;
-- add description and creator_id
-- ALTER TABLE resources
--   ADD COLUMN description TEXT NULL,
--   ADD COLUMN creator_id INT NULL;

-- add foreign key 
-- ALTER TABLE resources
--   ADD CONSTRAINT fk_resources_creator FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE SET NULL;
