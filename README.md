# NLP-enabled Labeling Repair in Event Logs

An application for Natural Language Processing Labeling Repair (NLPLR). NLPLR is a Python standalone application that demonstrates the use of Natural Language Processing for detection of labeling anomalies and includes an interactive repair approach. It is an implementation of the approach presented in "Application of Natural Language Processing for Detection and Interactive Repair of Labeling Anomalies in Event Logs".

## How it works

### 1) Download NLP model files and put into correct folder

Please download the [nlp model for GloVe](<https://www.kaggle.com/danielwillgeorge/glove6b100dtxt>) and replace the placeholder in folder "/data" with the following name "glove.6B.100d.txt".

### 2) Install necessary requirements and start main.py

Install the necessary requirements and start main.py (or main.exe if you use the executable).
![image](https://user-images.githubusercontent.com/93436324/141463850-c2f47891-f6bd-4f00-9ad1-e620e5b96f69.png)

### 3) Import Event Log to Repair

Select the event log through the import button and browse your computer to select a .xes-file that needs repair.
![image](https://user-images.githubusercontent.com/93436324/141463970-89b06bd1-b090-4111-8d2a-ffc298b07ad5.png)

### 4) Confirm which attributes shall be analyzed

Select pre-filtered attributes for all string values that can be analyzed, press "Confirm Selection" 
![image](https://user-images.githubusercontent.com/93436324/141464141-85e8e3bf-0a6b-4bad-ad2f-8bc0dff96b2d.png)

### 5) Start Analysis

Press "Start Analysis" after confirming the attributes to be analyzed and wait for results to appear (it might take a few seconds).

### 6) Interactively decide which selections are useful

After the analysis has run, the window updates to show all the results that the tool has generated.

**Information to help your decision:**

In the left column, you can see all values that are considered correct. You can select these to see all repair options connected to this correct value.

In the middle column, you can see an information tab that gives you details about the currently selected value from the left column.

| Value | Meaning | Example |
| ------------- |:-------------| :----- |
| Attribute | attribute in event log  | concept:name |
| Correct Value     | the value that is supposedly correct | 'Start Trip' |
| Correct Processed | 'Correct Value' but preprocessed for NLP analysis (the value that was actually compared to 'Incorrect Processed') | 'start trip' |
| Correct Freq | Number of occurences in the event log (higher numbers are less likely to be anomalous) | 6503 | 

In the right column, you can select the repair options that you deem useful to increase the event log quality of your event log.

| Value | Meaning | Example |
| ------------- |:-------------| :----- |
| Attribute | attribute in event log  | concept:name |
| Incorrect Value     | the value that is supposedly incorrect | 'Begins Trip' |
| Incorrect Processed | 'Incorrect Value' but preprocessed for NLP analysis (the value that was actually compared to 'Correct Processed') | 'begin trip' |
| Incorrect Freq | Number of occurences in the event log | 53 |
| NLP Result | similarity value based on NLP model after comparing 'Correct Processed' and 'Incorrect Processed' in Analysis | 0.9478... |
| Antonyms | antonymous relationships between compared values (highly unlikely that values have similar meaning) | {'start':'end'} |

![image](https://user-images.githubusercontent.com/93436324/141465491-83b564b2-6612-4579-858a-0bdf4227d968.png)

**How to select repair suggestions**
Select repair suggestions that are provided by tool through buttons on bottom.
If a repair is selected, all values that are 'Incorrect Value' in the original event log will be replaced by 'Correct Value' in the repaired event log.

Hold 'Ctrl' to select multiple values (color-scheme: <blue>):
| Button | Action | Color |
| ------------- |:-------------| :---: |
| Clear Selection | clear your current selection  |  |
| Reset Frame | reset frame to clear both selection and repair options |  |
| Discard Elements | Mark options that you deem incorrect | <lightred> |
| Elements to Repair | Mark options that you deem correct | <lightgreen> |
| Next Value from Listbox | skip to next value from left column |  |

![image](https://user-images.githubusercontent.com/93436324/141469598-ec428b01-faf0-45c7-aaf5-5653d548c140.png)

### 7) Run Repair, Next Analysis or Export Log

After selection of repair options, you need to actually run the repair by pressing 'Run Repair' at the bottom of the window. It is very important that you do not skip this step!
  
Furthermore, at any point during while using the tool, you are able to export the event log. Especially at the end of your iterative repair process, please export the event log as the temporary log within the tool is not exported automatically.

It is recommended to let multiple analyses run. The first ones are generally for syntax errors and afterwards, the tool detects semantic errors. Please use the full set of analyses to make sure that no anomalies stay in the log. Different NLP models are used to make sure that various errors are detected.

### Screencast Tutorial for Usage of Application

unlisted video uploaded on youtube (5min YT)

## Contact

- Jasper Wiltfang ([LinkedIn](https://www.linkedin.com/in/jasper-wiltfang))
