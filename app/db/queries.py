class QueryTag:
    INSERT_SINGLE = """
    insert into public.tags (tag_name, description) 
    values (:tag_name, :description) 
    returning *
    """


queries_tag = QueryTag


class QueryTagTopic:
    INSERT_SINGLE = """
    insert into public.tag_topic (topic_uniq_id, tag_uniq_id) 
    values (:topic_uniq_id, :tag_uniq_id) 
    returning *
    """


queries_tag_topic = QueryTagTopic


class QueryReadText:
    INSERT_SINGLE = """
    insert into public.read_texts (owner_uniq_id, read_text) 
    values (:owner_uniq_id, :read_text) 
    returning *
    """


queries_read_text = QueryReadText


class QueryRecord:
    INSERT_SINGLE = """
    insert into public.records (owner_uniq_id, filename) 
    values (:owner_uniq_id, :filename) 
    returning *
    """


queries_record = QueryRecord


class QueryCommentar:
    INSERT_SINGLE = """
    insert into public.commentars (owner_uniq_id, commentar) 
    values (:owner_uniq_id, :commentar) 
    returning *
    """


queries_commentar = QueryCommentar


class QueryTopicQuestion:
    INSERT_SINGLE = """
    insert into public.topic_question (topic_uniq_id, question_uniq_id) 
    values (:topic_uniq_id, :question_uniq_id) 
    returning *
    """

    DELETE_BY_TOPIC_UNIQ_ID = """
    delete from public.topic_question
    where topic_uniq_id = :topic_uniq_id
    """


queries_topic_question = QueryTopicQuestion


class QueryQuestion:
    INSERT_SINGLE = """
    insert into public.questions 
    (owner_uniq_id, commentar_uniq_id, record_uniq_id, text_uniq_id) 
    values (:owner_uniq_id, :commentar_uniq_id, :record_uniq_id, :text_uniq_id) 
    returning *
    """

    GET_QUESTION_BY_TOPIC_UNIQ_ID = """
    select * 
    from questions 
    where uniq_id = (
        select question_uniq_id 
        from topic_question 
        where topic_uniq_id = :topic_uniq_id
    )
    """


queries_question = QueryQuestion


class QueryAnswer:
    INSERT_SINGLE = """
    insert into public.answers 
    (owner_uniq_id, commentar_uniq_id, record_uniq_id) 
    values (:owner_uniq_id, :commentar_uniq_id, :record_uniq_id) 
    returning *
    """

    GET_COMBI_BY_UNIQ_ID = """
    select 
        answers.uniq_id as ans_uniq_id,
        answers.created_at as ans_created_at,
        answers.updated_at as ans_updated_at,
        --
        users.uniq_id as u_uniq_id, 
        users.username as u_username,  
        users.created_at as u_created_at,  
        --
        commentars.uniq_id as c_uniq_id, 
        commentars.commentar as c_commentar,  
        commentars.created_at as c_created_at,  
        commentars.updated_at as c_updated_at,  
        --
        records.uniq_id as rc_uniq_id, 
        records.filename as rc_filename,  
        records.created_at as rc_created_at, 
        records.updated_at as rc_updated_at
    
    from answers
    inner join commentars on answers.commentar_uniq_id = commentars.uniq_id 
    inner join records on answers.record_uniq_id = records.uniq_id 
    inner join users on answers.owner_uniq_id = users.uniq_id 
    
    where answers.uniq_id = :answer_uniq_id
    """

    GET_COMBI_BY_TOPIC_UNIQ_ID = """
    select 
        answers.uniq_id as ans_uniq_id,
        answers.created_at as ans_created_at,
        answers.updated_at as ans_updated_at,
        --
        users.uniq_id as u_uniq_id, 
        users.username as u_username,  
        users.created_at as u_created_at,  
        --
        commentars.uniq_id as c_uniq_id, 
        commentars.commentar as c_commentar,  
        commentars.created_at as c_created_at,  
        commentars.updated_at as c_updated_at,  
        --
        records.uniq_id as rc_uniq_id, 
        records.filename as rc_filename,  
        records.created_at as rc_created_at, 
        records.updated_at as rc_updated_at
    
    from answers
    inner join commentars on answers.commentar_uniq_id = commentars.uniq_id 
    inner join records on answers.record_uniq_id = records.uniq_id 
    inner join users on answers.owner_uniq_id = users.uniq_id 
    
    where answers.uniq_id in (
        select answer_uniq_id 
        from topic_answer tq 
        where topic_uniq_id = :topic_uniq_id
    )
    """


queries_answer = QueryAnswer


class QueryTopicAnswer:
    INSERT_SINGLE = """
    insert into public.topic_answer (topic_uniq_id, answer_uniq_id) 
    values (:topic_uniq_id, :answer_uniq_id) 
    returning *
    """


queries_topic_answer = QueryTopicAnswer


