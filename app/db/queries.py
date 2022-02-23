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


queries_topic_question = QueryTopicQuestion


class QueryQuestion:
    INSERT_SINGLE = """
    insert into public.questions 
    (owner_uniq_id, commentar_uniq_id, record_uniq_id, text_uniq_id) 
    values (:owner_uniq_id, :commentar_uniq_id, :record_uniq_id, :text_uniq_id) 
    returning *
    """


queries_question = QueryQuestion


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


queries_topic = QueryTopic

