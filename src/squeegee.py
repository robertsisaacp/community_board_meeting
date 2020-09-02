def word_counter(nlp_text):
    """
    Counts number of words
    """
    import spacy
    nlp = spacy.load('en_core_web_sm')

    # apply spacy nlp
    doc = nlp(nlp_text)

    # remove stopwords and punctuations
    words = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
    num_words = len(words)

    return num_words


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
    phrases = ['purpose', 'first', 'second', 'third', 'important', 'critical', 'success', 'failure',
               'unfortunate', 'pandemic', 'transparent', 'community', 'sick', 'concern', 'public',
               'homeless', 'safety', 'police', 'letter', 'petition', 'manage', 'support', 'access',
               'education', 'policy', 'situation', 'park', 'new york city', 'bureaucracy']

    # build vocabulary pattern
    patterns = [nlp(text) for text in phrases]
    # add list of phrases to A1 object
    phrase_matcher.add('A1', None, *patterns)

    # match on processed text
    processed_text = nlp(text)

    important_sentences = []
    for sent in processed_text.sents:
        for match_id, start, end in phrase_matcher(nlp(sent.text)):
            if nlp.vocab.strings[match_id] in ["A1"]:
                important_sentences.append(sent.text)
    # remove duplicate sentences and join
    all_text = " ".join(list(dict.fromkeys(important_sentences)))

    return all_text
