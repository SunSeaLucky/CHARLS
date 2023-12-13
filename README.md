# CHARLS
## Introduction
This project is serving for my college project - **Innovative Entrepreneurship Program for University Students**. For the rest of the part, I will clarify the process of processing data in detail.

## Data preprocessing
### Before that
I select the year of 2011 ~ 2015 in CHARLS to process. And in the first part, we need to determine which indicators are needed to be selected. That's depend on the scale we use (**MMSE** and **PFP**).

MMSE is some kind of very excellent scale. However, a part of indicators **DOES NOT** appear in the data provided by CHARLS.

But there seems no more scale to choose. So I'd to choose some indicator that **I think are good** from the vast array of indicators. Don't worry, I also do a verification to ensure that the indicators I choose are fitting.

PFP is good for us and all indicators it needs are perfectly appear in the fucking database CHARLS!

### Choose fitting indicator
This is an extremely boring process. The key point is: if one indicator is missing in CHARLS, just find any other indicator *seemingly* right to replace the former indicator.

For example, if the indicator `Please repeat '44 stone lions'` which is a tongue-twister in Chinese to test the verbal ability is missing, I will find other indicators like below:
- DA005 Speech impediment
- DA007 Memory-related disease
- DA056 Interacted with friends & Played Ma-jong, played chess, played cards, or went to community club

In this section, some indicators like `DA005` are positive, while some indicators are negative. Given this, I set a weight manually. It may not as exact as it really is, so I will try to confirm its validity.

After such operation, I'v successfully extract 78 indicators which can almost accurately replace the indicators which are not in CHARLS.

The following is the detailed choosing process:

|Former Indicator|Replaced By|
|-|-|
|dc007_w4|dc004|
|dc008_w4|dc004|
|dc009_w4|dc004|
|dc010_w4|dc004|
|dc012_w4|dc004|
|dc013_w4_1_s1|dc027s1, dc027s2, dc027s3|
|dc013_w4_1_s2|dc027s4, dc027s5, dc027s6|
|dc013_w4_1_s3|dc027s7, dc027s8, dc027s9|
|dc014_w4_1_1|dc019|
|dc014_w4_2_1|dc020|
|dc014_w4_3_1|dc021|
|dc014_w4_4_1|dc022|
|dc014_w4_5_1|dc023|
|dc015_w4_s1|dc027s1, dc027s2, dc027s3|
|dc015_w4_s2|dc027s4, dc027s5, dc027s6|
|dc015_w4_s3|dc027s7, dc027s8, dc027s9|
|dc016_w4|da007, da008, da013, da016, da018, da019|
|dc017_w4|da007, da008, da013, da016, da018, da019|
|dc018_w4|da005, da007, da017, da056|
|dc019_w4|db009|
|dc020_w4|db007|
|dc021_w4|db006|
|dc022_w4|da032, da033, da034, da056_w3, db006|
|dc023_w4|da056_w3, db009|
|dc024_w4|dc025|


### Confirm the validity of indicators we have chosen

I use the `Verify.py` in directory `IndicatorVerification`, you can see it easily in this project. It extract MMSE's all indicators (Yes, the data for the year of 2018 is complete) and the indicators we just choose, calculating the cognitive impairment score respectively. Then compare scores for same person respectively.

The result shows that pearson correlation coefficient between the scores of the new method and the scores of the MMSE scale is **above 0.8**.


