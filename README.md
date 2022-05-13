# airbnb-housing-project

**Authors**: Cedric Fleury, Damian Buess, Fabio Bohren<br>
**Version**: 1.0

# Project description: 
We created a dashboard to help real estate owners in New York City to price their properties on Airbnb.
For this reason the first part of this dashboard **"Explore Data"** is to analyse the market and see how it reacts to different factors like neighbourhood or room type.
If you now have analyzed the market and know which property you want to place on Airbnb or already knew it, the second part **"Price prediction"** helps you with pricing it. Our machine learning algorithm uses a **random forest regressor** to estimate an appropriate market price for your specific property!

In order to deploy the app **directly from a webbrowser**, we used the open source python framework **streamlit**.<br>
Click on https://share.streamlit.io/fabiob99/airbnb-housing-project/main/Airbnb_Dashboard.py to view the project. Alternatively, the program can be started from the cmd line on your local system.

# File description:
The project consists of the following documents (which are all included in the Gihub repo):<br>
<br>
**Airbnb_Dashboard.py**: The main python file for the application. The script loads the necessary files, creates all the interface elements and data vizualizations and runs the prediction algorithm. See below for further comments on this part of the project. <br>
**Airbnb Housing Data.ipynb**: This Jupyter Notebooks document was used to develop the prediction model and the related dataset (airbnb_prediction_data.csv).<br>
**finalized_mdoel.sav**: The prediction model created in the notebook was then exported using the pickle package and stored as a .sav file.<br>
**airbnb_data_dev.csv**: Contains the dataset which is used for the data visualization in the "Explore Data" section. <br>
**airbnb_prediction_data.csv**: Contains the transformed dataset which is used in the prediction section. <br>
**requirements.txt**: List for all the used packages.<br>
**Skyline.png**: Picture used in the header of the streamlit application.<br>

# Desciption for the Airbnb Dashboard file:
The main python file consistes of the following sections:
<br>
**1. Load libraries:** s
