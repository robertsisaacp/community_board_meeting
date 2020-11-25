from src.create_summary import *


def test_get_video_metadata():
    video_id = "MLysKMjWNbM"
    metadata_dict = get_video_metadata(video_id)[0]
    print(metadata_dict)
    title = metadata_dict.get('title')
    assert title == 'November 19,2020 Public Place/ Gowanus Green presentation and Q&A - YouTube'


def test_get_transcript():
    video_id = "JcQSyuttoRU"
    transcript_text = get_transcript(video_id)
    assert transcript_text[0][:270] == 'now at 5:30 9:00 p.m. under'


def test_get_cb_info():
    transcript_id = "cH59Mm-IfCk"
    metadata_dict = get_video_metadata(transcript_id)
    author = metadata_dict.get('author')
    communityID = author
    assert communityID == 'QCB3'


def test_get_cb_info_simple():
    communityID_dict = get_cb_info('Queens Community Board Thirteen')
    communityID = communityID_dict.get('communityID')
    assert communityID == 'QCB13'


def test_get_cb_info_notaCB():
    communityID_dict = get_cb_info('CNBC Television')
    communityID = communityID_dict.get('communityID')
    assert communityID == 'Other'


def test_get_cb_info_nan():
    communityID_dict = get_cb_info('Queens Community Board Thirteen')
    communityID = communityID_dict.get('twitterHandle')
    assert communityID == None


def test_make_json():
    output_json = make_json('hi', 'there', 'good', 'sir', 'how', 'are', 'you', 'good!')
    assert output_json == 'QCB3'


def test_get_video_list():
    all_ids = get_video_list(delta=True)
    assert len(all_ids) == 7


def test_get_title():
    import requests
    video_url = f"https://www.youtube.com/watch?v=MLysKMjWNbM"
    response = requests.get(video_url).content
    title = get_title(response)
    assert title == 'November 19,2020 Public Place/ Gowanus Green presentation and Q&A'


def test_summarize_text():
    import json
    with open(f'../json_objects/iFmGCX6Sf_0.json') as jsonfile:
        data = json.load(jsonfile)
        test_input = data.get('data').get('properties').get('fullTranscript')
        print(test_input[:1000])
    summary = summarize_text(test_input, .10)

    assert summary == "Let me tell you it's going to be 10 times worse if they had put the monitors where it really truly " \
                 "would impact people on the field, people in the playground, people in the streets, but that's, " \
                 "unfortunately, not what is happening and Kelly we want continuous air monitoring the entire time " \
                 "they have declined that many times we've asked for real-time data, of which we know they are " \
                 "collecting their Ebam equipment: is this facility adding pollutants that are dangerous to the " \
                 "community's health, and especially the elderly and the children that are closest to the vicinity " \
                 "and that's around asphalt, green."
