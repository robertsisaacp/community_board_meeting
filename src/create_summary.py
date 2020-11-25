from src.squeegee import *


def get_video_list(delta=None):
    """
    call csv file of url
    """
    import os
    from pathlib import Path
    import pandas as pd
    video_id_path = Path('../data/')
    video_id_file = os.path.join(video_id_path, 'video_id_list.csv')
    video_id_df = pd.read_csv(video_id_file)

    if delta is not None:
        # specify your path of directory
        path = os.path.join(os.getcwd(), '../json_objects')
        # get all files in directory
        directories = os.listdir(path)
        file_list_processed = [file.split('.json')[0] for file in directories if file != '.DS_Store']
        # filter out anything already processed
        video_id_df = video_id_df[~video_id_df['video_id'].isin(file_list_processed)]

    else:
        # filter out anything already processed
        video_id_df = video_id_df[video_id_df['status'].isna()]

    # make list of video ids
    video_id_list = list(set(video_id_df['video_id']))
    print(video_id_list)
    return video_id_list


def get_cb_info(cb_name):
    """
    @type cb_name: str
    :return: communityID from name in YouTube
    """
    import os
    from pathlib import Path
    import pandas as pd
    cb_id_path = Path('../data/')
    cb_id_file = os.path.join(cb_id_path, 'CB_ID.csv')
    cb_id_df = pd.read_csv(cb_id_file)

    try:
        # match column of youtubeChannelName, get cb_id
        cb_info = \
            cb_id_df[cb_id_df['youtubeChannelName'] == cb_name].where(cb_id_df.notnull(), None).to_dict(
                orient="records")[0]
    except IndexError:
        print('CB ID not found!')
        cb_info = {
            "communityID": "Other",
            "normalizedName": "Other",
            "twitterName": "",
            "youtubeChannelName": "",
            "youtubeChannelURL": "",
            "twitterHandle": "",
            "dateCheckLast": "",
            "status": ""
        }
    return cb_info


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def get_title(response):
    """
    Using beautifulsoup to get the title from the html page
    @param response:
    @return:
    """
    from bs4 import BeautifulSoup, SoupStrainer
    title_container = SoupStrainer("title")
    soup = BeautifulSoup(response, 'lxml', parse_only=title_container)
    title = soup.find('title').text
    # remove the YouTube substring applied to each page
    title = title.replace(" - YouTube", "")

    return title


def get_video_metadata(transcript_id):
    """
    Obtains metadata for video from video url requests
    :return: list of string values to output as text file along with transcript
    """
    import re
    import requests

    video_url = f"https://www.youtube.com/watch?v={transcript_id}"
    response = requests.get(video_url).text

    # collect metadata

    # Community Board Link
    cb = re.findall(r'"author":"[^>]*",', response)[0].split(',')[0]
    cb_channel = re.findall(r'"channelId":"[^>]*",', response)[0].split(',')[0][13:-1]
    channel_link = f'"channelId":"https://www.youtube.com/channel/{cb_channel}'

    # Meeting Information
    title = f'title":"{get_title(response)}"'
    date = re.findall(r'"publishDate":"[^>]*",', response)[0].split('",')[0]
    description = re.findall(r'"shortDescription":"[^>]*",', response)[0].split('",')[0]
    length = re.findall(r'"lengthSeconds":"[^>]*",', response)[0].split('",')[0]

    metadata = [cb, channel_link, title, date, description, length]
    print(metadata)

    # make dictionary from metadata values
    metadata_list = []
    for sub in metadata:
        if ':' in sub:
            metadata_list.append(map(str.strip, sub.replace('"', '').split(':', 1)))
    metadata_dict = dict(metadata_list)

    # convert length seconds into datetime format
    metadata_dict['lengthSeconds'] = convert_seconds(int(metadata_dict.get('lengthSeconds')))

    # get cb_info
    cb_info = get_cb_info(metadata_dict.get('author'))
    # normalize author name to communityID
    cb_id = cb_info.get('communityID')
    metadata_dict.update({'author': cb_id})

    return metadata_dict, cb_info


