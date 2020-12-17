from src.create_summary import *


def test_get_video_metadata():
    video_id = "MLysKMjWNbM"
    metadata_dict = get_video_metadata(video_id)[0]
    print(metadata_dict)
    title = metadata_dict.get('publishDate')
    assert title == 'Public Place/ Gowanus Green presentation and Q&A'


def test_get_transcript():
    video_id = "JcQSyuttoRU"
    transcript_text = get_transcript(video_id)
    assert transcript_text[:270] == 'now at 5:30 9:00 p.m. under'


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
    communityID_dict = get_cb_info('BronxCommunityBoard#2')
    communityID = communityID_dict.get('communityID')
    assert communityID == 'BXCB2'


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
    title = get_title(response).get('title')
    assert title == 'Public Place/ Gowanus Green presentation and Q&A'


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


def test_format_title_and_date():
    test_title = "12.02.2020 - CB2 Economic Development & Employment Committee Meeting"
    test_title_1 = "Land Use December 2020 Virtual meeting"
    test_title_2 = "CB14 Public Safety Committee Meeting"
    test_title_3 = "12/01 Transportation & Street Activity Permits Committee 2020"
    test_title_4 = "MCB4 ACES Committee Webinar"
    test_title_5 = "CB 3 Manhattan - Land Use Committee Meeting - Dec 9, 2020"
    test_title_6 = "Traffic & Transportation December 2020 Committee Meeting"
    title_output = format_title_and_date(test_title)
    title_output_1 = format_title_and_date(test_title_1)
    title_output_2 = format_title_and_date(test_title_2)
    title_output_3 = format_title_and_date(test_title_3)
    title_output_4 = format_title_and_date(test_title_4)
    title_output_5 = format_title_and_date(test_title_5)
    title_output_6 = format_title_and_date(test_title_6)
    assert title_output.get('title') == "Economic Development & Employment Committee Meeting"
    assert title_output_1.get('title') == "Land Use"
    assert title_output_2.get('title') == "Public Safety Committee Meeting"
    assert title_output_3.get('title') == "Transportation & Street Activity Permits Committee"
    assert title_output_4.get('title') == "ACES Committee Webinar"
    assert title_output_5.get('title') == "Manhattan - Land Use Committee Meeting"
    assert title_output_6.get('title') == "Traffic & Transportation Committee Meeting"


def test_final_title_scrub():
    test_string = 'Traffic & TransportationCommittee Meeting'

    assert final_title_scrub(test_string) == "Traffic & Transportation Committee Meeting"
