# Introduction

This `Python` project:

* Utilizes the Stationary Wavelet Transform (SWT) for denoising ECG signals
* Provides a library of functions to calculate ECG metrics, such as:
    * RR intervals
    * Heart rate
    * Heart rhythm status
    * ST segment related changes
    * T-wave relevant status
    * PQ interval status

## Usage

### Installation 
Use the following commands in `terminal` to clone this project into your local folder `ECG Project/~`

```bash
git clone https://github.com/0-Kaustubh-0/ECGmetrics_SWTdenoising.git
```

### Dependencies

You would need to install the following Python packages in your environment  

```
pip install numpy, scipy, pandas, math, matplotlib 
``` 

### Functions

There are 3 primary functions included as a part of the project:

* ecgDenoise        - Function to denoise an array of ECG signals
* ecgAnalyze        - Function library to generate metrics from the ECG data supplied
* main.py           - Main function which calls the two functions above

> Tip: You may utilize any denoising technique that you deem fit as per your data/ analyses. You can find [filter creation guides][1] or several wavelet denoising techniques in my other repos.

## Reference

If you utilize this resource or the article related to this project [Denoise (using Stationary Wavelets) and analyze ECG data][2], please provide the appropriate reference to this repository or webpage, respectively.

[1]: 
[2]:
