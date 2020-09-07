from src.squeegee import *
from src.create_summary import *


def test_total_num_word_counter():
    text = "Testing testing 1,2,3"
    word_count = total_num_word_counter(text)
    assert word_count == 3


def test_noun_counter():
    # get transcript text
    video_id = "JcQSyuttoRU"
    transcript_text = get_transcript(video_id)[0]
    word_count = noun_counter(transcript_text)
    assert word_count == 3


def test_phrase_list():
    text = "It is extremely difficult for the seniors and disabled. This sentence is not relevant."
    important_sentence = phrase_list(text)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled.'


def test_phrase_maker():
    all_output = phrase_maker()
    test_output = all_output.get('parks')[0]
    assert test_output == "park"


def test_clean_transcript():
    text = "um testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'testing 1,2,3'


def test_clean_transcript_covid():
    text = "covin um testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'Covid-19 testing 1,2,3'


def test_clean_transcript_capitalize():
    text = "cdc um testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'CDC testing 1,2,3'


def test_clean_transcript_title():
    text = "new york city um testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'New York City testing 1,2,3'


def test_clean_transcript_spelling():
    text = "screenway um testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'greenway testing 1,2,3'



