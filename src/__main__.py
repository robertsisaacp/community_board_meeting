if __name__ == "__main__":
    transcript_id = input('Enter id from Youtube link:')
    video_url = f"https://www.youtube.com/watch?v={transcript_id}"

    print(f'Obtaining transcript for {transcript_id}')
    meeting = get_transcript(transcript_id)
    print('Transcript obtained!')
    print('Removing uh any um filler words')
    meeting = clean_transcript(meeting)
    print('Splitting into Sentences, adding punctuation')
    summary_input = add_punctuation(meeting)
    print('Sentences ready for summarization.')
    print('Saving file output')
    ratio_of_transcript = .10
    summary_output = summarize_text(summary_input, ratio_of_transcript)
    print('Your Community Board transcript is ready!')
    output_transcript()