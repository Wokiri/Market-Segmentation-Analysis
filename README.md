
## <p align='center'>**Market Segmentation Analysis**</p>

<br/>



<p align='center'><img src="https://dub01pap001files.storage.live.com/y4m7hjHVg0zLNDAWMWjEuAXK3os1NSLS7zS-0oFtmmV7w1KM0eZJjKzaXfGq7qJTvgtFTGQOw9sMWdsoDWNiBB9ON3cdM-5n9C7flqa0RRFFfjaRR6zHy6a4K9LIcebbsINoy9UH5CAvZRFsIPJobbZAVniPZnqHA3lfYQB6aNMFz9RNqZhBvu0NJcZRMOOtQ2z?width=1280&height=800&cropmode=none" width="1280" alt="Map Thumbnail" /></p>

&nbsp;&nbsp;<br/>

---
<br/>

<h3 id='overview'>Overview</h3>

<br/>

This task requires a market segmentation analysis performed on a customer data set provided.
<br/>


<br/><br/>

<h1 id='toc'>Table of Contents</h1>

<a href="#overview">Overview</a><br/>
<a href="#softwares">Softwares Used</a><br/><br/>


**<p>PROJECT IMPLEMENTATION**</p>
   
1. <a href="#env_setup">Environment Setup</a><br/>
2. <a href="#django_project">Choice framework</a><br/>
3. <a href="#data_storage">Data storage into the database</a><br/>
4. <a href="#data_analysis">Data Analysis</a><br/>
5. <a href="#results_visualization">Results Visualization</a><br/>
6. <a href="#running_app">Running the App</a><br/>

  ---
<br/>

## <p id="env_setup">1. Environment Setup</p>

For a successful running of scripts in this project it is suggested that the packages listed in [requirements.txt](/requirements.txt) be installed.

At the core of these packages sits python which gives the 'base' platform upon which most of the others depend.


<br/>

## <p id="django_project">2. Django Project</p>

Django is a python web framework designed to make common Web development tasks fast and easy. It is used to make database-driven Web apps; that are interactive and enjoy the many beauties of available python libraries that are useful in one way or another. It is for these reasons, generally, that I thought to deliver this project using Django.


<br/>

<br/>

## <p id="data_storage">3. Data storage into the database</p>

### Excel Data:

With django's Object Relational Mapper, the provided excel file contents are uploaded into a database as whole a single file. 

In the process of so doing, the relevant information is extracted from within the excel file and accordingly stored into the Customer and Sales Object classes. It is possible to specify the number records to be written in the database.
<br/>


## <p id="data_analysis">4 Data Analysis</p>

Once the excel data is uploaded, there are a number of python functions that make it possible to view various segmentation procedures based on location, customers' prefered products, and number of sales per region.

I downloaded ward administrative boundary and clipped it on basis of intersection with the Customers/Sales Excel data and used the same to identify spatial context. 

Example of snapshots include:

</br>

#### Blank Homepage

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4m4s6KkfDhoc05nysTVT4zRXDLhbiIWVNgv36JIcA8tb5mvGnt4oW5RhijXnzas5poZHZByfYtrjfDHvl4fMz7VAfljldgsx0LJS8j4SYI3N9S67td_wONsyxWlUtaBTe76q5GKStrXlVI4V4mO2XeP6EIp41rcQ6Yg3TIdwEV9YpzrAzJ7d6QpU7-zZPhR5vA?width=1280&height=800&cropmode=none" width="1280" alt="Blank Homepage"/></p>

<br/>

</br>

#### Writting a portion of the Excel Data into the DataBase

Uploading the excel sheet into the databaase gives room for specifying the number of objects to actually write into the database. The example below shows a choice of 2500 Sales/Customer records written in the database. This value of course is flexible.

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mXhGdJnrfZj9_ngVsFMqXeiHhbSUZ3kNZt4G6S5aLK5SFTfpyGZPL60s5kWcyvJm8ta3KhZNhIzj4oTLTtygGTEKuTuAoisaqQoCTmwGdYv94hWq8Ua1jXdvqAOUlC95h_ZV59s2BB4G_wK4tfZtCUIDHDm0l_ar38jVwwnMwpYIgZX7A3kXebjs4h4IFzQJC?width=1280&height=720&cropmode=none" width="1280" alt="uploaded data, with partial database storage" /></p>

