from src.create_summary import *
from src.squeegee import phrase_list

if __name__ == "__main__":
    # Call in list of url strings from csv file
    all_ids = get_video_list()
    print(f'Getting transcripts for {len(all_ids)} Community Board meetings')
    for i in range(len(all_ids)):
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
        meeting = clean_transcript(meeting)

        if transcript_formatted is False:
            print('Splitting into Sentences, adding punctuation')
            print('Adding Punctuation')
            summary_input = add_punctuation(meeting)
        else:
            # if already formatted, just keep as is
            print('Already split into sentences, transcript aggregated')
            summary_input = meeting

        print('Filter to sentences with key content')
        key_sentences = phrase_list(summary_input)

        print('Sentences ready for Summarization.')
        # summarization
        ratio_of_transcript = .10
        summary_output = summarize_text(key_sentences, ratio_of_transcript)
        print('Saving file output')

        output_transcript(transcript_id, summary_input, summary_output, ratio_of_transcript)

        print('Your Community Board transcript is ready!')