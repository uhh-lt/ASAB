# ASAB
![Drag Racing](sentiment_XC5_icon.ico)
Amharic Sentiment Annotator Bot (ASAB)

#### ASAB: is the first of its kind to conduct surveys based on a specific reward scheme, which is mobile card vouchers.




# Abstract

**Sentiment analysis** is an important NLP application. As the number of social media users is ever-increasing, social media platforms would like to understand the latent meaning and sentiments of a text to enhance decision-making procedures. However, **low resource languages** such as **Amharic** have received less attention due to several reasons such as lack of well-annotated datasets, unavailability of computing resources, and fewer or no expert researchers in the area.

This work addresses three main research questions. We first explore the suitability of **existing tools** for the sentiment analysis task. There are no **tools** to support large-scale annotation tasks in Amharic. Also, the existing **crowdsourcing** platforms do not support Amharic text **annotation**. Hence, we build a social-network-friendly annotation tool called **ASAB** using the **Telegram bot**. 

We have collected **9.4k tweets**, where each tweet is annotated by **three** **Telegram** users. Secondly, we explore the suitability of machine learning approaches for Amharic sentiment analysis. The FLAIR deep learning text classifier, based on **network embeddings** that are computed from a **distributional thesaurus**, outperforms other supervised classifiers. Lastly, we have investigated the challenges in building a sentiment analysis system for Amharic and we found that the widespread usage of **sarcasm** and **figurative speech** are the main issues in dealing with the problem. 

# Components
## Annotator
Details about the ASAB annotator tools are available in the [ASAB annotator](annotator/readme.md)

The annotation instruction and examples are available [here](https://annotation-wq.github.io/)

If you want to test ASAB (without rewards, obviously), you can access  it from [telegram](https://t.me/Hizevbot)
## Model
# How to use it

### Citation

If you use these resources and methods, please cite the following paper:

```
@InProceedings{yimametalcoling2020,
  author    = {Seid Muhie Yimam and Hizkiel Mitiku Alemayehu and Abinew Ayele and Chris Biemann },
  title     = {Exploring Amharic Sentiment Analysis from Social Media Texts: Building Annotation Tools and Classification Models},
  booktitle = {The 28th International Conference on Computational Linguistics (COLING 2020) },
  year      = {2020},
  address   = {Barcelona, Spain},
  pages     = {to apear}
}
```