class QueryTopic:
    INSERT_SINGLE = """
    insert into public.topics 
    (owner_uniq_id, title, source_language, source_level, wish_correct_languages) 
    values 
    (:owner_uniq_id, :title, :source_language, :source_level, :wish_correct_languages) 
    returning *
    """

    GET_COMBI_BY_TOPIC_UNIQ_ID = """
    select 
        -- topics.id  as t_id,
        topics.uniq_id  as t_uniq_id,
        topics.title as t_title,
        topics.source_language as t_source_language,
        topics.source_level as t_source_level,
        topics.wish_correct_languages as t_wish_correct_languages,
        topics.created_at t_created_at,
        topics.updated_at t_updated_at,
        ----------
        temp_owner.u_uniq_id,
        temp_owner.u_username,
        ----------
        temp_nbr_ans.nbr_answers,
        ----------
        temp_tags.tt_tags,
        temp_tags.tt_tag_uuids,
        ----------
        temp_question_data.q_uniq_id,
        temp_question_data.q_created_at,
        temp_question_data.q_updated_at,
        --
        temp_question_data.rt_uniq_id,
        temp_question_data.rt_read_text,
        temp_question_data.rt_created_at,
        temp_question_data.rt_updated_at,
        --
        temp_question_data.rc_uniq_id,
        temp_question_data.rc_filename,
        temp_question_data.rc_created_at,
        temp_question_data.rc_updated_at,
        --
        temp_question_data.c_uniq_id,
        temp_question_data.c_commentar,
        temp_question_data.c_created_at,
        temp_question_data.c_updated_at
    from topics
    -- temp table for tags for topic id
    inner join (	
        SELECT 
            topics.id as t_id, 
            topics.uniq_id as t_uniq_id, 
            array_agg(tags.tag_name) as tt_tags,
            array_agg(tags.uniq_id) as tt_tag_uuids
        FROM topics
        INNER JOIN tag_topic
        ON tag_topic.topic_uniq_id = topics.uniq_id
        INNER JOIN tags
        ON tags.uniq_id = tag_topic.tag_uniq_id
        GROUP BY topics.uniq_id, topics.title
    ) temp_tags 
    on temp_tags.t_uniq_id = topics.uniq_id
    -- temp table for number of answers
    inner join (	
        SELECT 
            topics.uniq_id as t_uniq_id , 
            count( topic_answer.answer_uniq_id ) as nbr_answers
        FROM topics LEFT JOIN topic_answer ON topics.uniq_id=topic_answer.topic_uniq_id 
        GROUP BY topics.uniq_id
    ) temp_nbr_ans 
    on temp_nbr_ans.t_uniq_id = topics.uniq_id
    -- temp table for question data: text+comment+record file
    -------------------------------------------------------------------------------------------------
    inner join (
        SELECT 
            topic_question.topic_uniq_id as t_uniq_id,
            questions.uniq_id as q_uniq_id,
            questions.created_at as q_created_at,
            questions.updated_at as q_updated_at,
            read_texts.uniq_id as rt_uniq_id,
            read_texts.read_text as rt_read_text,
            read_texts.created_at as rt_created_at,
            read_texts.updated_at as rt_updated_at,
            records.uniq_id as rc_uniq_id,
            records.filename as rc_filename,
            records.created_at as rc_created_at,
            records.updated_at as rc_updated_at,
            commentars.uniq_id as c_uniq_id,
            commentars.commentar as c_commentar,
            commentars.created_at as c_created_at,
            commentars.updated_at as c_updated_at
        FROM questions 
        LEFT JOIN topic_question ON questions.uniq_id =topic_question.question_uniq_id 
        LEFT JOIN read_texts ON questions.text_uniq_id =read_texts.uniq_id 
        LEFT JOIN records ON questions.record_uniq_id =records.uniq_id 
        LEFT JOIN commentars ON questions.commentar_uniq_id =commentars.uniq_id 
        group by 
            questions.uniq_id, questions.id, topic_question.topic_uniq_id, questions.uniq_id,
            read_texts.uniq_id, read_texts.read_text, read_texts.created_at, read_texts.updated_at,
            records.uniq_id, records.filename, records.created_at, records.updated_at,
            commentars.uniq_id, commentars.commentar, commentars.created_at, commentars.updated_at
    ) temp_question_data
    on temp_question_data.t_uniq_id = topics.uniq_id 
    -- temp table for user infor: uuid and username
    -------------------------------------------------------------------------------------------------
    inner join (	
        SELECT 
            topics.id as t_id, 
            topics.uniq_id as t_uniq_id, 
            users.username as u_username,
            users.uniq_id as u_uniq_id
        FROM topics
        INNER JOIN users
        ON topics.owner_uniq_id = users.uniq_id
        GROUP BY topics.id, topics.uniq_id, users.username, users.uniq_id
    ) temp_owner 
    on temp_owner.t_uniq_id = topics.uniq_id
    -------------------------------------------------------------------------------------------------
    where topics.uniq_id = :topic_uniq_id
    """

    GET_COMBI_BY_USER_UNIQ_ID = """
    -- get topic-combi by owner id
    select 
        topics.id  as t_id,
        topics.uniq_id  as t_uniq_id,
        topics.title as t_title,
        topics.source_language as t_source_language,
        topics.source_level as t_source_level,
        topics.wish_correct_languages as t_wish_correct_languages,
        topics.created_at t_created_at,
        topics.updated_at t_updated_at,
        ----------
        temp_owner.u_uniq_id,
        temp_owner.u_username,
        ----------
        temp_nbr_ans.nbr_answers,
        ----------
        temp_tags.tt_tags,
        temp_tags.tt_tag_uuids,
        ----------
        temp_question_data.q_uniq_id,
        temp_question_data.q_created_at,
        temp_question_data.q_updated_at,
        --
        temp_question_data.rt_uniq_id,
        temp_question_data.rt_read_text,
        temp_question_data.rt_created_at,
        temp_question_data.rt_updated_at,
        --
        temp_question_data.rc_uniq_id,
        temp_question_data.rc_filename,
        temp_question_data.rc_created_at,
        temp_question_data.rc_updated_at,
        --
        temp_question_data.c_uniq_id,
        temp_question_data.c_commentar,
        temp_question_data.c_created_at,
        temp_question_data.c_updated_at
    from topics
    -- temp table for tags for topic id
    inner join (	
        SELECT 
            topics.id as t_id, 
            topics.uniq_id as t_uniq_id, 
            array_agg(tags.tag_name) as tt_tags,
            array_agg(tags.uniq_id) as tt_tag_uuids
        FROM topics
        INNER JOIN tag_topic
        ON tag_topic.topic_uniq_id = topics.uniq_id
        INNER JOIN tags
        ON tags.uniq_id = tag_topic.tag_uniq_id
        GROUP BY topics.uniq_id, topics.title
    ) temp_tags 
    on temp_tags.t_uniq_id = topics.uniq_id
    -- temp table for number of answers
    inner join (	
        SELECT 
            topics.uniq_id as t_uniq_id , 
            count( topic_answer.answer_uniq_id ) as nbr_answers
        FROM topics LEFT JOIN topic_answer ON topics.uniq_id=topic_answer.topic_uniq_id 
        GROUP BY topics.uniq_id
    ) temp_nbr_ans 
    on temp_nbr_ans.t_uniq_id = topics.uniq_id
    -- temp table for question data: text+comment+record file
    -------------------------------------------------------------------------------------------------
    inner join (
        SELECT 
            topic_question.topic_uniq_id as t_uniq_id,
            questions.uniq_id as q_uniq_id,
            questions.created_at as q_created_at,
            questions.updated_at as q_updated_at,
            read_texts.uniq_id as rt_uniq_id,
            read_texts.read_text as rt_read_text,
            read_texts.created_at as rt_created_at,
            read_texts.updated_at as rt_updated_at,
            records.uniq_id as rc_uniq_id,
            records.filename as rc_filename,
            records.created_at as rc_created_at,
            records.updated_at as rc_updated_at,
            commentars.uniq_id as c_uniq_id,
            commentars.commentar as c_commentar,
            commentars.created_at as c_created_at,
            commentars.updated_at as c_updated_at
        FROM questions 
        LEFT JOIN topic_question ON questions.uniq_id =topic_question.question_uniq_id 
        LEFT JOIN read_texts ON questions.text_uniq_id =read_texts.uniq_id 
        LEFT JOIN records ON questions.record_uniq_id =records.uniq_id 
        LEFT JOIN commentars ON questions.commentar_uniq_id =commentars.uniq_id 
        group by 
            questions.uniq_id, questions.id, topic_question.topic_uniq_id, questions.uniq_id,
            read_texts.uniq_id, read_texts.read_text, read_texts.created_at, read_texts.updated_at,
            records.uniq_id, records.filename, records.created_at, records.updated_at,
            commentars.uniq_id, commentars.commentar, commentars.created_at, commentars.updated_at
    ) temp_question_data
    on temp_question_data.t_uniq_id = topics.uniq_id 
    -- temp table for user infor: uuid and username
    -------------------------------------------------------------------------------------------------
    inner join (	
        SELECT 
            topics.id as t_id, 
            topics.uniq_id as t_uniq_id, 
            users.username as u_username,
            users.uniq_id as u_uniq_id
        FROM topics
        INNER JOIN users
        ON topics.owner_uniq_id = users.uniq_id
        GROUP BY topics.id, topics.uniq_id, users.username, users.uniq_id
    ) temp_owner 
    on temp_owner.t_uniq_id = topics.uniq_id
    -------------------------------------------------------------------------------------------------
    where topics.uniq_id in (
        select uniq_id from topics where owner_uniq_id = :owner_uniq_id
    )
    ORDER by t_created_at DESC 
    OFFSET :skip
    LIMIT :limit
    """


queries_topic = QueryTopic

