from src.create_summary import *
from src.squeegee import *

if __name__ == "__main__":
    # Call in list of url strings from csv file
    all_ids = get_video_list()
    print(f'Getting transcripts for {len(all_ids)} Community Board meetings')
    progress_batch = 0
    total_in_queue = len(all_ids)
    for i in range(len(all_ids)):
        print("Progress: ")
        print(f'{progress_batch} ids processed, out of {len(all_ids)} Community Board meetings queued')
        print(f'{total_in_queue} ids in queue')
        print(f'Obtaining transcript {all_ids[i]}')
        transcript_id = all_ids[i]
        video_url = f"https://www.youtube.com/watch?v={transcript_id}"
        print(f'Obtaining transcript for {transcript_id}')
        try:
            meeting, transcript_formatted = get_transcript(transcript_id)
            print('Transcript obtained!')

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print('Transcript failed!')
            continue
        print('Removing uh any um filler words')
        meeting, num_filler = clean_transcript(meeting)

        if transcript_formatted is False:
            print('Splitting into Sentences, adding punctuation')
            print('Adding Punctuation')
            summary_input = add_punctuation(meeting)
        else:
            # if already formatted, just keep as is
            print('Already split into sentences, transcript aggregated')
            summary_input = meeting

        print('Filter to sentences with key content first time')
        key_sentences = phrase_list(summary_input)

        print('Filter to sentences with key content second time')
        key_sentences = iterate_summary_input(key_sentences)

        print('Sentences ready for Summarization.')
        # summarization
        ratio_of_transcript = .10
        summary_output = summarize_text(key_sentences, ratio_of_transcript)
        print('Saving file output')
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