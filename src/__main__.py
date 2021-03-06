from src.create_summary import *
from src.squeegee import *

if __name__ == "__main__":
    # Call in list of url strings from csv file
    all_ids = get_video_list(delta=True)
    processed_ids = []
    print(f'Getting transcripts for {len(all_ids)} Community Board meetings')
    progress_batch = 0
    total_in_queue = len(all_ids)
    for i in range(len(all_ids)):
        print("Progress: ")
        print(f'{progress_batch} ids processed, out of {len(all_ids)} Community Board meetings queued')
        print(f'{total_in_queue} ids in queue')
        print(f'Obtaining transcript for https://www.youtube.com/watch?v={all_ids[i]}')
        transcript_id = all_ids[i]
        video_url = f"https://www.youtube.com/watch?v={transcript_id}"
        print(f'Obtaining transcript for {transcript_id}')
        try:
            meeting = get_transcript(transcript_id)
            print('Transcript obtained!')
            processed_ids.append(transcript_id)
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print('Transcript failed!')
            continue
        print('Cleaning Transcript...')
        meeting, num_filler = clean_transcript(meeting)

        print('Splitting into Sentences, adding punctuation')
        print('Adding Punctuation')
        summary_input = add_punctuation(meeting)

        print("Get phrase_list:")
        phrase_list_intermediary_summary = phrase_maker()
        print('Filter to sentences with key content first time')
        key_sentences = phrase_list(summary_input, phrase_list_intermediary_summary)

        print('Filter to sentences with key content second time')
        key_sentences = iterate_summary_input(key_sentences, phrase_list_intermediary_summary)

        print('Sentences ready for Summarization.')
        # summarization
        ratio_of_transcript = .10
        try:
            summary_output = summarize_text(key_sentences, ratio_of_transcript)
            print('Saving file output')
        except ValueError:
            summary_output = ""
        youtube_metadata, cb_metadata = get_video_metadata(transcript_id)
        output_transcript(transcript_id, summary_input, summary_output, ratio_of_transcript, youtube_metadata)

        print('Your Community Board transcript is ready!')

        # get word count frequency
        print('Analyzing most frequent nouns')
        full_word_count = noun_counter(summary_input, 10)
        summary_word_count = noun_counter(summary_output, 10)
        # generate json for database
        print('Generating json object')

        make_json(transcript_id, youtube_metadata, cb_metadata, summary_input, summary_output, full_word_count,
                  summary_word_count, num_filler)
        # Add to progress bar
        progress_batch = progress_batch + 1
        total_in_queue = total_in_queue - 1

    if total_in_queue != 0:
        print(f"Left {total_in_queue} ids in queue:")
        print(list(set(all_ids) ^ set(processed_ids)))
    else:
        print('All ids processed.')
