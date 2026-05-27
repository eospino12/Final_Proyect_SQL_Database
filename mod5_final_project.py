# -*- coding: utf-8 -*-
"""
Archivo generado a partir de mod5_final_project.ipynb
"""

# %% [markdown]
# <center>
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/images/SN_web_lightmode.png" width="300" alt="cognitiveclass.ai logo">
# </center>
# 
# <h1 align=center><font size = 5>Assignment: Notebook for Graded Assessment</font></h1>


# %% [markdown]
# # Introduction
# 
# Using this Python notebook you will:
# 
# 1.  Understand three Chicago datasets
# 2.  Load the three datasets into three tables in a SQLIte database
# 3.  Execute SQL queries to answer assignment questions


# %% [markdown]
# ## Understand the datasets
# 
# To complete the assignment problems in this notebook you will be using three datasets that are available on the city of Chicago's Data Portal:
# 
# 1.  <a href="https://data.cityofchicago.org/Health-Human-Services/Census-Data-Selected-socioeconomic-indicators-in-C/kn9c-c2s2?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01">Socioeconomic Indicators in Chicago</a>
# 2.  <a href="https://data.cityofchicago.org/Education/Chicago-Public-Schools-Progress-Report-Cards-2011-/9xs2-f89t?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01">Chicago Public Schools</a>
# 3.  <a href="https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01">Chicago Crime Data</a>
# 
# ### 1. Socioeconomic Indicators in Chicago
# 
# This dataset contains a selection of six socioeconomic indicators of public health significance and a “hardship index,” for each Chicago community area, for the years 2008 – 2012.
# 
# A detailed description of this dataset and the original dataset can be obtained from the Chicago Data Portal at:
# 
# [https://data.cityofchicago.org/Health-Human-Services/Census-Data-Selected-socioeconomic-indicators-in-C/kn9c-c2s2](https://data.cityofchicago.org/Health-Human-Services/Census-Data-Selected-socioeconomic-indicators-in-C/kn9c-c2s2?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01&cm_mmc=Email_Newsletter-\_-Developer_Ed%2BTech-\_-WW_WW-\_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork-20127838&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ)
# 
# ### 2. Chicago Public Schools
# 
# This dataset shows all school level performance data used to create CPS School Report Cards for the 2011-2012 school year. This dataset is provided by the city of Chicago's Data Portal.
# 
# A detailed description of this dataset and the original dataset can be obtained from the Chicago Data Portal at:
# 
# [https://data.cityofchicago.org/Education/Chicago-Public-Schools-Progress-Report-Cards-2011-/9xs2-f89t](https://data.cityofchicago.org/Education/Chicago-Public-Schools-Progress-Report-Cards-2011-/9xs2-f89t?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01&cm_mmc=Email_Newsletter-\_-Developer_Ed%2BTech-\_-WW_WW-\_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork-20127838&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ)
# 
# ### 3. Chicago Crime Data
# 
# This dataset reflects reported incidents of crime (with the exception of murders where data exists for each victim) that occurred in the City of Chicago from 2001 to present, minus the most recent seven days.
# 
# A detailed description of this dataset and the original dataset can be obtained from the Chicago Data Portal at:
# 
# [https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01&cm_mmc=Email_Newsletter-\_-Developer_Ed%2BTech-\_-WW_WW-\_-SkillsNetwork-Courses-IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork-20127838&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ)


# %% [markdown]
# ### Download the datasets
# 
# This assignment requires you to have these three tables populated with a subset of the whole datasets.
# 
# In many cases the dataset to be analyzed is available as a .CSV (comma separated values) file, perhaps on the internet. 
# 
# Use the links below to read the data files using the Pandas library. 
# 
# * Chicago Census Data
# 
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCensusData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01
# 
# * Chicago Public Schools
# 
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoPublicSchools.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01
# 
# * Chicago Crime Data
# 
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCrimeData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01
# 
# **NOTE:** Ensure you use the datasets available on the links above instead of directly from the Chicago Data Portal. The versions linked here are subsets of the original datasets and have some of the column names modified to be more database friendly which will make it easier to complete this assignment.


# %% [markdown]
# Execute the below code cell to install the required libraries


# %% [code]
!pip install pandas
!pip install ipython-sql prettytable 

import prettytable

prettytable.DEFAULT = 'DEFAULT'


# %% [markdown]
# ### Store the datasets in database tables
# 
# To analyze the data using SQL, it first needs to be loaded into SQLite DB.
# We will create three tables in as under:
# 
# 1.  **CENSUS_DATA**
# 2.  **CHICAGO_PUBLIC_SCHOOLS**
# 3.  **CHICAGO_CRIME_DATA**


# %% [markdown]
# Load the `pandas` and `sqlite3` libraries and establish a connection to `FinalDB.db`


# %% [code]
import sqlite3 as sql
import pandas as pd

conn = sql.connect("FinalDB.db")


# %% [markdown]
# Load the SQL magic module


# %% [code]
%load_ext sql


# %% [markdown]
# Use `Pandas` to load the data available in the links above to dataframes. Use these dataframes to load data on to the database `FinalDB.db` as required tables.


# %% [code]
import pandas as pd

census_df = pd.read_csv("ChicagoCensusData.csv")
schools_df = pd.read_csv("ChicagoPublicSchools.csv")
crime_df = pd.read_csv("ChicagoCrimeData.csv")

census_df.to_sql("CENSUS_DATA", conn, if_exists='replace', index=False)

schools_df.to_sql("CHICAGO_PUBLIC_SCHOOLS", conn, if_exists='replace', index=False)

crime_df.to_sql("CHICAGO_CRIME_DATA", conn, if_exists='replace', index=False)


# %% [markdown]
# Establish a connection between SQL magic module and the database `FinalDB.db`


