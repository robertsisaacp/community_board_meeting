def proper_noun_capitalizer(input_text):
    """
    Leverage spaCy's tokenizer to understand part of speech to capitalize any proper noun
    @param input_text:
    @return:
    """
    import spacy
    import re
    # Create the nlp object
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(input_text)

    # if word all lowercase and identified as a proper noun by spacy, make into title case
    token_texts = " ".join([tok.text.title() if tok.pos_ == "PROPN" and tok.text.islower()
                            else tok.text for tok in doc])

    # fix spacing if not whitespace
    output = re.sub(r' (?=\W)', '', token_texts)

    # replace conjunction split by spacy with not
    output = output.replace("n't", 'not')
    output = output.replace("ca not", "can't")
    output = output.replace("wo not", "won't")
    # replace split of gon na
    output = output.replace("gon na", 'going to')
    return output


def fix_time(input_string):
    """
    Formats any time string that is missing a colon, adds , to number
    @param input_string:
    @return:
    """
    import re

    # regexp pattern to match on (ex: 12 30)
    ptrn = "\\s(\\d{1,2})\\s(\\d{1,2})\\s"
    output = re.sub(fr'{ptrn}', fr' \1:\2 ', input_string)

    # regexp pattern to match on thousand (12 300)
    ptrn = "\\s(\\d{1,3})\\s(\\d{1,3})\\s"
    output = re.sub(fr'{ptrn}', fr' \1,\2 ', output)

    return output


def clean_transcript(text_input):
    """
    Removes filler words from transcript and any repeat words, fixes spelling errors and adds capitalization that is
    previously hard coded. Also formats any time strings.
    :return:
    """
    import itertools
    import json
    import re

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

    # join all text
    fix_title = ' '.join(fix_title)

    # fix spelling
    spelling_words = data.get('spelling')
    regex = re.compile("|".join(map(re.escape, spelling_words.keys())))
    text_output = regex.sub(lambda match: spelling_words[match.group(0)], fix_title)

    # capitalize proper nouns
    text_output = proper_noun_capitalizer(text_output)

    # fix time string formatting
    text_output = fix_time(text_output)
    return text_output, num_filler


def add_punctuation(text_input, iteration=None):
    """
    Using Punctuator2 from https://github.com/ottokart/punctuator2
    Breakdown the transcript chunk into sentences with grammar.
    :param text_input: transcript input
    :return: transcript input with grammar added
    @param text_input:
    @param iteration: if True, then remove the commas to re-ad
    """
    # import re
    from punctuator import Punctuator

    # import default pre-trained model from punctuator
    p = Punctuator('Demo-Europarl-EN.pcl')

    if iteration is None:
        sentences = p.punctuate(text_input)
    else:
        # remove existing commas
        # text_input = re.sub(r'\.(?!\d)', '', text_input)
        # text_input = re.sub(r'\,(?!\d)', '', text_input)

        # remove lingering repeated word

        sentences = p.punctuate(text_input)

        # fix duplicate punctuation
        sentences = sentences.replace(' .', '.')
        sentences = sentences.replace(' :', ':')
        sentences = sentences.replace(' ,', ',')
        sentences = sentences.replace('  ,', ',')
        sentences = sentences.replace(', ,', ',')
        sentences = sentences.replace(', :', ',')
        sentences = sentences.replace(', .', ',')
        sentences = sentences.replace(' ,,', ',')
        sentences = sentences.replace('. .', '.')
        sentences = sentences.replace('.,', '.')
        sentences = sentences.replace(',-', '-')
        sentences = sentences.replace('??', '?')
        sentences = sentences.replace('?,', '?')
        sentences = sentences.replace(',?', '?')
        sentences = sentences.replace('?,', '?')
        sentences = sentences.replace('?.', '?')
        sentences = sentences.replace('.?', '?')
        sentences = sentences.replace('!!', '!')
        sentences = sentences.replace(',!', '!')
        sentences = sentences.replace('::', ':')
        sentences = sentences.replace(':.', ':')
        sentences = sentences.replace(',:', ',')
        sentences = sentences.replace(',.', '.')
        sentences = sentences.replace(':,', ',')
        sentences = sentences.replace(',;', ';')
        sentences = sentences.replace('-,', ',')
        sentences = sentences.replace('.-', '.')
        sentences = sentences.replace(': ,', ':')
        sentences = sentences.replace('..', '.')
        sentences = sentences.replace(',,', ',')

    return sentences


def text_length(text_input):
    import readtime
    length = readtime.of_text(text_input)
    return length


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

    # remove the vague words
    vague_words = ['organizations', 'priorities', 'point', 'points', 'letters', 'community', 'area', 'issues', 'lot',
                   'meeting',
                   'district', 'issue', 'people', 'application', 'process', 'applicants', 'process', 'comments',
                   'committee', 'committees', 'things', 'thing', 'members', 'office', 'letter', 'board', 'city', 'time',
                   'borough',
                   'question', 'way', 'application', 'resolution', 'questions', 'year', 'site', 'number', 'folks',
                   'support', 'group', 'sort', 'recommendations', 'recommendation', 'items', 'co', 'a.m.', 'p.m.',
                   "A.M.", "P.M.", "districts", "use", "presentation", "tonight", "majority", "meetings", "discussion",
                   "couple", "hand", "hands", "stuff"]
    vague_counter = collections.Counter()
    for i in vague_words:
        value = noun_counter.get(i)
        vague_counter[i] = value
        noun_counter.pop(i, None)
    [print(f"Removing {i[0]} from top words") for i in vague_counter.items() if i[1] is not None]
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

    # match on processed text
    important_sentences = []
    for sent in processed_text.sents:
        for match_id, start, end in phrase_matcher(nlp(sent.text)):
            if sent.text not in important_sentences:
                for i in range(len(nlp_list)):
                    if nlp.vocab.strings[match_id] in [nlp_list[i]]:
                        important_sentences.append(sent.text)
            else:
                continue
    # remove duplicate sentences and join
    #all_sents = list(dict.fromkeys(important_sentences))
    all_sents = important_sentences
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
