# fetch_data

In this script I've used selenium chrome webdriver for web-scraping an infinite-scroll page.

You may please the right version of chrome webdriver and give the correct path to your driver

and run the script.

# Storing Data

I have created a mysql database and inserted all of fetched data into it. You can see the 

database scheme in the text file name database-scheme.txt.

I have also created a dictionary for building types and regions to map the to integers for

modeling them and saved them as json objects in .json files.


# Modeling data

I Have written a script in "train_on_dataset.py" file. In this script I've used used sklearn.LinearRegression

to fit a model to the data stored in database. And saved the computed model in a .sav binary file using pickle

library.


# Predict Price

In the last script I've loaded the stored regression model in the previous script and used it to predict 

the price of buildings which their data are given by the user.