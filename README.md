# NYC Community Board Meeting Minutes -NLP & Civic Tech
<i>A public written record of meeting transcript and summary</i>

Sarah Sachs and Brandon Pachucua

This project seeks to create a tool for the community to stay informed about their local Community Board meetings. 

Currently this script will import the Youtube recorded transcript from a Community Board meeting and summarize the meeting into a short summary.

Youtube recordings are very helpful in downloading the raw text from a video. However there is no punctuation added. In order to transform the meeting into a summary, we needed to add punctuation. I use puncutator to automatically add in puncutation.

Once we have a more grammatical text corpus, I used Gensim's summarization to automatically create a summary that can be easily circulated throughout the community.

### Requirements:

Download punctuator model from: https://drive.google.com/uc?id=0B7BsN5f2F1fZd1Q0aXlrUDhDbnM

This script uses Demo-Europarl-EN.pcl


### Next Steps:

- [ ] Launch API

- [ ] Automate collection of Community Board transcript link

- [ ] Connect API to email service provider

- [ ] Improve extractive summarization quality 

- [ ] Develop abstractive summarization 

- [ ] Compile list of Community Board members/participants 

### Citations:

Pulling Transcript from Youtube:

https://pypi.org/project/youtube-transcript-api/

Adding Punctuation:

https://pypi.org/project/punctuator/

Punctuator Model
@inproceedings{tilk2016,
  author    = {Ottokar Tilk and Tanel Alum{\"a}e},
  title     = {Bidirectional Recurrent Neural Network with Attention Mechanism for Punctuation Restoration},
  booktitle = {Interspeech 2016},
  year      = {2016}
}

Summarization of Text:
https://radimrehurek.com/gensim/summarization/summariser.html
