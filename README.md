<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://blockparty.emptybox.io/">
    <img src="images/block_party_logo.png" alt="block party" width="80" height="80">
  </a>

  <h3 align="center">Block Party</h3>
  <p align="center">
    <i>Making local policy information accessible and byte-sized</i>
    <br/>
    <br/>
    A public written record of community board meeting transcript and summary.
    <br/>
    <br />
    <a href="https://blockparty.emptybox.io/"><strong>Explore transcripts »</strong></a>
    <br />
    <br />
    <a href="https://medium.com/@sarah_june42/nyc-community-board-meeting-minutes-nlp-civic-tech-8b5d9e4716d9">Medium</a>
    ·
    <a href="https://twitter.com/my_block_party">Twitter</a>
    ·
    <a href="mailto:blockparty.meeting@gmail.com?subject = Feedback&body = Message">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project
<strong>Community Board Meeting Minutes - NLP & Civic Tech</strong>

block party makes local policy information accessible and byte-sized, with a weekly email of your community board’s most recent meeting synopsis and transcript data. 

block party generates summarizations of community board meetings directly from transcript data collected from YouTube.

Here's How:
* Collect closed captions from YouTube recordings of community board meetings
* Clean text and add grammar
* Extract key content and automatically generate summary

### Built With: 

1. Pull Transcript from Youtube

    https://pypi.org/project/youtube-transcript-api/

2. Add Punctuation and grammar

    https://pypi.org/project/punctuator/

    <strong>Punctuator Model</strong>

    Ottokar Tilk and Tanel Alum{\"a}e},
    Bidirectional Recurrent Neural Network with Attention Mechanism for Punctuation Restoration,
    Interspeech 2016

3. Extract key content
    
    Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing.

4. Summarize Text
    https://radimrehurek.com/gensim/summarization/summariser.html

<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Sarah Sachs: [@sarah_june42](https://twitter.com/sarah_june42) 

Brandon Pachucua  

Project Link: [https://github.com/sarahJune1/community_board_meeting](https://github.com/sarahJune1/community_board_meeting)