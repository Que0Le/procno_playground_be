-- name: get_all_users
-- Get all users from public.users table
select * from public.users;

-- name: add_user<!
INSERT INTO public.users (username, email, salt, hashed_password)
VALUES (:username, :email, :salt, :hashed_password)
RETURNING
    id, created_at, updated_at;


-- name: get_user_by_email^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       bio,
       created_at,
       updated_at
FROM users
WHERE email = :email
LIMIT 1;


-- name: get_1_user_by_id
select * from public.users
where id = :id
limit 1;

-- name: get_all_users_uniq_id
select uniq_id from public.users;



-- name: add_record<!
INSERT INTO public.records (owner_uniq_id, filename)
VALUES (:owner_uniq_id, :filename)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_read_text<!
INSERT INTO public.read_texts (owner_uniq_id, read_text)
VALUES (:owner_uniq_id, :read_text)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_commentar<!
INSERT INTO public.commentars (owner_uniq_id, commentar)
VALUES (:owner_uniq_id, :commentar)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_question<!
INSERT INTO public.questions (owner_uniq_id, commentar_uniq_id, record_uniq_id, text_uniq_id)
VALUES (:owner_uniq_id, :commentar_uniq_id, :record_uniq_id, :text_uniq_id)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_topic<!
INSERT INTO public.topics (owner_uniq_id, title, source_language, source_level, wish_correct_languages)
VALUES (:owner_uniq_id, :title, :source_language, :source_level, :wish_correct_languages)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_answer<!
INSERT INTO public.answers (owner_uniq_id, commentar_uniq_id, record_uniq_id)
VALUES (:owner_uniq_id, :commentar_uniq_id, :record_uniq_id)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_topic_answer<!
INSERT INTO public.topic_answer (topic_uniq_id, answer_uniq_id)
VALUES (:topic_uniq_id, :answer_uniq_id)
RETURNING
    created_at, updated_at;

-- name: add_topic_question<!
INSERT INTO public.topic_question (topic_uniq_id, question_uniq_id)
VALUES (:topic_uniq_id, :question_uniq_id)
RETURNING
    created_at, updated_at;

-- name: get_tag_uniq_id_by_tagname<!
select uniq_id from public.tags
where tag_name = :tag_name
LIMIT 1;

-- name: add_tag<!
INSERT INTO public.tags (tag_name)
VALUES (:tag_name)
RETURNING
    uniq_id, created_at, updated_at;

-- name: add_tag_topic<!
INSERT INTO public.tag_topic (topic_uniq_id, tag_uniq_id)
VALUES (:topic_uniq_id, :tag_uniq_id)
RETURNING
    created_at, updated_at;