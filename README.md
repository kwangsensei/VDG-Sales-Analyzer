# Video Game Sales Analyzer

## Description
The application can analyze the sales of the video game data since 2000 - 2010. The user must be select year to analyzing data from selected year and user can select publisher name and/or country that games sale from. Then the data will be display as bar graph like picture below. Please note that year must be selected.

<img src="app.png">

Demo Clip
https://youtu.be/iUsl-jlKlwA

## Running the Application
Pandas: To create DataFrame by pandas.read_csv().
Seaborn: To plot graph by barplot().
    
## Design
Application's UI design by let user choose what year user want to look and then user can be more deep access by choosing publisher or counrtry or both. When user finish choosing topic to analyze, press "Show" button to display bar graph. There are reset buttons so user can quickly change the POV of data easier I added progess bar to tell user that data is analyzing.

<img src="uml.png">

## Design Patterns Used
State Pattern: To check what combobox being selected.
Observer Pattern: To use with buttons that occur some actions.
 
## Other Information
Anything else you would like to include. Anything you think is important or interesting that you learned. For example, any interesting libraries or packages you use in your application.
