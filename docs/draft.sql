


-- count topics per user
--SELECT users.id, users.username , count( topics.owner_id ) 
--FROM users LEFT JOIN topics ON users.id=topics.owner_id 
--GROUP BY users.id
------------------------------------------------------------------------------

-- get question-combi for topic id
--SELECT 
--	questions.id as q_id,
--	questions.created_at as q_created_at,
--	questions.updated_at as q_updated_at,
--	read_texts.read_text as rt_read_text,
--	read_texts.created_at as rt_created_at,
--	read_texts.updated_at as rt_updated_at,
--	records.filename as rc_filename,
--	records.created_at as rc_created_at,
--	records.updated_at as rc_updated_at,
--	commentars.commentar as c_commentar,
--	commentars.created_at as c_created_at,
--	commentars.updated_at as c_updated_at
--FROM questions 
--LEFT JOIN read_texts ON questions.text_id =read_texts.id 
--LEFT JOIN records ON questions.record_id =records.id 
--LEFT JOIN commentars ON questions.commentar_id =commentars.id 
--where questions.id = (
--	select topics.question_id 
--	from topics 
--	where topics.id = 1
--)
------------------------------------------------------------------------------

-- get answer-combi for topic
--SELECT 
--	answers.id as a_id,
--	answers.created_at as a_created_at,
--	answers.updated_at as a_updated_at,
--	records.filename as rc_filename,
--	records.created_at as rc_created_at,
--	records.updated_at as rc_updated_at,
--	commentars.commentar as c_commentar,
--	commentars.created_at as c_created_at,
--	commentars.updated_at as c_updated_at
--FROM answers 
--LEFT JOIN records ON answers.record_id =records.id 
--LEFT JOIN commentars ON answers.commentar_id =commentars.id 
--where answers.id in (
--	select 	topic_answers.answer_id 
--	from topic_answers 
--	where topic_answers.topic_id = 1
--)
--ORDER by a_created_at
------------------------------------------------------------------------------

-- get tags for topic id
--SELECT 
--	topics.id as t_id, 
--	topics.title as t_title, 
--	array_agg(tags.tag_name) as tt_tags
--FROM topics
--INNER JOIN tag_topic
--ON tag_topic.topic_id = topics.id
--INNER JOIN tags
--ON tags.id = tag_topic.tag_id
--where topics.id = 1
--GROUP BY topics.id, topics.title

------------------------------------------------------------------------------

-- get topic-combi by id
select 
	topics.id  as t_id,
	topics.title as t_title,
	topics.source_language as t_source_language,
	topics.source_level as t_source_level,
	topics.wish_correct_languages as t_wish_correct_languages,
	topics.created_at t_created_at,
	topics.updated_at t_updated_at,
	--
	temp1_tags.tt_tags,
	--
	temp2_nbr_ans.nbr_answers,
	--
	temp3_question_data.q_created_at,
	temp3_question_data.q_updated_at,
	temp3_question_data.rt_read_text,
	temp3_question_data.rt_created_at,
	temp3_question_data.rt_updated_at,
	temp3_question_data.rc_filename,
	temp3_question_data.rc_created_at,
	temp3_question_data.rc_updated_at,
	temp3_question_data.c_commentar,
	temp3_question_data.c_created_at,
	temp3_question_data.c_updated_at
from topics
-- temp table for tags for topic id
inner join (	
	SELECT 
		topics.id as t_id, 
		array_agg(tags.tag_name) as tt_tags
	FROM topics
	INNER JOIN tag_topic
	ON tag_topic.topic_id = topics.id
	INNER JOIN tags
	ON tags.id = tag_topic.tag_id
	where topics.id = 1
	GROUP BY topics.id, topics.title
) temp1_tags 
on temp1_tags.t_id = topics.id
-- temp table for number of answers
inner join (	
	SELECT 
		topics.id as t_id , 
		count( topic_answers.answer_id ) as nbr_answers
	FROM topics LEFT JOIN topic_answers ON topics.id=topic_answers.topic_id 
	where topics.id = 1
	GROUP BY topics.id
) temp2_nbr_ans 
on temp2_nbr_ans.t_id = topics.id
-- temp table for question data: text+comment+record file
inner join (
	SELECT 
		1 as t_id,
		questions.created_at as q_created_at,
		questions.updated_at as q_updated_at,
		read_texts.read_text as rt_read_text,
		read_texts.created_at as rt_created_at,
		read_texts.updated_at as rt_updated_at,
		records.filename as rc_filename,
		records.created_at as rc_created_at,
		records.updated_at as rc_updated_at,
		commentars.commentar as c_commentar,
		commentars.created_at as c_created_at,
		commentars.updated_at as c_updated_at
	FROM questions 
	LEFT JOIN read_texts ON questions.text_id =read_texts.id 
	LEFT JOIN records ON questions.record_id =records.id 
	LEFT JOIN commentars ON questions.commentar_id =commentars.id 
	where questions.id = (
		select topics.question_id 
		from topics 
		where topics.id = 1
	)
) temp3_question_data
on temp3_question_data.t_id = topics.id 
where topics.id = 1
	

	
	















