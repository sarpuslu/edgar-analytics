# Edgar Analytics

## Introduction
Many investors, researchers, journalists and others use the Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system to retrieve financial documents, whether they are doing a deep dive into a particular company's financials or learning new information that a company has revealed through their filings.

The EDGAR Log File Data Set contains information in CSV format extracted from Apache log files that record and store user access statistics for the SEC.gov website. 

## Motivation
This repo is a submission for the insight coding challenge. 
For more details: https://github.com/InsightDataScience/edgar-analytics

## Goal
The goal of the challenge is to use the log files to identify when a user visits, calculate the duration of and number of documents requested during that visit, and then write the output to a file.

## Data 

### Input
EDGAR log files can be found here: https://www.sec.gov/dera/data/edgar-log-file-data-set.html

These log files are in the following format:
* ip: identifies the IP address of the device requesting the data. While the SEC anonymizes the last three digits, it uses a consistent formula that allows you to assume that any two ip fields with the duplicate values are referring to the same IP address
* date: date of the request (yyyy-mm-dd)
* time: time of the request (hh:mm:ss)
* cik: SEC Central Index Key
* accession: SEC document accession number
* extention: Value that helps determine the document being requested

### Output
Once the log entries are sessionized they should be stored in the following format:
* IP address of the user exactly as found in log.csv
* date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
* date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
* duration of the session in seconds
* count of webpage requests during the session

## How to run this script
Pass input files log.csv and inactivity_period as command line arguments. The sessionized entries will be written in output.txt.

'''
python3 ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/output.txt
'''



