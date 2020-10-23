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
    text = "It is extremely difficult for the seniors and disabled. This sentence is not relevant. Mayor De Blasio did" \
           " this. Now we have it covered from soup-to-nuts."
    text1 = "The. Very next thing is in by January 16th of every year the mayor drafts a financial plan and the " \
            "preliminary budget once he drafts the So in february you're going to see you know the agencies start to " \
            "respond to our request and by the 15th."
    important_sentence = phrase_list(text)
    important_sentence1 = phrase_list(text1)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled. Mayor De Blasio did this.  Now we have it covered from soup-to-nuts.'
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
    test_output = all_output.get('capital')[0]
    assert test_output == "park"


def test_clean_transcript():
    text = "um testing testing testing 1,2,3"
    clean_text = clean_transcript(text)
    assert clean_text == 'testing 1,2,3'


def test_clean_transcript_count_uh():
    text = "uh testing testing testing 1,2,3"
    clean_text = clean_transcript(text)[1]
    clean_text = clean_text.get('uh')
    assert clean_text == 1


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
    souped = "because it's a nice, diverse range of resources and programs, souped nuts, from individuals on the street"
    clean_text = clean_transcript(text)[0]
    clean_soup = clean_transcript(souped)[0]
    assert clean_text == "greenway testing 1,2,3"
    assert clean_soup == "because it's a nice, diverse range of resources and programs, soup-to-nuts, " \
                         "from individuals on the street "


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


def test_proper_noun_capitalizer():
    import json
    with open(f'../json_objects/Mu_rYVwkOVw.json') as jsonfile:
        data = json.load(jsonfile)
        summary = data.get('data').get('properties').get('summary')
        summary = summary[:2000]
        important_sentence = proper_noun_capitalizer(summary)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled.'


def test_proper_noun_capitalizer_dont():
    test = "There can't be more people impact with more seniors impacted, I'm gonna work it in Okay, number two priority was to increase substance abuse services, including opioid, Overdose, prevention, education and funding for syringe, cleanups and collections."
    summary = "There are so many people that we really need to do the right thing, for, and that really means to stay home if you're, sick, we're face covering when you're in public really do n't gather in large crowds with people who are not your immediate family members, because we're seeing that this is as a result of this behavior we're seeing significant increases in cases, and We want everyone to go, get tested so that the data is as accurate as possible, and the reason why we want people to get tested is so that we can really go and mitigate and prevent these clusters from spreading into larger community transmission and where we have to revert back to the beginning of this pandemic."
    important_sentence = proper_noun_capitalizer(test)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled.'


def test_fix_time():
    test = "Brooklyn bridge, and you know we have about 200 200 by 250 officers. What is starting to make parents unhappy is seeing the Brooklyn tech model which is their two full days from 8 30 to like 2 45 in schools like one week and period class and leave their house at 10 of noon"
    important_sentence = fix_time(test)
    assert important_sentence == 'It is extremely difficult for the seniors and disabled.'
