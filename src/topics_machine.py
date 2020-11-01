def analyze_week():
    """
    Input date
    @param start_date:
    @return:
    """
    import datetime as dt
    # Query to last week's data
    day = dt.datetime.now().date()

    # Make range date
    start = day - dt.timedelta(days=day.weekday() + 1)
    end = start + dt.timedelta(days=6)
    return start, end


def get_collection(collection_name):
    import pymongo
    client_address = "mongodb+srv://sarah:FPb9QGT9UexUim7@block-party.099ce.mongodb.net/community-board?retryWrites=true&w=majority"
    # establish connection to database
    client = pymongo.MongoClient(client_address)
    # access the database by making an instance
    db = client['community-board']
    # make collection instance
    collection = db[collection_name]

    return collection


def filter_db_object(collection_obj, start_db, end_db):
    query = collection_obj.find(
        {"YoutubeMetadata.publishDate": {"$gte": start_db.isoformat(), "$lt": end_db.isoformat()}})
    return query


def generate_word_list(id_input_obj):
    """
    Make word count from top summary words and full transcript words
    @param id_input_obj:
    @return:
    """
    full_word_count = id_input_obj.get('properties').get('wordCountFullTranscript')
    summary_word_count = id_input_obj.get('properties').get('wordCountSummary')
    word_count = list(dict(list(full_word_count.items()) + list(summary_word_count.items())).keys())

    # make into dictionary
    word_count_dict = dict({"top_words": word_count})
    print(word_count_dict)
    return word_count_dict


def generate_executive_summary(id_input_obj, input_word_list):
    """
    Take id input obj and generate summary using list from top words
    @param id_input_obj:
    @param input_word_list:
    @return:
    """
    from src.squeegee import phrase_list, text_length
    from src.create_summary import summarize_text

    full_transcript = id_input_obj.get('properties').get('fullTranscript')

    # make summary using top words from transcript and summary
    executive_summary_input = phrase_list(full_transcript, input_word_list)

    # generate summary with 500 words
    executive_summary_output = summarize_text(executive_summary_input, word_count=500)
    read_time = text_length(executive_summary_output)

    return executive_summary_output, read_time


def update_db(id_input_obj, executive_summary_output, read_time):
    """
    Add execSummary and readTimeExecSummary into properties
    @param id_input_obj:
    @param executive_summary_output:
    @param read_time:
    @return:
    """
    print(f'Updating db for {id_input_obj.get("_id")} in {id_input_obj.get("properties").get("videoURL")}.json')
    db_collection.update_one({'_id': id_input_obj.get("_id")},
                            {'$set': {'properties.execSummary': executive_summary_output,
                                      'properties.readTimeExecSummary': str(read_time)}})


if __name__ == "__main__":
    start_date, end_date = analyze_week()
    db_collection = get_collection('transcripts_v3')
    db_query = filter_db_object(db_collection, start_date, end_date)
    # print(query)
    index = 0
    for id in db_query:
        print('Generating word list')
        top_word_list_input = generate_word_list(id)
        print('Compiling summary and read time')
        executive_summary, read_time_executive_summary = generate_executive_summary(id, top_word_list_input)
        print('Updating database')
        update_db(id, executive_summary, read_time_executive_summary)