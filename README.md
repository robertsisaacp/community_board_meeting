# Community Board Meeting Transcripts
Source for obtaining the transcript from a Community Board meeting. 

Currently this script will import the Youtube recorded transcript from a Community Board meeting and summarize the meeting into a short summary.

Youtube recordings are very helpful in downloading the raw text from a video. However there is no punctuation added. In order to transform the meeting into a summary, we needed to add punctuation. I use puncutator to automatically add in puncutation.

Once we have a more grammatical text corpus, I used Gensim's summarization to automatically create a summary that can be easily circulated throughout the community.

Next Steps:

- [ ] Output video information, such as meeting title

- [ ] Save textfile in more easy to read format

- [ ] Connect to email generator so community can read about the meeting by subscribing

- [ ] Remove some boilerplate language from community board meeting transcript such as introductions?


