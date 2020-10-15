#### ASAB: is the first of its kind to conduct surveys based on a specific reward scheme, which is mobile card vouchers.

File Organization

#### 10birr.txt

Is a text file that contain a list of ten birr mobile card voucher numbers. 

|                 |
|-----------------|
| 456789456715... |
| 246794123116... |


#### 5irr.txt

Is a text file that contain a list of ten birr mobile card voucher numbers. 

|                 |
|-----------------|
| 781641319456715... |
| 246794123118906... |

#### annotated_tweets.csv

Is a csv file that used for stoting the annotated data.  It is consists of four columns namely:
- tweet_id - The id of the tweet
- sentiment - The sentiment classification of the tweet
- tweet - The text content of the tweet
- username - The telegram username of the user


| tweet_id | sentiment | tweet | username |
|----------|-----------|-------|----------|
|          |           |       |          |


#### blocked_user.txt

Is a text file that stores list of blocked users. 

|                  |
|------------------|
| blocked username |

#### bot.properties

This file consists of the token of the bot,the email address of the admin for receiving emails from the bot and users,  password of the email address. All the defualt data for all the three requirements should be replace with the right information before running the bot.py. 

- TOKEN = Insert here the token of your bot
- EMAIL =  Insert here the email address that will used for receiving emails from the bot and the users
- PASSWORD = Insert here the password for your eamil.

#### control_answers.csv

Consists the answer a user gave to the control questions.  It has three columns

- tweet =  The text content of the tweet.
- answer = The answer of the user for that specific tweet.
- username = The useranme of the respective user.

| tweet                  | answer | username |
|------------------------|--------|----------|
| ይህንን ይህንን መኪና እወዳለሁ ፡፡ | Pos    | username |


#### control_questions.csv

It is a csv file that stores the simple questions for verification of a user. Consists two columns one for the tweet and the other for the sentiment of the respective tweet.

| tweet                  | class |
|------------------------|-------|
| ይህንን ይህንን መኪና እወዳለሁ ፡፡ | Pos   |

#### raw_tweets.csv

Contains all the tweets to be annotated. It has two columns one for the list of tweets and the other one for their respective ID. 

| tweet_id     | tweet      |
|--------------|------------|
| 4564644..... | some tweet |

#### rewarded_cards.txt

It is a file that stores all the mobile voutcher numbers that are awarded to the winners. 

requirement.txt
Contains all the libraries that are required to run bot.py. 

#### Directory Structure

```
├── annotator
│   ├── css
│   ├── 10birr.txt
│   ├── 5birr.txt
│   ├── annotated_tweets.txt
│   ├── blocked_user.txt
│   ├── bot.properties
│   ├── bot.py
│   ├── control_answers.csv
│   ├── control_questions.csv
│   ├── raw_tweets.csv
│   ├── requirements.txt
│   ├── rewarded_cards.csv
│   ├── readme.md
```


[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/


  