def get_transcript(video_id):
    """
    Use string id from youtube video to get raw transcript text. Join each text phrase into one chunk of text
    :param video_id: id of youtube video
    :return: string of text
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    import itertools

    # use api to read in transcript
    transcript_input = YouTubeTranscriptApi.get_transcript(video_id, languages=('en', 'en-US'))

    n = len(transcript_input)
    # get all text for each line of transcript
    transcript_text = [transcript_input[i].get('text') for i in range(n)]

    # if there is already a semicolon in the raw text, the video was formatted differently
    formatted = False
    if ',' not in transcript_text[0]:
        transcript_output = " ".join(f"{line}" for line in transcript_text)

    # if captions already formatted, we do not want to add punctuation
    if ',' in transcript_text[0]:
        formatted = True
        print("Transcript already formatted")
        transcript_text = [line.lower().split(': ')[-1:] for line in transcript_text]
        transcript_text = list(itertools.chain.from_iterable(transcript_text))
        transcript_output = " ".join(transcript_text)

    # output in one string chunk
    return transcript_output, formatted


def summarize_text(text_input=None, ratio_input=None, word_count=None):
    """
    Generate summary from the sentences of transcript, using Gensim
    :param text_input: punctuated transcript
    :param ratio_input: proportion of transcript to output as summary
    :param word_count: if entered
    :return: summary of transcript that is shortened to the ratio proportion
    """
    from gensim.summarization import summarize

    summary = summarize(text_input, ratio=ratio_input, word_count=word_count)
    # remove any weird punctuation
    # fix any funky punctuation
    text_output = fix_weird_punctuation(summary)
    return text_output


def output_transcript(transcript_id, summary_input, summary_output, ratio_of_transcript, metadata):
    """
    Save video metadata, transcript and summary file to text files
    :return: 3 text files in new directory for each community board
    """
    import os
    from pathlib import Path

    transcript_folder_path = Path('../transcripts/')
    new_transcript_dir = os.path.join(transcript_folder_path, metadata.get('author'),
                                      metadata.get('publishDate'))
    os.makedirs(new_transcript_dir, exist_ok=True)

    # output video metadata
    with open(f'{new_transcript_dir}//metadata_{transcript_id}.txt', 'w') as f:
        for value in metadata.values():
            f.write('{}\n'.format(value))

    # output full transcript
    with open(f'{new_transcript_dir}//full_transcript_{transcript_id}.txt', 'w') as f:
        f.write(summary_input)

    # output summary transcript
    with open(f'{new_transcript_dir}//summary_{ratio_of_transcript * 100}%_transcript_{transcript_id}.txt', 'w') as f:
        f.write(summary_output)


def make_json(transcript_id, metadata, cb_info, summary_input, summary_output, full_word_count, summary_word_count,
              num_filler) -> object:
    """make json object from all data"""
    import json
    from pathlib import Path

    json_folder_path = Path('../json_objects/')

    output_json = {
        "data": {
            "YoutubeMetadata": metadata,
            "metadata": {"ID": "String",
                         "creationDate": "datetime"},
            "CommunityBoardInfo": cb_info,

            "properties": {
                "videoURL": transcript_id,
                "fillerWordCount": num_filler,
                "readTimeFullTranscript": str(text_length(summary_input)),
                "readTimeSummary": str(text_length(summary_output)),
                "wordCountFullTranscript": full_word_count,
                "wordCountSummary": summary_word_count,
                "fullTranscript": summary_input,
                "summary": summary_output}
        }
    }
    out_file = open(f"{json_folder_path}//{transcript_id}.json", "w")
    json.dump(output_json, out_file, indent=4, sort_keys=False)
    out_file.close()
