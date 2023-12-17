# CHARLS
## Introduction
This project is serving for my college project - IEPUS (Innovative Entrepreneurship Program for University Students). For the rest of the part, I will clarify the process of processing data in detail.

## Preprocessing
### Before that
I select the year of 2011 ~ 2015 in CHARLS (China Health and Retirement Longitudinal Study) to process. And in the first part, we need to determine which indicators are needed to be selected. That's depend on the scale we use (**MMSE** and **PFP**).

MMSE is some kind of very excellent scale. However, a part of indicators **DOES NOT** appear in the data provided by CHARLS.

But there seems no more scale to choose. So I'd to choose some indicator that **I think are good** from the vast array of indicators. Don't worry, I also do a verification to ensure that the indicators I choose are fitting.

PFP is good for us and all indicators it needs are perfectly appear in the fucking database CHARLS!

### Choose appropriate indicator
This is an extremely boring process. The key point is: if one indicator is missing in CHARLS, just find any other indicator *seemingly* right to replace the former indicator.

For example, if the indicator `Please repeat '44 stone lions'` which is a tongue-twister in Chinese to test the verbal ability is missing, I will find other indicators like below:
- DA005 Speech impediment
- DA007 Memory-related disease
- DA056 Interacted with friends & Played Ma-jong, played chess, played cards, or went to community club

In this section, some indicators like `DA005` are positive, while some indicators are negative. Given this, I set a weight manually. It may not as exact as it really is, so I will try to confirm its validity.

After such operation, I'v successfully extract 78 indicators which can almost accurately replace the indicators which are not in CHARLS.

The following is the detailed choosing relationship:

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

For the indicators left is not appear in CHARLS, it will be replaced by the indicators right. 
### How the indicators are calculated?
I believe that you must understand why some indicators are needed to be replaced by multiple indicators. So I'm going to explain how this indicators are calculated.

For `dc013_w4_1_s1`, `dc013_w4_1_s2` and `dc013_w4_1_s3` are replaced by `dc027si` (`i` stands for 1, 2, 3 etc.), `dc013_w4_1_s1` will be true if any of `dc027si` (`i` stands for 1, 2, 3) is true, `dc013_w4_1_s2` will be true if any of `dc027si` (`i` stands for 4, 5, 6) is true. What is exactly the same for `dc013_w4_1_s3`.

Well, there is a slightly different on `dc015_w4_si` (`i` stands for 1, 2, 3). For example, `dc015_w4_si` is true only when `dc027si`(`i` stands for 1, 2, 3) are all true.

For `dc016_w4` and `dc017_w4` are both set as the second way I mentioned above. So I won't explain it any more.

Let's discuss about `dc018_w4`. In my code, you can see the weight as below:
|Indicator|`da005`|`da007`|`da017`|`da056`|
|-|-|-|-|-|
|Weight|0.3|0.3|0.2|0.2|

After all the four indicators are calculated, if the sum of them is greater than 0.5, then we assume `dc018_w4` is true.

For `dc022_w4`:
|Indicator|`da032`|`da033`|`da034`|`da056_w3`|`db006`|
|-|-|-|-|-|-|
|Weight|0.2|0.2|0.2|0.3|0.3|

For `dc023_w4`:
|Indicator|`da056_w3`|`db009`|
|-|-|-|
|Weight|0.5|0.4|


### Confirm the validity of indicators we have chosen

I use the `Verify.py` in directory `IndicatorVerification`, you can see it easily in this project. It extract MMSE's all indicators (Yes, the data for the year of 2018 is full) and the indicators we just choose, calculating the cognitive impairment of new method and MMSE method score respectively. Then compare scores for the same person respectively.

The result shows that pearson correlation coefficient between the scores of the new method and the scores of the MMSE scale is **above 0.8**. So now we assume that new method can work as better as MMSE.


## Calculate
### Extract PFP indicators and calculate score
Get 1 score for each item:

