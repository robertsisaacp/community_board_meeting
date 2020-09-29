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

    # count and store number of "um", "uh" that was removed
    num_filler = {'uh': query_words.count('uh'), 'um': query_words.count('um')}

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

    return ' '.join(text_output), num_filler


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
        #text_input = re.sub(r'\.(?!\d)', '', text_input)
        #text_input = re.sub(r'\,(?!\d)', '', text_input)

        # remove lingering repeated word

        sentences = p.punctuate(text_input)

        # fix duplicate punctuation
        sentences = sentences.replace(' .', '.')
        sentences = sentences.replace(' :', ':')
        sentences = sentences.replace(' ,', ',')
        sentences = sentences.replace(', ,', ',')
        sentences = sentences.replace(', :', ',')
        sentences = sentences.replace(', .', ',')
        sentences = sentences.replace(' ,,', ',')
        sentences = sentences.replace(',,', ',')
        sentences = sentences.replace('. .', '.')
        sentences = sentences.replace('.,', '.')
        sentences = sentences.replace(',-', '-')
        sentences = sentences.replace('..', '.')
        sentences = sentences.replace('??', '?')
        sentences = sentences.replace('?,', '?')
        sentences = sentences.replace(',?', '?')
        sentences = sentences.replace('?,', '?')
        sentences = sentences.replace('?.', '?')
        sentences = sentences.replace('.?', '?')
        sentences = sentences.replace('!!', '!')
        sentences = sentences.replace('::', ':')
        sentences = sentences.replace(':.', ':')
        sentences = sentences.replace(',.', '.')
        sentences = sentences.replace(':,', ',')
        sentences = sentences.replace('-,', ',')

    return sentences


def noun_counter(nlp_text, n=None, all_nouns=None):
    """
    Counts number of nouns from raw transcript text, makes dictionary of top words
    returns: Counter object
    """
    import collections
    import spacy

    nlp = spacy.load('en_core_web_sm')
    # apply spacy nlp
    doc = nlp(nlp_text)

    # Just looking at nouns
    nouns = []
    for token in doc:
        if token.is_stop != True and token.is_punct != True and token.pos_ == 'NOUN':
            nouns.append(str(token))

    noun_counter = collections.Counter(nouns)
    if n is not None:
        most_common_noun = noun_counter.most_common(n)
    else:
        # most_common_noun = list(noun_counter.items())
        most_common_noun = noun_counter.most_common()
    # make dictionary and store top n words
    top_nouns = collections.OrderedDict(most_common_noun)
    return top_nouns


def total_num_word_counter(processed_text):
    """
    Counts number of words
    """
    # remove stopwords and punctuations
    words = [token.text for token in processed_text if token.is_stop != True and token.is_punct != True]
    print(words)
    num_words = len(words)

    return num_words


def phrase_maker():
    """read in list from nlp_matcher.json object"""
    import json

    # read in nlp_matcher json object to add to list
    with open('../data/keyword/nlp_matcher.json') as f:
        nlp_matcher = json.load(f)

    # read in clean json object to add capitalization words
    with open('../data/keyword/clean.json') as f:
        clean_json = json.load(f)

    get_clean_content = {}
    # get all capitalized words
    for i in clean_json['capital']:
        get_clean_content['capital'] = [word.upper() for word in clean_json['capital']]

    # get all title words
    for i in clean_json['title']:
        get_clean_content['title'] = [word.title() for word in clean_json['title']]

    # append to nlp_matcher
    data = dict(list(get_clean_content.items()) + list(nlp_matcher.items()))
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
    all_sents = list(dict.fromkeys(important_sentences))
    all_sents = [sent.lstrip()[0].capitalize() + sent.lstrip()[1:] for sent in all_sents]

    all_text = " ".join(all_sents)
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
