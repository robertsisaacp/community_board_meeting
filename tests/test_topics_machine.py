from src.topics_machine import *


def test_generate_topic():
    assert False


def test_analyze_week_None():
    start, end = analyze_week(start_date_input=None)
    assert str(start) == '2020-11-08'


def test_analyze_week():
    start, end = analyze_week(start_date_input='2020-10-25')
    assert str(start) == '2020-10-25'


def test_get_collection():
    collection = get_collection('transcripts_v3')
    assert collection == 'test'


def test_filter_db_object():
    collection = get_collection('transcripts_v3')
    start, end = analyze_week(start_date_input='2020-10-25')
    filter_db = filter_db_object(collection, start, end)

    for id in filter_db:
        print('Generating word list for ' + str(id.get('YoutubeMetadata').get('title')))
        print('Generating word list for ' + str(id.get('properties').get('videoURL')))
        top_word_list = generate_word_list(id)
        input_string = word_list_converter(top_word_list)
    assert input_string == 'air heat parks projects park gas heating energy program project capital place kind'


def test_word_list_converter():
    input_dict = {'top_words': ['report', 'information', 'budget', 'person', 'page', 'parks', 'example', 'idea', 'month', 'guys', 'licensing', 'documents', 'seniors', 'hours']}
    input_string = word_list_converter(input_dict)
    assert input_string == 'report information budget person page parks example idea month guys licensing documents ' \
                           'seniors hours '
