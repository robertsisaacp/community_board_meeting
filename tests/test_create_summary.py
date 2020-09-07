from src.create_summary import *


def test_get_video_metadata():
    video_id = "dIT1iiPoLKU"
    metadata_dict = get_video_metadata(video_id)
    author = metadata_dict.get('author')
    assert author == "CB2 Staten Island"


def test_get_transcript():
    video_id = "JcQSyuttoRU"
    transcript_text = get_transcript(video_id)
    assert transcript_text[0][:270] == 'now at 5:30 9:00 p.m. under'