<br/>


</br>

#### Homepage with a tabular summary when Spatial and Sales data are uploaded

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mCBm2Y-8Hg9dIEn_meHwKGxQnHscLfAh-R3QsvVu-NmYFmScMJ1AHKGFKpsxTYp-M3an-ez0EEKALEDLXJSqP1iL-mzKZVxr-OXXjQkN_YsR0XIvTgK-g_Rne4t4cIPchD72iRoLawdm1KIdP6YxYWyX2x9mtEVoQG49lUhecwnsgVVIBPPPh5xXFch3Dg0xT?width=1280&height=800&cropmode=none" width="1280" alt="Homepage when Spatial and Sales data is uploaded" /></p>

Every ward name in the table above is a link that navigates to the map view of that specific ward

<br/>

</br>

#### Pie Charts showing the Market Size per County and SubCounty.

This can also be shown on a ward basis.

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mqewTSF1yl-ehx-0Jx278cDR6ZuZwYpsSG6n_bLedP3SfDT9MFNP8-N9PE2DEpcm80T84aybbU8Cnvd6RnEb17APMPK21-Aa2wIZEhbfWtSVAFRx4x4hu6UbDNyWdLbzonk6b_jfzAYGeH3kB0_XFnnCgeMN5PBvwd9CoQ3UnbyJMVqcQtfCsptI9S7v5JA4i?width=1282&height=802&cropmode=none" width="1282" alt="Market_Size_by_Number_of_Clients" /></p>

<br/>

</br>

#### Map of a ward and tabular summary about quantities of products consumption

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mNr4pbaFvTJI2SHFa6y_nYO7hTyf6y87gdmP1LdrWrWb7RXgy9jdnFkSsWS4ozO5ERWPdzNlbE3Au_qXuxeQR9D53g1-8SidklfTE9fMMU8wAVyTIZ1Mj14iPbYOXi-I3dFZs1lmBvJV5FDIY9NktgyVnmZBnl_5uOQwcGdaw4_smNRBuyALN4gk3d_aGvOkw?width=1280&height=800&cropmode=none" width="1280" alt="Ward_Map_Details" /></p>

<br/>

</br>

#### Vertical Bar graph showing sales per product in a given ward

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4m6GMMSJo1U7aq2G9Z3ggU6jgr-iKY-7o-QNx9g6I9a3leLhnmYCQdKZNNj_r9YIQjMZ1AnCYXMH70OfTJNLZDGeV0EGjPk8WCt877hvjr5w6WdQLH2jkY6kFLcDABWkuXSpkKiFCFLowS8oyolBGS58g3qhtus8etuYKRTIv4AF0BZ0fHsPXJRkUqEqNTdtZa?width=1120&height=600&cropmode=none" width="1120" alt="Vertical_bar_graph_about_sales" /></p>


Bokeh intergrates well with django which further enhances applicabity.

<br/>

</br>

#### Map showing all wards (with a selection bearing an active navigation link)

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4m27rKjaLWlomNrWOhNeuJ-lBaD4epvUYjvjtozz34pjXWVRWvFE-KnudlBxOM0kJwwOabKJPeIfPtc-4IepQszXbG0MwTLVJ8pKG7jLTUK18uULhEd9tUb01m4lY43oEuDr47N1KcjYYuOBvsanStynSgAM-7y2-f9vyPQPokQwbCI_1wCuxhnIDOS8ZWBhv1?width=1280&height=800&cropmode=none" width="1280" alt="All Wards" /></p>

<br/>

</br>

