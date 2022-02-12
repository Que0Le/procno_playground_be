import psycopg2
import aiosql
import csv
import sys
import random

# Connect to an existing database
try:
    conn = psycopg2.connect("dbname='testing' user='postgres' host='192.168.1.23' password='postgres'")
    cur = conn.cursor()
except:
    print("I am unable to connect to the database")
queries = aiosql.from_path("./queries.sql", "psycopg2")

def add_user_from_fakes():
    with open("fake_data/1k_fake_user_with_true_salt_and_hash.csv", "r") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            try:
                count += 1
                if count == 1:
                    header = row
                    continue
                # print(row)
                # break
                r = queries.add_user(
                    conn, username=row[1], email=row[2],
                    salt=row[4], hashed_password=row[5],
                )
                # print(r)
                conn.commit()
                # if count == 5:
                #     break
            except KeyboardInterrupt:
                print('Interrupted')
                break
            except:
                print(row)
                if count==10:
                    break

def add_records_to_random_user():
    all_users_id = queries.get_all_users_id(conn)
    with open("fake_data/1k_records_filename.csv", "r") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            try:
                count += 1
                if count == 1:
                    header = row
                    continue

                r = queries.add_record(conn,
                                    owner_id= random.choice(all_users_id),
                                    filename=row[1])
                print(r)
                conn.commit()
                # if count == 5:
                #     break
            except KeyboardInterrupt:
                print('Interrupted')
                break
            except:
                print(row)

add_user_from_fakes()           
all_users_id = queries.get_all_users_id(conn)

# create topic
## pic a user, create question, create text and commentar and record. Also create tags and add to tag_topic
## pic some more users, create answer (with commentars and records)

records_filename = []
commentars_commentar = []
read_texts_text = []
topics = []

list_record_files = [
    "1k_records_filename.csv", "1k_records_filename_2.csv", 
    "1k_records_filename_3.csv", "1k_records_filename_4.csv",
    "1k_records_filename_5.csv", "1k_records_filename_6.csv",
    "1k_records_filename_7.csv", "1k_records_filename_8.csv",
    "1k_records_filename_9.csv"
]
print("Reading recor filenames from files ...")
for f in list_record_files:
    with open("fake_data/"+f, "r") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            try:
                count += 1
                if count == 1:
                    header = row
                    continue
                records_filename.append(row[1])
            except KeyboardInterrupt:
                print('Interrupted')
                break
            except:
                print(str(f) + ":" + str(row))
list_commentar_files= [
    "commentars.csv", "commentars_2.csv", "commentars_3.csv", 
    "commentars_4.csv", "commentars_5.csv", "commentars_6.csv", 
    "commentars_7.csv", "commentars_8.csv", "commentars_9.csv"
]
print("Reading commentars from files ...")
for f in list_commentar_files:
    with open("fake_data/"+f, "r") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            try:
                count += 1
                if count == 1:
                    header = row
                    continue
                commentars_commentar.append(row[1])
            except KeyboardInterrupt:
                print('Interrupted')
                break
            except:
                print(str(f) + ":" + str(row))
print("Reading read_texts from files ...")
for f in ["read_texts.csv", "read_texts_2.csv", "read_texts_3.csv"]:
    with open("fake_data/"+f, "r") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            try:
                count += 1
                if count == 1:
                    header = row
                    continue
                read_texts_text.append(row[1])
            except KeyboardInterrupt:
                print('Interrupted')
                break
            except:
                print(str(f) + ":" + str(row))
print("Reading topics from files ...")
for f in ["topic.csv", "topic_2.csv"]:
    # id,
    # topic_name,source_lang,source_level,
    # wish_correct_language_1,wish_correct_language_2,wish_correct_language_3,
    # tags
    with open("fake_data/"+f, "r", encoding="utf8", errors="ignore") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            try:
                count += 1
                if count == 1:
                    header = row
                    continue
                # title, source_lang, source_level, wish_lang[], tags[],
                wish_lang = []
                if row[4]!='':
                    wish_lang.append(row[4])
                if row[5]!='':
                    wish_lang.append(row[5])
                if row[6]!='':
                    wish_lang.append(row[6])
                topics.append(
                    [row[1], row[2], row[3], wish_lang, row[7].split(' ')]
                )
            except KeyboardInterrupt:
                print('Interrupted')
                break
            except:
                print(str(f) + ":" + str(row))

