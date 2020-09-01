import os
import spacy
from pathlib import Path
from itertools import chain

from spacy.matcher import PhraseMatcher
from gensim.summarization import summarize


def summarize_text(text_input=None, ratio_input=None, word_count=None):
    """
    Generate summary from the sentences of transcript, using Gensim
    :param text_input: punctuated transcript
    :param ratio_input: proportion of transcript to output as summary
    :param word_count
    :return: summary of transcript that is shortened to the ratio proportion
    """
    summary_text = summarize(text_input, ratio=ratio_input, word_count=word_count)
    return summary_text


def get_sentence():
    important_sentences = []
    for sent in processed_text.sents:
        for match_id, start, end in phrase_matcher_object(nlp(sent.text)):
            if nlp.vocab.strings[match_id] in ["A1"]:
                important_sentences.append(sent.text)
    # remove duplicate sentences and join
    all_text = " ".join(list(dict.fromkeys(important_sentences)))
    return all_text


def print_phrase():
    for match_id, start, end in important_phrase:
        string_id = nlp.vocab.strings[match_id]
        span = processed_text[start:end]
        print(match_id, string_id, start, end, span.text)


def get_index(phrase_matcher):

    matched_phrases = phrase_matcher(processed_text)
    return matched_phrases


def phrase_list():
    """
    Finds sentences that match phrase
    """
    phrase_matcher = PhraseMatcher(nlp.vocab)

    phrases = ['purpose', 'first', 'second', 'third', 'important', 'critical', 'success', 'failure', 'unfortunate'
               'pandemic', 'transparent', 'community', 'sick', 'concern', 'public', 'homeless', 'safety', 'police',
               'letter', 'petition', 'manage', 'support', 'access', 'education', 'policy']
    patterns = [nlp(text) for text in phrases]

    phrase_matcher.add('A1', None, *patterns)

    return phrase_matcher


def read_file(directory, file_prefix):
    all_files = os.listdir(directory)
    for text_dir in all_files:
        if text_dir.startswith(file_prefix):
            print(text_dir)
            transcript_file = os.path.join(directory, text_dir)
            f = open(transcript_file, 'r')
            transcript_text = f.read()
    return transcript_text


if __name__ == '__main__':
    directory = Path('../transcripts/Brooklyn Community Board 8/2020-08-14')
    transcript = read_file(directory, 'full_transcript')
    nlp = spacy.load('en_core_web_sm')
    processed_text = nlp(transcript)
    phrase_matcher_object = phrase_list()
    important_phrase = get_index(phrase_matcher_object)
    important_text = get_sentence()
    #print('most important sentences')
    #print(important_text)
    summary = summarize_text(important_text, ratio_input=.1)
    print(summary)