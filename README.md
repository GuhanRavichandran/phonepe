Guvi_CAPSTON_Project_Phonepe-Pulse-Data-Visualization-and-Exploration
The aim of this project is to develop a solution that extracts, transforms, and visualizes data from the Phonepe Pulse GitHub repository. The process involves:

Data Extraction: Scripting to clone the repository and collect data.

Data Transformation: Using Python and Pandas to clean and structure the data.

Database Insertion: Storing transformed data in a POSTGRESQL database.

Dashboard Creation: Using Streamlit and Plotly to build an interactive dashboard.

Data Retrieval: Fetching data from the database to dynamically update the dashboard.

Imported packages
import pandas as pd

import mysql.connector

import streamlit as st

import plotly.express as px

import requests as rq

import json 

