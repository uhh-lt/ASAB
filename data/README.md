<div align="justify">Each tweet is annotated with <b>'Positive'</b>,<b>'Negative'</b>, <b>'Neutral</b>, and <b>'Mixed'</b> sentiment classes. The 9.4k annotated tweets are further split into training, development, and test instances using an 80:10:10 split. We have used the development dataset to optimize the learning algorithms. All the results reported in the remaining sections are based on the test dataset instances.  </div> <br>

<div align="justify">After error analysis, we found out that tweets annotated with the <b>'Mixed'</b> are noises, which can be regarded as <b>'Positive'</b>, <b>'Negative'</b>, and <b>'Neutral'</b>. Hence, we further cleanse the dataset and exclude tweets labeled as <b>'Mixed'</b>, which leads to a final dataset of size 8.6k tweets.  </div>

### File structure

##### train.csv
 
Contains the training set, including the ids and labels of tweets.  

##### test.csv

Contains the test set, including the ids and labels of tweets.  

##### dev.csv

Contains the development set, including the ids and labels of tweets.  

#### Accessing tweet using their id from the dataset

https://twitter.com/evan_greer/status/#tweet_id

Replace '#tweet_id' with any id from the dataset. 
