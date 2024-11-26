<h1 align="center">
  🤖 EnigmaV3 - A music recommender bot for Discord
  
 [![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
</h1>

<div align="center">

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DOI](https://zenodo.org/badge/533639670.svg)](https://zenodo.org/badge/latestdoi/533639670)
[![Build Status](https://github.com/ForkBombers/Enigma/actions/workflows/github-actions-build.yml/badge.svg)](https://github.com/ForkBombers/Enigma/actions)
[![GitHub Release](https://img.shields.io/github/release/ForkBombers/Enigma.svg)](https://github.com/ForkBombers/Enigma/releases)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/ForkBombers/Enigma.svg)](https://img.shields.io/github/repo-size/ForkBombers/Enigma.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub contributors](https://img.shields.io/badge/contributors-3-green)](https://github.com/ForkBombers/Enigma#--contributors--)
[![Open Issues](https://img.shields.io/badge/issues-0-yellow)](https://github.com/ForkBombers/Enigma/issues?q=is%3Aopen+is%3Aissue)
[![Pull Requests](https://img.shields.io/badge/pull%20requests-0-yellow)](https://github.com/ForkBombers/Enigma/pulls)
[![YAPF](https://img.shields.io/badge/code%20style-yapf-ff69b4)](https://github.com/ForkBombers/Enigma/blob/main/.github/workflows/code-formatter.yml)
![Supports Python](https://img.shields.io/pypi/pyversions/pytest)
[![Formatting python code](https://github.com/ForkBombers/Enigma/actions/workflows/code-formatter.yml/badge.svg)](https://github.com/ForkBombers/Enigma/actions/workflows/code-formatter.yml)
[![codecov](https://codecov.io/gh/rahulgautam21/Enigma/branch/main/graph/badge.svg?token=OEPEJ0W8CR)](https://codecov.io/gh/rahulgautam21/Enigma)

</div>

<p align="center">
    <a href="https://github.com/rohit-sram/Enigma/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/rohit-sram/Enigma/issues">Request Feature</a>
</p>
</br>

<h1> 🎼 FEATURES </h1>

<div>
<ul>
  <li>Recommend songs based on user input and play them on discord voice channel</li>
  <li>Can be used in chat rooms by teams, friends, organizations to encourage a 'sound' environment </li>
  <li>Capability to toggle music pause/resume</li>
  <li>Capability to play any song- requires no youtube search</li>
  <li>Capability to switch back and forth between songs</li>
  <li>Capability to shuffle songs in queue</li>
  <li>Authorize specific channels for the bot to access</li>
  <li>Acts as an amplifier - can be used to play same music on multiple speakers to give a surround sound effect and increase volume output</li>
</ul>


</div>
  
<h1> 📣 V3 : New Features </h1>

<div>
<ul>
  <li>Added a new functionality to add a custom song to the queue</li>
  <li>Added a new functionality to shuffle the songs within the queue</li>
  <li>A play feature to continue playing from queue</li>
  <li>Reconnect command to reconnect to VC</li>
  <li>Added authorization feature for channels and roles</li>
  <li>Made Enigma accessible on Linux and Windows</li>  <!-- maybe add it at the top LATER? -->
</ul>
</div>

If you want to get added to the music server on discord to test the bot, drop an email to rsriram3.edu

<h1> ⚒️ Installation Procedure </h1>


## 1. Prerequisites 

  * Install FFMPEG from [FFMPEG builds](https://www.gyan.dev/ffmpeg/builds), extract it and add it to your path [How to add FFMPEG to Path](https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10#:~:text=Add%20FFmpeg%20to%20Windows%20path%20using%20Environment%20variables&text=In%20the%20Environment%20Variables%20window,bin%5C%E2%80%9D%20and%20click%20OK.)

## 2. Running Code

First, clone the repository and cd into the folder:

```
$ git clone https://github.com/rohit-sram/Enigma.git
```

Alternatively, clone repo using SSH keys,
  ```
  $ git clone git@github.com:rohit-sram/Enigma.git
  ```
```
$ cd Enigma
```

### Create a .env file for Discord token: 
Use the following format `DISCORD_TOKEN=#SECRET_TOKEN#`
<!-- ### Join the discord channel of the bot [Discord Channel of bot](https://discord.com/channels/1017135653315686490/1017135653789646850) and connect to the voice channel. -->

Install requirements 
```
$ pip install -r requirements.txt
```
Start the bot
```
$ python bot.py
```

You can now use the discord bot to give music recommendations! Use `]help` to see all functionalities of bot.


#### Note: Make sure the bot has the role `bot` and the user has the role `DJ` 

<h1> 🚀 Demo </h1>


https://user-images.githubusercontent.com/20087273/194780603-f163caf6-2c9e-4d74-8fbd-c93f30e8935a.mp4

<h1> 🚀 Demo 2 - Group 17 </h1>


https://user-images.githubusercontent.com/21155121/205782352-426dcee7-f145-43f1-af2e-a6eead2ccea3.mp4


<h1> 📍 Roadmap </h1>

What We've Done:
  * Enigma now works on Linux and Windows
  * Created a Discord Bot via the Discord Developer Portal.
  * Added functionalities to the Discord bot. Check [Features](https://github.com/rohit-sram/Enigma#--features-) above.
  * Call Enigma to voice channel to play music based on the user's requests.
  * Enigma plays songs without having to search on YouTube.
  * Added a lil more functionality to Enigma:
      * `]play` command to play from queue 
      * `]reconnect` to reconnect Enigma to Voice channel 
      * Enigma now checks for Authorized roles and channels

Scope for the future:
  * Make the song recommendations more sophisticated by using content-based recommender systems.
  * User profile integration with bot
  * Integrating likes and dislikes for profiled users- for potentially personalized recommendations.
  * Broader platform access(ubuntu, Android, iOS etc.)
  * More functionalitiies for the bot: 
      * Loop and replay features
      * Move a song within a queue or to the top of the queue
      * Jump to a specific song in the queue
  * A Dataset suggestion : ['Music Dataset (1950-2019)'](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019)

<h1> 📖 Documentation</h1>

Documentation for the code available at - <a href="https://saswat123.github.io/Enigma/">Enigma Docs</a>  


<h1> 👥 Contributors <a name="Contributors"></a> </h1>

### Group 86

<table>
  <tr>
    <td align="center"><a href="https://github.com/KaustubhAs"><img src="https://avatars.githubusercontent.com/u/58294503?v=4" width="75px;" alt=""/><br /><sub><b>Kaustubh Sonawane</b></sub></a></td>
    <td align="center"><a href="https://github.com/iamNikitaC"><img src="https://avatars.githubusercontent.com/u/87129562?v=4" width="75px;" alt=""/><br /><sub><b>Nikita Chaudhari</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/tejasdesai27"><img src="https://avatars.githubusercontent.com/u/139948226?v=4" width="75px;" alt=""/><br /><sub><b>Tejas Desai</b></sub></a><br /></td>
  </tr>

</table>

<h1> Contributing </h1>

Please see [`CONTRIBUTING`](CONTRIBUTING.md) for contributing to this project.

<h1> Data </h1>

The dataset for Enigma is present [here](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019)
You can find the dataset here <a href='https://www.kaggle.com/datasets/leonardopena/top-spotify-songs-from-20102019-by-year'>Top Spotify Songs (2010-2019)</a> which contains around 600 songs.

<h1> Support </h1>
For any support reach out to rsriram3@ncsu.edu








<!-- STASH -->

  <!-- * Incorporated a [dataset](https://www.kaggle.com/datasets/leonardopena/top-spotify-songs-from-20102019-by-year) to our application. -->


  <!-- * Extend the application to be deployed online (via a website or an application). -->

  <!-- * Alternatively, use [this](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019) as the primary data source to make better recommendations. -->
