# Airbnb Dashboard

**Authors**: Cedric Fleury, Damian Buess, Fabio Bohren<br>
**Version**: 1.0

## Project description: 
We created a web-dashboard to help **real estate owners in New York City** to **price their properties on Airbnb**. For this reason the **first part** of this dashboard **"Explore Data"** is to analyse the market and see how it reacts to different factors like neighbourhood or room type. If you now have analyzed the market and know which property you want to place on Airbnb or already knew it, the **second part "Price prediction"** helps you with pricing it. Our machine learning algorithm uses a random forest regressor to estimate an appropriate market price for your specific property!

**IMPORTANT NOTE:**<br>
The **dataset we used** for this app can be accessed for free on kaggle (https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data). In order to deploy the app **directly in a webbrowser**, we also used the open source python framework **streamlit** (https://streamlit.io/). Streamlit allows us to create the dashboard in python, while automating the graphical interface, as well as hosting the webpage for us.<br> 
<br> 
**View the project**: https://share.streamlit.io/fabiob99/airbnb_dashboard/main/Airbnb_Dashboard.py <br>

**Alternative**:<br>
You can also run the program from your **local system** with **Anaconda**<br>
**1. Start the Anaconda prompt** with the environment where the required packages are installed (view requirements.txt)<br>
**2. Type into the command line:** streamlit run "path of the Github repo or the project file"<br>

## File description:
The project consists of the following documents (which are all included in the Github repo):<br>

**Airbnb_Dashboard.py**: The main python file for the application. The script loads the necessary files, creates all the interface elements and data vizualizations and runs the prediction algorithm. See below for further comments on this part of the project. <br>
**Airbnb Housing Data.ipynb**: This Jupyter Notebooks document was used to develop the prediction model and the related dataset (airbnb_prediction_data.csv).<br>
**finalized_model.sav**: The prediction model created in the notebook was then exported using the pickle package and stored as a .sav file.<br>
**airbnb_data_dev.csv**: Contains the dataset which is used for the data visualization in the "Explore Data" section. <br>
**airbnb_prediction_data.csv**: Contains the transformed dataset which is used in the prediction section. <br>
**requirements.txt**: List for all the used packages in this project (includes only non-standard python packages).<br>
**Skyline.png**: Picture used in the header of the streamlit application.<br>
<br>

### The "Airbnb_Dashboard.py" file:
The main python file consistesconsists of sections of **6 main sections**. The more detailed information for the individual code snippets is included directly in the python file.
<br>

**Section 1: Load libraries**<br>
This part of the code is used to load in the used datasets (mentioned above) and the prediction model. In addition, some basic layoute settings (ex. to adjust the header) are done right at the beginning of the program.
<br>

**Section 2: Additional preparation**<br>
The second part of the file consists mainly of some functions which are used to store all the names of NYC neighborhoods in string arrays. These arrays are used later in the project for some filtering functions.
<br>

**Section 3: Header**<br>
The third section only consists of a few lines of code to **layout the header**.
<br>

**Section 4: Filter section**<br>
In this part of the code, the **filtering sidebar** on the left side of the page is created. The code consists of some **streamlit input widgets** (https://docs.streamlit.io/library/api-reference/widgets) which are used to filter the data in the "Explore Data" section (Section 5). The last part of this section uses the selected filtering options from the input widgets to **show the filtered data in realtime** on the page. Everytime the filters are changed, the page refreshes and runs the filtering process again.
<br>

**Section 5: Explore Data**<br>
The 5th part of the dashboard focuses on creating the **data visualization**, which is connected to the filtering section and is able to **adjust in realtime**. This section contains **three parts**: Firstly, the code generates **three KPI-Boxes** with some general information about the filtered dataset which will be visualized in the following graphs. Secondly, the **subsection “Plots”** generates **three graphs** with the **plotly package**. Thirdly, **two maps** are created with the package pydeck to visualize the individual datapoints. In addition, there is also the option to show the **filtered dataframe** as a **responsive table**.
<br>

**Section 6: Price Prediction**<br>
The last part of the project is used to create the **price prediction**. In the first part of this section, the **user interface elements** are created, using a similar filtering logic as in section 4. Then, a new dataframe is being created based on the **chosen input elements**. However, before running the prediction model, the **dataframe** has to be **transformed** into the same shape, as the training dataset used in the model. To start the prediction process, a **clickable button** is added as well.