# %% [code]


%sql sqlite:///FinalDB.db


# %% [markdown]
# You can now proceed to the the following questions. Please note that a graded assignment will follow this lab and there will be a question on each of the problems stated below. It can be from the answer you received or the code you write for this problem. Therefore, please keep a note of both your codes as well as the response you generate.


# %% [markdown]
# ## Problems
# 
# Now write and execute SQL queries to solve assignment problems
# 
# ### Problem 1
# 
# ##### Find the total number of crimes recorded in the CRIME table.


# %% [code]
%%sql
SELECT COUNT(*) 
FROM CHICAGO_CRIME_DATA;


# %% [markdown]
# ### Problem 2
# 
# ##### List community area names and numbers with per capita income less than 11000.


# %% [code]
%%sql
SELECT COMMUNITY_AREA_NAME, COMMUNITY_AREA_NUMBER
FROM CENSUS_DATA
WHERE PER_CAPITA_INCOME < 11000;


# %% [markdown]
# ### Problem 3
# 
# ##### List all case numbers for crimes involving minors?(children are not considered minors for the purposes of crime analysis) 


# %% [code]
%%sql
SELECT CASE_NUMBER
FROM CHICAGO_CRIME_DATA
WHERE DESCRIPTION LIKE '%MINOR%';


# %% [markdown]
# ### Problem 4
# 
# ##### List all kidnapping crimes involving a child?


# %% [code]
%%sql
SELECT *
FROM CHICAGO_CRIME_DATA
WHERE PRIMARY_TYPE = 'KIDNAPPING'
AND DESCRIPTION LIKE '%CHILD%';


# %% [markdown]
# ### Problem 5
# 
# ##### List the kind of crimes that were recorded at schools. (No repetitions)


# %% [code]
%%sql
SELECT DISTINCT PRIMARY_TYPE
FROM CHICAGO_CRIME_DATA
WHERE LOCATION_DESCRIPTION LIKE '%SCHOOL%';


# %% [markdown]
# ### Problem 6
# 
# ##### List the type of schools along with the average safety score for each type.


# %% [code]
%%sql
SELECT "Elementary, Middle, or High School",
       AVG(SAFETY_SCORE) AS AVG_SAFETY_SCORE
FROM CHICAGO_PUBLIC_SCHOOLS
GROUP BY "Elementary, Middle, or High School";


# %% [markdown]
# ### Problem 7
# 
# ##### List 5 community areas with highest % of households below poverty line


# %% [code]
%%sql
SELECT COMMUNITY_AREA_NAME,
       PERCENT_HOUSEHOLDS_BELOW_POVERTY
FROM CENSUS_DATA
ORDER BY PERCENT_HOUSEHOLDS_BELOW_POVERTY DESC
LIMIT 5;


# %% [markdown]
# ### Problem 8
# 
# ##### Which community area is most crime prone? Display the coumminty area number only.


# %% [code]
%%sql
SELECT COMMUNITY_AREA_NUMBER
FROM CHICAGO_CRIME_DATA
GROUP BY COMMUNITY_AREA_NUMBER
ORDER BY COUNT(*) DESC
LIMIT 1;


# %% [markdown]
# 
# Double-click **here** for a hint
# 
# <!--
# Query for the 'community area number' that has most number of incidents
# -->


# %% [markdown]
# ### Problem 9
# 
# ##### Use a sub-query to find the name of the community area with highest hardship index


# %% [code]
%%sql
SELECT COMMUNITY_AREA_NAME
FROM CENSUS_DATA
WHERE HARDSHIP_INDEX = (
    SELECT MAX(HARDSHIP_INDEX)
    FROM CENSUS_DATA
);


# %% [markdown]
# ### Problem 10
# 
# ##### Use a sub-query to determine the Community Area Name with most number of crimes?


# %% [code]
%%sql
SELECT COMMUNITY_AREA_NAME
FROM CENSUS_DATA
WHERE COMMUNITY_AREA_NUMBER = (
    SELECT COMMUNITY_AREA_NUMBER
    FROM CHICAGO_CRIME_DATA
    GROUP BY COMMUNITY_AREA_NUMBER
    ORDER BY COUNT(*) DESC
    LIMIT 1
);


# %% [markdown]
# ## Author(s)
# 
# <h4> Hima Vasudevan </h4>
# <h4> Rav Ahuja </h4>
# <h4> Ramesh Sannreddy </h4>
# 
# ## Contribtuor(s)
# 
# <h4> Malika Singla </h4>
# <h4>Abhishek Gagneja</h4>
# <!--
# ## Change log
# 
# | Date       | Version | Changed by        | Change Description                             |
# | ---------- | ------- | ----------------- | ---------------------------------------------- |
# |2023-10-18  | 2.6     | Abhishek Gagneja  | Modified instruction set |
# | 2022-03-04 | 2.5     | Lakshmi Holla     | Changed markdown.                   |
# | 2021-05-19 | 2.4     | Lakshmi Holla     | Updated the question                           |
# | 2021-04-30 | 2.3     | Malika Singla     | Updated the libraries                          |
# | 2021-01-15 | 2.2     | Rav Ahuja         | Removed problem 11 and fixed changelog         |
# | 2020-11-25 | 2.1     | Ramesh Sannareddy | Updated the problem statements, and datasets   |
# | 2020-09-05 | 2.0     | Malika Singla     | Moved lab to course repo in GitLab             |
# | 2018-07-18 | 1.0     | Rav Ahuja         | Several updates including loading instructions |
# | 2018-05-04 | 0.1     | Hima Vasudevan    | Created initial version                        |
# -->
# ## <h3 align="center"> © IBM Corporation 2023. All rights reserved. <h3/>

