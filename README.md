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
This is an extremly boring process. The key point is: if one indicator is missing in CHARLS, just find any other indicator *seemingly* right to replace the former indicator.

For example, if the indicator `Please repeat '44 stone lions'` which is a tongue-twister in Chinese to test the verbal ability is missing, I will find other indicators like below:
- DA005 Speech impediment
- DA007 Memory-related disease
- DA056 Interacted with friends & Played Ma-jong, played chess, played cards, or went to community club

In this section, some indicators like `DA005` are positive, while some indicators are negative. Given this, I set a weight manually.