random.shuffle(records_filename)
print("records_filename: " + str(len(records_filename)))
random.shuffle(commentars_commentar)
print("commentars_commentar: " + str(len(commentars_commentar)))
random.shuffle(read_texts_text)
print("read_texts_text: " + str(len(read_texts_text)))
random.shuffle(topics)
print("topics: " + str(len(topics)))

#all_users_id
count_topic = 0
for topic in topics:
    # Create a question by 
    # 1.record 2.read_text 3.commentar
    try:
        topic_owner_id = random.choice(all_users_id)
        record_filename = records_filename.pop()
        read_text_text = read_texts_text.pop()
        commentar_commentar = commentars_commentar.pop()
    except:
        print("failed get data for topic")
        exit()
        continue
    try:
        inserted_record = queries.add_record(conn,
                            owner_id=topic_owner_id,
                            filename=record_filename)
        conn.commit()
        inserted_text = queries.add_read_text(conn,
                            owner_id=topic_owner_id,
                            read_text=read_text_text)
        conn.commit()
        inserted_commentar = queries.add_commentar(conn,
                            owner_id=topic_owner_id,
                            commentar=commentar_commentar)
        conn.commit()

        # Now create question
        inserted_question = queries.add_question(conn,
                        owner_id=topic_owner_id,
                        commentar_id = inserted_commentar[0], 
                        record_id = inserted_record[0], 
                        text_id = inserted_text[0])
        conn.commit()

        # Create topic
        # with these information
        inserted_topic = queries.add_topic(
            conn,
            owner_id=topic_owner_id,
            title=topic[0],
            source_language=topic[1],
            source_level=topic[2],
            wish_correct_languages=topic[3]
            # question_id=inserted_question[0]
        )
        # ... and add to topic_question
        inserted_topic_question = queries.add_topic_question(
            conn,
            topic_id=inserted_topic[0],
            question_id=inserted_question[0]
        )
        # print(r)
        conn.commit()
        print(f"Topic {str(count_topic)}/{str(len(topics))}")
        count_topic += 1
    except:
        print("failed create topic and/or quest/comm/record")
        exit()
        continue

    # Create tags/get tags id for topic
    for tag in topic[4]:
        try:
            tag_id = queries.get_tagid_by_tagname(conn, tag_name=tag)
            if tag_id==None:
                r = queries.add_tag(conn, tag_name=tag)
                # print(r)
                conn.commit()
                tag_id = r[0]
            # insert to tag_topic
            inserted_tag_topic = queries.add_tag_topic(
                conn,
                topic_id=inserted_topic[0],
                tag_id=tag_id
            )
            conn.commit()
        except:
            print(f"failed create tag '{tag}' for topic")

    # Random number of answer
    num_ans = random.randint(0,9)   
    for na in range(0, num_ans):
        # Create a ans by 
        # 1.record 2.read_text 3.commentar
        try:
            topic_owner_id = random.choice(all_users_id)
            record_filename = records_filename.pop()
            commentar_commentar = commentars_commentar.pop()
        except:
            print("failed get data")
            continue
        try:
            inserted_record = queries.add_record(conn,
                                owner_id=topic_owner_id,
                                filename=record_filename)
            conn.commit()
            inserted_commentar = queries.add_commentar(conn,
                                owner_id=topic_owner_id,
                                commentar=commentar_commentar)
            conn.commit()

            # Now create answer
            inserted_answer = queries.add_answer(conn,
                            owner_id=topic_owner_id,
                            commentar_id = inserted_commentar[0], 
                            record_id = inserted_record[0]) 
            conn.commit()
            # Add to topic answer
            inserted_topic_answer = queries.add_topic_answer(conn,
                    topic_id=inserted_topic[0],
                    answer_id=inserted_answer[0])
            conn.commit()
        except:
            print(f"Failed create answer for topic id={str(inserted_topic[0])}")

# Close communication with the database
cur.close()
conn.close()
