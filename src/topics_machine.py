def analyze_month(end_date=None):
    """
    Input date to filter database by.
    @param start_date: initial date to filter a month from
    @return: date range of month from start date.
    """
    import datetime as dt
    from datetime import datetime

    # Query to last week's data
    if end_date is not None:
        day = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        day = dt.datetime.now().date()

    # Make range date
    start = day - dt.timedelta(days=30)
    end = day
    return start, end

def analyze_week(start_date_input=None):
    """
    Input date
    @param start_date:
    @return:
    """
    import datetime as dt
    from datetime import datetime
    # Query to last week's data

    if start_date_input is not None:
        day = datetime.strptime(start_date_input, '%Y-%m-%d')
    else:
        day = dt.datetime.now().date()

    # Make range date
    start = day - dt.timedelta(days=day.weekday() + 1)
    end = start + dt.timedelta(days=6)
    return start, end


def get_collection(collection_name):
    """
    Read in key to mongoDB and return collection
    @param collection_name: specify the collection to call
    @return: collection object
    """
    import pymongo
    import os

    path = os.path.join(os.getcwd(), '../../data/')
    with open(f"{path}mongo_key.txt", "r") as f:
        data = f.readlines()
    client_address = data
    # establish connection to database
    client = pymongo.MongoClient(client_address)
    # access the database by making an instance
    db = client['community-board']
    # make collection instance
    collection = db[collection_name]

    return collection


def filter_db_object(collection_obj, start_db, end_db):
    """
    Grab all objects in collection that are between specified range
    @param collection_obj: collection object from mongoDB
    @param start_db: initial date to begin
    @param end_db: the date to end
    @return: database collection object filtered to date
    """
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


def word_list_converter(top_word_list):
    """
    Take top word count and reformat into string for classification
    @return:
    """
    from itertools import chain
    input_string_list = []
    {input_string_list.append(x) for x in chain(*top_word_list.values()) if x}
    input_string = ' '.join(input_string_list)
    return input_string


def classify_meeting_type(input_keyword_str):
    """
    Using zeo-shot-classification from Hugging Face, classify the type of meeting
    @param input_keyword_str: top word list from full transcript and summary, used to classify meeting type
    @return:
    """
    print('classifying title')
    sequence = input_keyword_str
    candidate_labels = ["General", "Social Services", "Education", "Health", "Employment", "Safety",
                        "Quality of Life", "Transportation", "Infrastructure", "Parks", "Waterfront",
                        "Commercial Development", "Land Use", "Budget", "Housing", "Equity", "Arts and Culture"]

    # save classification
    classification_result = classifier(sequence, candidate_labels)
    print(classification_result)
    # return only top classification
    return classification_result.get('labels')[0]


def update_db(id_input_obj, executive_summary_output, read_time, meeting_classification):
    """
    Add execSummary and readTimeExecSummary into properties
    @param meeting_classification: meeting type from hugging face classification
    @param id_input_obj:
    @param executive_summary_output:
    @param read_time:
    @return:
    """
    print(f'Updating db for {id_input_obj.get("_id")} in {id_input_obj.get("properties").get("videoURL")}.json')
    db_collection.update_one({'_id': id_input_obj.get("_id")},
                             {'$set': {'properties.meetingType': meeting_classification,
                                       'properties.execSummary': executive_summary_output,
                                       'properties.readTimeExecSummary': str(read_time)}})


if __name__ == "__main__":
    from transformers import pipeline

    classifier = pipeline("zero-shot-classification")
    start_date, end_date = analyze_month(end_date='2020-12-04')
    print(f'analyze from {start_date} to {end_date}')
    db_collection = get_collection('transcripts_v3')
    db_query = filter_db_object(db_collection, start_date, end_date)
    # print(query)
    index = 0
    all_summary = []
    for id in db_query:
        print('Generating word list for ' + str(id.get('properties').get('videoURL')))
        top_word_list_input = generate_word_list(id)
        print('Compiling summary and read time')
        executive_summary, read_time_executive_summary = generate_executive_summary(id, top_word_list_input)
        all_summary.append(executive_summary)
        print('Classify Meeting Type')
        print('converting top word list into string')
        input_to_classify = word_list_converter(top_word_list_input)
        print('classifying top word list')
        meeting_type = classify_meeting_type(input_to_classify)
        print('Updating database')
        update_db(id, executive_summary, read_time_executive_summary, meeting_type)
    print(all_summary)
