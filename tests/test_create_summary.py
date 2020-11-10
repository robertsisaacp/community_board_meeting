from src.create_summary import *


def test_get_video_metadata():
    video_id = "QeNf4ZZxqiU"
    metadata_dict = get_video_metadata(video_id)[0]

    # author = metadata_dict.get('author')
    assert metadata_dict == "SCB2"


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
