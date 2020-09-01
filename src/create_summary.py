def get_video_list():
    """
    call csv file of url
    """
    import os
    from pathlib import Path
    import pandas as pd
    video_id_path = Path('../data/')
    video_id_file = os.path.join(video_id_path, 'video_id_list.csv')
    video_id_df = pd.read_csv(video_id_file)

    # filter out anything already processed
    video_id_df = video_id_df[video_id_df['status'].isna()]

    # make list of video ids
    video_id_list = list(set(video_id_df['video_id']))

    return video_id_list


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
    title = re.findall(r'"title":"[^>]*",', response)[0].split(',')[0]
    date = re.findall(r'"publishDate":"[^>]*",', response)[0].split('",')[0]
    description = re.findall(r'"shortDescription":"[^>]*",', response)[0].split('",')[0]

    metadata = [cb, channel_link, title, date, description]

    # make dictionary from metadata values
    res = []
    for sub in metadata:
        if ':' in sub:
            res.append(map(str.strip, sub.replace('"', '').split(':', 1)))
    res = dict(res)
    return res


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
    if ':' not in transcript_text[0]:
        transcript_output = " ".join("{}".format(line) for line in transcript_text)

    # if captions already formatted, we do not want to add punctuation
    if ':' in transcript_text[0]:
        formatted = True
        print("Transcript already formatted")
        transcript_text = [line.split(': ')[-1:] for line in transcript_text]
        transcript_text = list(itertools.chain.from_iterable(transcript_text))
        transcript_output = ' '.join(transcript_text)

    # output in one string chunk
    return transcript_output, formatted


def clean_transcript(text_input):
    """
    Removes filler words from transcript and any repeat words
    :return:
    """
    import itertools

    filler_words = ['um', 'uh', '[music]', '[Music]']
    query_words = text_input.split()

    # check for filler words or for word that repeats in sequence
    result_words = [word for word, _ in itertools.groupby(query_words) if word not in filler_words]
    return ' '.join(result_words)


def add_punctuation(text_input):
    """
    Using Punctuator2 from https://github.com/ottokart/punctuator2
    Breakdown the transcript chunk into sentences with grammar.
    :param text_input: transcript input
    :return: transcript input with grammar added
    """
    from punctuator import Punctuator

    # import default pre-trained model from punctuator
    p = Punctuator('Demo-Europarl-EN.pcl')

    sentences = p.punctuate(text_input)
    return sentences


def summarize_text(text_input=None, ratio_input=None, word_count=None):
    """
    Generate summary from the sentences of transcript, using Gensim
    :param text_input: punctuated transcript
    :param ratio_input: proportion of transcript to output as summary
    :param word_count: if entered
    :return: summary of transcript that is shortened to the ratio proportion
    """
    from gensim.summarization import summarize

    summary = summarize(text_input, ratio=ratio_input)
    return summary


def output_transcript(transcript_id, summary_input, summary_output, ratio_of_transcript):
    """
    Save video metadata, transcript and summary file to text files
    :return: 3 text files in new directory for each community board
    """
    import os
    from pathlib import Path

    metadata = get_video_metadata(transcript_id)
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