#### Gatina Ward selected from map of all wards

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mg8Gan-gH2DBNHaGgVQ6HiCC9YDOPW1zWFzBCY4HsB20PTDD0rejbT_nVxCz_05MKXL8q7FrGvV8Ygw_znmoNkULpsqPyDmo3dkBF_ajab2LXmtH_qfmLAza18jODGwYTKGUpKEi_O6qQuNrIxNWq1ZyiUQ-VtnVfohhgjb_KdBvxJa8JBYveD5qkrl-L9KFj?width=1280&height=800&cropmode=none" width="1280" alt="Gatina Ward" /></p>

<br/>


## <p id="results_visualization">5. Result Observations</p>

Displaying these data in the various formarts as shown in the pictures gives a way of clearly understanding the various aspects of market segmentation.

Geographic composition of this market was deeply analyzed from county, subcounty to ward levels.

The number of clients per ward has been shown.

The quantity of consumption of every product has been shown on a ward per ward basis.

- It can be seen, for example, that the most consumed product across wards is Product B.
- We can also see that those wards eastwards the CBD especially give the largest market.
- We also noticed that a in many of the wards there was a linear population along major roads.
- The total number of wards that have at least a client are 71.


<br/>

## <p id="running_app">6. Running App</p>

A summarized procedure of the steps to take in order to run the application.

## Accessing the code:

Clone this repo. With the command prompt or PowerShell in your directory of choice, you can download the project with the command:

```bash
git clone --depth 1 https://github.com/Wokiri/Market-Segmentation-Analysis.git
```

### Make a python virtual environment:

A virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories. This is important due to the fact that the installed packages for each virtual environment don’t interfere with each other, or, it prevents installed packages from affecting system services and other users of the machine.
With your command prompt or PowerShell in your directory of choice, a virtual environment can then be created by running:

```bash
C:\Python38\python.exe -m venv parkvenv
```


NB: This will work only if python is located in the address C:\Python38. If your python 3 isn’t residing in that path, just identify it and replace C:\Python38 with it.


### Activate python environment

```bash
.\parkvenv\Scripts\activate
```


### Install the libraries in the requirements.txt

```bash
python -m pip install -U -r requirements.txt
```


### Download Python gdal library
Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

From amongst the wide array of options, you want to chose a gdal version matching the python version used to make and activate your virtual environment, e.g for python 3.8 (as in my case) you download one with cp38 i.e. GDAL-3.1.4-cp38-cp38-win_amd64; for python 3.7, download one with cp37 i.e. GDAL-3.1.4-cp37-cp37m-win_amd64; and so on and so forth.
Put the downloaded gdal python wheel file in your working folder, then install it with:

```bash
python -m pip install GDAL-3.1.4-cp38-cp38-win_amd64.whl
```


### Create a database:
In the settings.py file found inside carpark directory, you will see we specified the PostGIS database called carpark. We should create it. While still inside this file, modify the password part by replacing the **os.environ.get('DB_PASSWORD')**, with **“your-postgres-password”**

Create the database. In PowerShell, type:

```bash
psql -U postgres
```

When the authorization is successful, go ahead and type:

```bash
CREATE DATABASE "mkt_segmentation";
```

If the creation is successful, we can now prepare and link the project with the database. Type exit to leave the psql shell.
Then create a migration:

```bash
py manage.py migrate
```

Various tables e.g. auth, amongst others will at this point be created in the database.
Then make a migration, to create all the database instances used in the project:

```bash
py manage.py makemigrations
```


### Effect the changes by running another migration:

```bash
py manage.py migrate
```


Your project is now ready. BUT, populate the database with the wards data first.

```bash
py manage.py loaddata wards.json
```


### Start the server:

```bash
py manage.py runserver
```


In your browser of choice, go to the address:
http://127.0.0.1:8000/

---

<br/><br/>


## Observed Issues:

1. The large dataset requires that database methods be optimized otherwise, depending on the computer, there are potential situations of memory lapses.
2. There is a GDAL error warning when i used the latest version of gdal which could be a cause of some delays.
