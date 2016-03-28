# HiBot ChatBot

![version](https://img.shields.io/badge/version-v0.1.0-blue.svg "version v0.1.0")
![license](https://img.shields.io/badge/license-CC_BY--ND-blue.svg "license CC BY-ND")

## Prototype ChatBot Specifications

The Consultant will create a prototype chatbot to be used with preliminary
synthetic data (hereafter the “Data Science Project”). The goal of the Data
Science Project will be to build a modular chatbot that can accommodate
independently generated data (e.g., data gathered by the Company related to
different market segments) formatted into JSON files, using either IBM's
Bluemix, or another framework suggested by the Consultant.

The Consultant will familiarize himself with IBM's Bluemix framework in order
to evaluate how it compares to the tools necessary to perform the Data Science
Project.

The Consultant estimates a maximum of 160 hours worth of work will be required
to complete the Data Science Project, all of which will be billable to the
Company. This work will be divided by week into the following scheme:

*   Weeks 1 & 2: chatbot engine:

  + 60 hours: Develop chatbot engine with with weather and movie scenario
implementation;

  + 20 hours: Integrate chatbot with existing frontend and backend
infrastructure.

*   Weeks 3 & 4: Integrate user history:

  + 40 hours: Develop recommendation system based on user history;

  + 40 hours: Develop user segmentation model based on user history.

Depending on the desired complexity of the prototype, any changes to the
requirements by the Company, and/or the successful completion of the Data
Science Project before the four week deadline, the Company can instruct the
Consultant to work more or less hours than aforementioned.

The Consultant will conduct the following activities in the course of the Data
Science Project:

1.  chatbot Development: build the chatbot’s engine using the Python
framework.

  a. Natural Language ToolKit: leading platform for building Python programs to
  work with human language data.

  b. Modular Architecture: in order to facilitate the further creation and usage
  of different pluggable modules related to storage, IO, and logic.

  c. AIML: depending on time constraints, and the desire of the Company, the
  prototype may include this component related to the Artificial Intelligence
  Markup Language, developed by Richard Wallace for a chatbot called
  A.L.I.C.E. (Artificial Linguistics Internet Computer Entity) which won several
  artificial intelligence awards.

2.  Scenario Examples:

  <DL>
    <DT>Dialog:</DT>
      <DD>user: Good morning! How are you doing?</DD>
      <DD>bot: I am doing very well, thank you for asking.</DD>
      <DD>user: You're welcome.</DD>
      <DD>bot: Do you like hats?</DD>

    <DT>Weather:</DT>
      <DD>user: What’s the weather in Boston?</DD>
      <DD>bot: The forecast for Boston is ...</DD>

    <DT>Movies</DT>
      <DD>user: What are the movies in New York City?</DD>
      <DD>bot: The movies in NYC are ...</DD>
  </DL>

3.  Integrated User History: enhance chatbot’s interaction by incorporating
user history.

  a. Recommendation system: by using the collected history and known
  demographics of all known users, a recommendation system can be built. This
  system will enable the chatbot to recommend suggestions to the user through
  either an iter-based or user-based collaborative filtering algorithm. For
  example, the algorithm will suggest that the user purchase a particular
  cellular plan based on their previous history and their similarity to other
  users.

  b. User segmentation model: by using the collected history and known
  demographics of all known users, a segmentation model can be built based on
  hierarchical clustering. Being assigned to a specific cluster will enable the
  chatbot to make more targeted suggestions for the users. For example, if a
  user is in a particular cluster the chatbot will know to recommend a
  certain type of movie.

4.  Investigate the Company’s proposed updates to the chatbot and, if time
and data permits, implement these changes.

## Self-Hosting Python Solution

1.  HiBot ChatBot latest stable release: v0.1.0.

2.  Installation:

  ```bash
  $ pip install --upgrade pip
  $ pip install -r requirements.txt
  $ python -m textblob.download_corpora

  # To run using mongodb
  $ brew install mongodb
  $ sudo mkdir -p /data/db
  $ sudo mongod
  ```

3.  Basic Usage and Testing: All examples are found within example/ folder

  Testing of the installed code can be performed as follows:

  ```python
  from os import sys, path
  sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

  from chatbot import ChatBot
  chatbot = ChatBot("HiBot")

  # Train based on the english corpus
  chatbot.train("chatbot.corpus.english.greetings")
  chatbot.train("chatbot.corpus.english.conversations")
  chatbot.train("chatbot.corpus.english.trivia")

  # Get a response to an input statement
  chatbot.get_response("Good morning! How are you doing?")

  u'I am doing well, how about you?'
  ```

  chatbot's built in tests can be run using `nose`:

  ```bash
  $ cd ./path/to/project
  $ nosetests
  ```

4.  Training Data:
  chatbot comes with a data utility module that can be used to train chat
  bots. Data files are in the chatbot/corpus directory.

  ```python
  # Train based on the english corpus (this should only be done if using MongoDB for storage)
  chatbot.train("chatbot.corpus.english")

  # Train based on english greetings corpus
  chatbot.train("chatbot.corpus.english.greetings")

  # Train based on the english conversations corpus
  chatbot.train("chatbot.corpus.english.conversations")

  # Train based on the AIML atomic corpus
  chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.atomic")
  ```

  The first time the Chatbot is ran, a database will be created with all available responses based on the training data.
  This is a timely operation and will inhibit the user for quickly interacting with the Chatbot. Therefore, the following
  sequence is recommend.

  a. Create a MongoDB database and train on full corpus:
  ```python

  # Initialize Chatbot
  chatbot = ChatBot("HiBot", read_only=False,
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    database="chatterbot-database")

  # Train based on the english corpus
  chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.atomic")

  response = chatbot.get_response("welcome")
  ```

  b. For subsequent conversations, use Chatbot in read_only mode and provide no training
  ```python

  # Initialize Chatbot
  chatbot = ChatBot("HiBot", read_only=True,
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    database="chatterbot-database")

  response = chatbot.get_response("welcome")
  ```

5.  Teaching the Bot to learn:
  Chatbot comes with the utility that users can teach the bot about themselves.

  ```python
  chatbot = ChatBot("HiBot", read_only=True,
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    database="chatterbot-database")

  chatbot.get_response("Learn my name is Mike")
  ```

  In response you will see
  ```python
  'u[ChatBot]: Ok, I Learned your name is Mike'
  ```

  You can teach the Chatbot the following attributes by using this exact format
  ```python
  chatbot.get_response("Who am I")
  'u[ChatBot]: Your name is friend, you are 30 years old, you are a male, you live in Boston, you job is a Physicists, and you are great.'

  chatbot.get_response("Learn my name is Mike")
  chatbot.get_response("Learn my age is 29")
  chatbot.get_response("Learn my gender is male")
  chatbot.get_response("Learn my location is Boston")
  chatbot.get_response("Learn my personality is happy")
  chatbot.get_response("Learn my job is a Physicists")

  chatbot.get_response("Who am I")
  'u[ChatBot]: Your name is Mike, you are 29 years old, you are a male, you live in Boston, you job is a Physicists, and you are happy.'
  ```

  To save a user's attributes to a pickled file just call the following function with a desired file name
  ```python
  chatbot.save_user_attributes(file_name = 'user.pkl')
  ```

  To load a user's attributes back from the pickled file add a `user_profile` option to the ChatBot interface call.
  ```python
  # Train based on the english conversations corpus
  chatbot = ChatBot("HiBot", read_only=True,
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    database="chatterbot-database",
    user_profile="user.pkl")
  ```
  This will allow you to store and reuse all attributes that you learn about a user.


## Getting Started with Git and GitHub

* Simple guide to [Git](https://rogerdudler.github.io/git-guide).
* Simple guide to [GitHub](https://guides.github.com).

## Versioning Large Files

Git Large File Storage (Git LFS) is an open-source extension to Git that allows you to work with large files the same way as any other text file.

With Git LFS, you and your repository's contributors can clone large files from the Git command line, open pull requests, and comment on the diffs. It's the ideal solution for pushing files to GitHub that are larger than 100 MB.

For more information on Git LFS, visit https://git-lfs.github.com.

With Git LFS enabled, you'll be able to fetch, modify, and push large files just as you would expect with any file that Git manages. However, a user that doesn't have Git LFS will experience a different workflow.

If collaborators on your repository don't have Git LFS installed, they won't have access to the original large file. If they attempt to clone your repository, they will only fetch the pointer files, and won't have access to any of the actual data.

## Authors

@danieldf, @msegala.

## Licensing

[![CC-BY-ND](https://licensebuttons.net/l/by-nd/4.0/88x31.png)](https://creativecommons.org/licenses/by-nd/4.0/)

To the extent possible under the law, and under our agreements,
[SFL Scientific](http://sflscientific.com/) retains all copyright and related
or neighboring rights to this work.
