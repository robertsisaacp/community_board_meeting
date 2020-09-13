def clean_transcript(text_input):
    """
    Removes filler words from transcript and any repeat words
    :return:
    """
    import itertools
    import json

    with open('../data/keyword/clean.json') as f:
        data = json.load(f)

    # remove filler words
    filler_words = data.get('filler')
    query_words = text_input.split()

    # check for filler words or for word that repeats in sequence
    remove_dupe_and_filler_words = [word for word, _ in itertools.groupby(query_words) if word not in filler_words]

    # replace mispelling of covid
    covid_normalized = 'Covid-19'
    covid_words = data.get(covid_normalized)
    fix_covid = [covid_normalized if word in covid_words else word for word in remove_dupe_and_filler_words]

    # fix capitalization
    capitalize_words = data.get('capital')
    fix_capitalization = [word.upper() if word in capitalize_words else word for word in fix_covid]

    # fix title case
    title_words = data.get('title')
    fix_title = [word.title() if word in title_words else word for word in fix_capitalization]

    # fix spelling
    spelling_words = data.get('spelling')
    text_output = [spelling_words[word] if word in spelling_words else word for word in fix_title]

    return ' '.join(text_output)


def add_punctuation(text_input, iteration=None):
    """
    Using Punctuator2 from https://github.com/ottokart/punctuator2
    Breakdown the transcript chunk into sentences with grammar.
    :param text_input: transcript input
    :return: transcript input with grammar added
    @param text_input:
    @param iteration: if True, then remove the commas to re-ad
    """
    import re
    from punctuator import Punctuator

    # import default pre-trained model from punctuator
    p = Punctuator('Demo-Europarl-EN.pcl')

    if iteration is None:
        sentences = p.punctuate(text_input)
    else:
        # remove existing commas
        text_input = re.sub(r'\.(?!\d)', '', text_input)
        text_input = re.sub(r'\,(?!\d)', '', text_input)

        # remove lingering repeated word

        sentences = p.punctuate(text_input)

        # fix duplicate punctuation
        sentences = sentences.replace('..', '.')
        sentences = sentences.replace('??', '?')
        sentences = sentences.replace('!!', '!')
        sentences = sentences.replace(':.', ':')
        sentences = sentences.replace(',.', '.')
        sentences = sentences.replace(':,', ',')
        sentences = sentences.replace('-,', ',')

    return sentences


def noun_counter(nlp_text):
    """
    Counts number of nouns from raw transcript text, makes dictionary of top words
    returns: Counter object
    """
    import spacy
    nlp = spacy.load('en_core_web_sm')

    # apply spacy nlp
    doc = nlp(nlp_text)

    # Just looking at nouns
    nouns = []
    for token in doc:
        if token.is_stop != True and token.is_punct != True and token.pos_ == 'NOUN':
            nouns.append(str(token))

    return nouns


def total_num_word_counter(processed_text):
    """
    Counts number of words
    """
    import spacy

    # remove stopwords and punctuations
    words = [token.text for token in processed_text if token.is_stop != True and token.is_punct != True]
    print(words)
    num_words = len(words)

    return num_words


def phrase_maker():
    """read in list from nlp_matcher.json object"""
    import json

    with open('../data/keyword/nlp_matcher.json') as f:
        data = json.load(f)

    return data


def phrase_list(text):
    """
    Establish list of terms to capture desired context parameters. Extracts sentences that match phrase
    """

    import spacy
    from spacy.matcher import PhraseMatcher
    nlp = spacy.load('en_core_web_sm')

    # use spacy nlp.vocab object for encoded annotations adds the “key” for index
    phrase_matcher = PhraseMatcher(nlp.vocab)

    # create list of phrases that should provide important context to capture in text
    phrases = phrase_maker()
    nlp_list = list(phrases.keys())
    # build vocabulary pattern
    for key, value in phrases.items():
        patterns = [nlp(text) for text in value]
        # add list of phrases to key name object
        phrase_matcher.add(f'{key}', None, *patterns)

    # apply nlp model
    processed_text = nlp(text)

    """# add top words from document if not already in nlp_matcher list
    doc_top_nouns = total_num_word_counter()

    noun_words = [nlp(text) for text in doc_top_nouns.keys()]
    phrase_matcher.add('top_noun', None, *noun_words)"""

    # match on processed text
    important_sentences = []
    for sent in processed_text.sents:
        for match_id, start, end in phrase_matcher(nlp(sent.text)):
            for i in range(len(nlp_list)):
                if nlp.vocab.strings[match_id] in [nlp_list[i]]:
                    important_sentences.append(sent.text)
    # remove duplicate sentences and join
    all_text = " ".join(list(dict.fromkeys(important_sentences)))

    return all_text


def iterate_summary_input(input_text):
    """
    run second time to re-add punctuation and then filter though key word list
    @return:
    """
    # rerun punctuation model, with better performance on smaller subset of text
    all_text = add_punctuation(input_text, iteration=True)
    all_text = phrase_list(all_text)
    return all_text
