# NLP-enabled Labeling Repair in Event Logs

An application for Natural Language Processing Labeling Repair (NLPLR). NLPLR is a Python standalone application that demonstrates the use of Natural Language Processing for detection and includes an interactive repair approach. It is an implementation of the approach presented in "Application of Natural Language Processing for Detection and
Interactive Repair of Labeling Anomalies in Event Logs".

## How it works

### 1) Download NLP model files and put into correct folder

Please download the following nlp model and place it into folder "nlp_label_quality/data/" and replace the placeholder with the following name "glove.6B.100d.txt".
<https://www.kaggle.com/danielwillgeorge/glove6b100dtxt>

### 2) Install necessary requirements and start main.py

Install the necessary requirements that can be found in the requirements.txt
![import_page](https://user-images.githubusercontent.com/93436324/140188257-68c1040e-bd9d-47ac-86b7-28815461f30c.png)

### 3) Select event logs for repair

Select the event log you want to repair through the import button

### 4) Select repair suggestions that are provided by tool

Explanations for values
'Theoretical Assumption: Decreasing probability of correct assignment of Original Label if occurence is lower than Suggested Label.\n' \
                    'Numerical values can be sorted manually by clicking on column title.\n\n'
                    'Glove Result: similarity value based on glove model_glove\n'
                    'Tfidf result: similarity value based on \'term frequency - inverted document fequency\'\n'
                    'Depth: depth of analysis; 2 -> second highest value of sorted similarity based on glove\n\n'
                    '\'Occurence\' counts total appearance within event eventlog.\n'
                    '\'Original Label\' will be replaced by \'Suggested Label\' in repaired event eventlog.'

        }

### Screencast Tutorial for Usage of Application

unlisted video uploaded on youtube (5min YT)

## Contact

fehlende Kontaktdaten

- Jasper Wiltfang ([LinkedIn](https://www.linkedin.com/in/jasper-wiltfang))
