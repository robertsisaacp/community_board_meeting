from src.squeegee import *
from src.create_summary import *


def test_total_num_word_counter():
    text = "Testing testing 1,2,3"
    word_count = total_num_word_counter(text)
    assert word_count == 3


def test_noun_counter():
    # get transcript text

    import json
    with open(f'../json_objects/BiPmjuZAJkc.json') as jsonfile:
        data = json.load(jsonfile)
        summary = data.get('properties').get('summary')
        word_count = noun_counter(summary, 10)

    assert word_count == 3


def test_phrase_list():
    text = "It is extremely difficult for the seniors and disabled. This sentence is not relevant."
    text1 = "The. Very next thing is in by January 16th of every year the mayor drafts a financial plan and the " \
            "preliminary budget once he drafts the So in february you're going to see you know the agencies start to " \
            "respond to our request and by the 15th."
    important_sentence = phrase_list(text)
    important_sentence1 = phrase_list(text1)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled.'
    assert important_sentence1 == "Very next thing is in by January 16th of every year the mayor drafts a financial " \
                                  "plan and the " \
                                  "preliminary budget once he drafts the So in february you're going to see you know " \
                                  "the agencies start to " \
                                  "respond to our request and by the 15th."


def test_phrase_list_more_robust():
    import json
    with open(f'../json_objects/BiPmjuZAJkc.json') as jsonfile:
        data = json.load(jsonfile)
        summary = data.get('properties').get('summary')
        important_sentence = phrase_list(summary)
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
    text = "screenway um testing testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'greenway testing 1,2,3'


def test_add_punctuation():
    text = "and I'm the assistant director of community relations and I'm going to speak first, just kind of briefly " \
           "about the university's reopening plans Even in march, when we sent students home, we still had about 11 " \
           "000, employee, essential employees who remained on campus to work and who are still working today"
    clean_text = add_punctuation(text)
    assert clean_text == "And I'm the assistant director of community relations and I'm, going to speak first, " \
                         "just kind of briefly about the university's reopening plans Even in march, when we sent " \
                         "students home, we still had about 11 000, employee, essential employees who remained on " \
                         "campus to work and who are still working today."


def test_iterate_summary_input():
    import json
    with open(f'../json_objects/Z1YnL2Bq23U_v1.json') as jsonfile:
        data = json.load(jsonfile)
        summary = data.get('properties').get('summary')
        important_sentence = iterate_summary_input(summary)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled.'