| Indicator Name                                               | Indicator Code |
|--------------------------------------------------------------|----------------|
| Weight Measurement                                           | ql002          |
| Height                                                       | qi002          |
| Left Hand-1（kg）                                            | qc003          |
| Right Hand-1（kg）                                           | qc004          |
| Left Hand-2（kg）                                            | qc005          |
| Right Hand-2（kg）                                           | qc006          |
| Walking Speed Time-1                                         | qg002          |
| Repeat the Measurement                                       | qg003          |
| Do Vigorous Activities At Least 10 Minutes Continuously      | da051_1_       |
| Do Moderate Physical Effort At Least 10 Minutes Continuously | da051_2_       |
| Walking At Least 10 Minutes Continuously                     | da051_3_       |
| Could Not Get Going                                          | dc018          |
| Felt Everything I Did Was An Effort                          | dc012          |
### Calculate frail score
We divide the 13 indicators into 5 parts, which stands for the following 5 parts:
1. Weight Loss
2. Weakness
3. Slowness
4. Low Energy Expenditure
5. Exhaustion

And the criterion to judge wether somebody is frail or not is shown as below:
> ≥3/5 criteria met indicates frailty; 1-2/5 indicates pre-or-intermediate frailty; 0/5 indicates non-frail.

If you want to know any specific indicator is divided into which part, please refer to `Assets/DataPreproccessing.pdf`.
### Extract MMSE indicators and calculate score
Get 1 score for each item:

| Indicator Name                      | Indicator Code                           |
|-------------------------------------|------------------------------------------|
| Checking Year                       | dc001s1                                  |
| Checking Month                      | dc001s2                                  |
| Checking Date                       | dc001s3                                  |
| Checking Day of Week                | dc002                                    |
| Checking Season                     | dc003                                    |
| Checking State                      | dc004                                    |
| Checking County                     | dc004                                    |
| Checking City                       | dc004                                    |
| Checking Floor                      | dc004                                    |
| Checking Address                    | dc004                                    |
| Repeated Time 1: Ball               | dc027s1, dc027s2, dc027s3                |
| Repeated Time 1: Flag               | dc027s4, dc027s5, dc027s6                |
| Repeated Time 1: Tree               | dc027s7, dc027s8, dc027s9                |
| Specific Result from 100-7          | dc019                                    |
| Specific Result from dc014_w4_2-7   | dc020                                    |
| Specific Result from dc014_w4_3-7   | dc021                                    |
| Specific Result from dc014_w4_4-7   | dc022                                    |
| Specific Result from dc014_w4_5-7   | dc023                                    |
| Delayed Recall: Ball Flag Tree      | dc027s1, dc027s2, dc027s3                |
| Delayed Recall: Ball Flag Tree.1    | dc027s4, dc027s5, dc027s6                |
| Delayed Recall: Ball Flag Tree.2    | dc027s7, dc027s8, dc027s9                |
| Watch Correct                       | da007, da008, da013, da016, da018, da019 |
| Pencil Correct                      | da007, da008, da013, da016, da018, da019 |                                        |
| Repeat Correct                      | da005, da007, da017, da056               |
| Hand Correct                        | db009                                    |
| Folds Correct                       | db007                                    |
| Leg Correct                         | db006                                    |
| Close Your Eye                      | da032, da033, da034, da056_w3, db006     |
| Sentence Correct                    | da056_w3, db009                          |
| Draw Correct                        | dc025                                    |
| Highest Level of Education Attained | bd001                                    |
| Age                                 | ba004                                    |
| Sex                                 | rgender                                  |



### Calculate cognitive impairment score
`Highest Level of Education Attained` and `Age` is also considered in the calculation. 

We firstly remove people who's age is less than `45`, then the calculation of score is followed as below:
|Score|Education|
|-|-|
|21|Abnormal for 8-th grade education|
|<23|Abnormal for high school education|
|<24|Abnormal for college education|
