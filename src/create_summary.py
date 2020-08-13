from youtube_transcript_api import YouTubeTranscriptApi
from gensim.summarization import summarize
from punctuator import Punctuator
import os
from pathlib import Path
import requests
import re


def get_video_metadata():
    """
    Obtains metadata for video
    :return: list of string values to output as text file along with transcript
    """
    response = requests.get(video_url).text

    # collect metadata

    # Community Board Link
    CB = re.findall(r'"author":"[^>]*",', response)[0].split(',')[0]
    CB_channel = re.findall(r'"channelId":"[^>]*",', response)[0].split(',')[0][13:-1]
    channel_link = f'"channelId":"https://www.youtube.com/channel/{CB_channel}'

    # Meeting Information
    title = re.findall(r'"title":"[^>]*",', response)[0].split(',')[0]
    date = re.findall(r'"publishDate":"[^>]*",', response)[0].split('",')[0]
    description = re.findall(r'"shortDescription":"[^>]*",', response)[0].split('",')[0]

    metadata = [CB, title, date, description, channel_link]

    res = []
    for sub in metadata:
        if ':' in sub:
            res.append(map(str.strip, sub.split(':', 1)))
    res = dict(res)
    return res


def get_transcript(video_id):
    """
    With id from youtube, obtain transcript and join each text phrase into one chunk
    :param video_id: id of youtube video
    :return: string of text
    """
    video_id = None if video_id is None else video_id

    # use api to read in transcript
    transcript_input = YouTubeTranscriptApi.get_transcript(video_id)

    # count number of lines
    n = len(transcript_input)

    # get text for each line of transcript
    transcript_text = [transcript_input[i].get('text') for i in range(n)]

    # output in one string chunk
    return " ".join("{}".format(line) for line in transcript_text)


def clean_transcript(text_input):
    """
    Removes filler words from transcript
    :return:
    """
    filler_words = ['um', 'uh', '[music]']
    query_words = text_input.split()

    result_words = [word for word in query_words if word.lower() not in filler_words]
    return ' '.join(result_words)


def add_punctuation(text_input):
    """
    Using Punctuator2 from https://github.com/ottokart/punctuator2
    Breakdown the transcript chunk into sentences with grammar.
    :param text_input: transcript input
    :return: transcript input with grammar added
    """
    # import default pre-trained model from punctuator
    p = Punctuator('Demo-Europarl-EN.pcl')

    text_input = None if text_input is None else text_input

    sentences = p.punctuate(text_input)
    return sentences


def summarize_text(text_input=None, ratio_input=None):
    """
    Generate summary from the sentences of transcript, using Gensim
    :param text_input: punctuated transcript
    :param ratio_input: proportion of transcript to output as summary
    :return: summary of transcript that is shortened to the ratio proportion
    """
    text_input = None if text_input is None else text_input

    summary = summarize(text_input, ratio=ratio_input)
    return summary


def output_transcript():
    """
    Save video metadata, transcript and summary file to text files
    :return: 3 text files in new directory for each community board
    """

    metadata = get_video_metadata()
    transcript_folder_path = Path("transcripts/")
    new_transcript_dir = os.path.join(transcript_folder_path, metadata.get('"author"').strip('"'))
    os.makedirs(new_transcript_dir, exist_ok=True)

    # output video metadata
    with open(f'{new_transcript_dir}//metadata_{transcript_id}.txt', 'w') as f:
        for value in metadata.values():
            f.write('{}\n'.format(value))

    # output full transcript
    with open(f'{new_transcript_dir}//full_transcript_{transcript_id}.txt', 'w') as f:
        f.write(summary_input)

    # output summary transcript
    with open(f'{new_transcript_dir}//summary_{ratio_of_transcript*100}%_transcript_{transcript_id}.txt', 'w') as f:
        f.write(summary_output)


if __name__ == "__main__":
    transcript_id = input('Enter id from Youtube link:')
    video_url = f"https://www.youtube.com/watch?v={transcript_id}"

    print(f'Obtaining transcript for {transcript_id}')
    meeting = get_transcript(transcript_id)
    print('Transcript obtained!')
    print('Removing uh any um filler words')
    meeting = clean_transcript(meeting)
    print('Splitting into Sentences')
    summary_input = add_punctuation(meeting)
    print('Sentences ready for summarization.')
    print('Saving file output')
    ratio_of_transcript = .10
    summary_output = summarize_text(summary_input, ratio_of_transcript)
    print('Your Community Board transcript is ready!')
    output_transcript()


