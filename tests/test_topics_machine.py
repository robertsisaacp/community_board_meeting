from src.topics_machine import *


def test_generate_topic():
    assert False


def test_get_db_object():
    start, end = analyze_week()
    get_db_object(start, end)
    assert False


def test_analyze_week():
    start, end = analyze_week()
    assert str(start) == '2020-10-25'


def test_get_collection():
    collection = get_collection('transcripts_v3')
    assert collection == 'test'


def test_filter_db_object():
    collection = get_collection('transcripts_v3')
    start, end = analyze_week()
    filter_db = filter_db_object(collection, start, end)
    assert filter_db == 'test'
