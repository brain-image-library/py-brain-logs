# README
The purpose of this project is to read the file `data/access.log` and parse it so that we can load it into workspace to a dataframe that has the following columns

* date
* IP
* dataset
* number of downloads

## The project
The main issue is that each line in this log file represents a request on a file, not a dataset. So we need to find a way to map the filename back to the dataset.

* Parse the log file and return a valid dataframe
* Extract metrics from the dataframe.
