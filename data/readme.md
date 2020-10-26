As we have discussed in Section \ref{datacllection} and Section \ref{sentimentapproach}, each tweet is annotated with **'Positive'**,**'Negative'**, **'Neutral'**, and **'Mixed'** sentiment classes. The 9.4k annotated tweets are further split into training, development, and test instances using an 80:10:10 split. We have used the development dataset to optimize the learning algorithms. All the results reported in the remaining sections are based on the test dataset instances.  

After error analysis, we found out that tweets annotated with the **'Mixed'** are noises, which can be regarded as **'Positive'**, '**Negative'**, and **'Neutral'**. Hence, we further cleanse the dataset and exclude tweets labeled as **'Mixed'**, which leads to a final dataset of size 8.6k tweets.  We follow the same split and report the results accordingly (see column 'Cleaned' in Table \ref{expresults}).

File structure

train.csv
Contains the training set. The first column (twee_it) shows the id of the tweet and the second column contians the label of that specific tweet. 

test.csv
Contains the test set. The first column (twee_it) shows the id of the tweet and the second column contians the label of that specific tweet. 

dev.csv
Contains the development set. The first column (twee_it) shows the id of the tweet and the second column contians the label of that specific tweet. 

ow to access tweet using their id from the dataset

https://twitter.com/evan_greer/status/#tweet_id

Replace '#tweet_id' with any id from the dataset. 
