# HCI_Proj
**[GOOGLE DOCS](https://docs.google.com/document/d/1XwcLXEZ9ANSSibMToS6_dBphzFJvFjoHpnBYjqQWyGQ/edit?usp=sharing)**

## Dependencies
  ```
  pip install -r requirements.txt
  ```
## Link to a running website
[Link](https://danez13-crrjd-data-driven-basetball-application-main-guwczn.streamlit.app/)
## Introduction and Motivation
A web application is an interactive computer program developed using web technologies (HTML, CSS, JS), which stores (Database, Files) and manipulates data (CRUD - create, read, update and delete). Webapps can be used by a team or single user to perform tasks over the internet.

## Objective: 
In this assignment, you will develop a web application using the Streamlit framework that focuses on usability goals and adheres to human-computer interaction (HCI) design principles. You will use Streamlit features and API requests to fetch and display data in various forms, such as charts, plots, maps, and tables. Your web app must include interactive widgets, such as buttons, select boxes, radio buttons, text input, color input, and other features that help achieve the HCI guidelines. Your project needs to manipulate data requested through an API. The format of the documents received can be of any type, but I highly recommend JSON, XML, or CSV.

## Assignment Details
Select a theme or topic for your web application: Choose a topic that interests you and has public APIs available for data retrieval. Examples include weather forecasting, stock market analysis, social media trends, or public transportation information.

### Research and identify relevant APIs: 
Find one or more APIs that provide data relevant to your chosen topic. Ensure the APIs are publicly accessible and have clear documentation.

Here is a list of possible APIs that might be of interest to you:
- https://github.com/public-apis/public-apis
- https://rapidapi.com/collection/list-of-free-apis

### Define usability goals: 
Based on your selected topic, define a set of usability goals for your web app. These may include effectiveness, efficiency, learnability, memorability, error prevention, and user satisfaction.

### Design the web application: 
Sketch out a rough layout of your application, identifying the key components and user interactions. Consider the placement of widgets, navigation elements, and data visualizations.

### Develop the web app using Streamlit: 
Implement your design using Streamlit, incorporating the following features:

#### API requests: 
- Fetch data from the selected APIs
- At least 1 interactive table (https://docs.streamlit.io/library/api-reference/data/st.dataframeLinks to an external site.)
- At least 2 chart elements,  such as line, area or bar charts (matplotlib is allowed). To display:
  - **a line chart** - https://docs.streamlit.io/library/api-reference/charts/st.line_chartLinks to an external site.
  - **an area chart** - https://docs.streamlit.io/library/api-reference/charts/st.area_chartLinks to an external site.
  - **a bar chart** - https://docs.streamlit.io/library/api-reference/charts/st.bar_chartLinks to an external site.
- At least 1 map with points marked on it (a simple map can be created using https://docs.streamlit.io/library/api-reference/charts/st.mapLinks to an external site. or a  more complex 3d map at https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chartLinks to an external site.)
- At least 1 button widget (https://docs.streamlit.io/library/api-reference/widgets/st.button)
- At least 1 checkbox widget (https://docs.streamlit.io/library/api-reference/widgets/st.checkbox)
- At least 2 of the essential feedback and messages boxes to the users:
  - **Success box** - https://docs.streamlit.io/library/api-reference/status/st.successLinks to an external site. 
  - **Information box** - https://docs.streamlit.io/library/api-reference/status/st.infoLinks to an external site. 
  - **Warning box** - https://docs.streamlit.io/library/api-reference/status/st.warningLinks to an external site. 
  - **Error box** - https://docs.streamlit.io/library/api-reference/status/st.errorLinks to an external site. 
  - **Exception message (optional)** - https://docs.streamlit.io/library/api-reference/status/st.exceptionLinks to an external site. 
- At least any 5 different widgets chosen from the following:
  - **Radio button** - https://docs.streamlit.io/library/api-reference/widgets/st.radioLinks to an external site. 
  - **Selectbox** - https://docs.streamlit.io/library/api-reference/widgets/st.selectboxLinks to an external site. 
  - **Multiselect** - https://docs.streamlit.io/library/api-reference/widgets/st.multiselectLinks to an external site. 
  - **Slider** - https://docs.streamlit.io/library/api-reference/widgets/st.sliderLinks to an external site. 
  - **Select-slider** - https://docs.streamlit.io/library/api-reference/widgets/st.select_sliderLinks to an external site. 
  - **Text input** - https://docs.streamlit.io/library/api-reference/widgets/st.text_inputLinks to an external site. 
  - **Number input** - https://docs.streamlit.io/library/api-reference/widgets/st.number_inputLinks to an external site. 
  - **Text-area** - https://docs.streamlit.io/library/api-reference/widgets/st.text_areaLinks to an external site. 
  - **Date input** - https://docs.streamlit.io/library/api-reference/widgets/st.date_inputLinks to an external site. 
  - **Time input** - https://docs.streamlit.io/library/api-reference/widgets/st.time_inputLinks to an external site. 
  - **File uploader** - https://docs.streamlit.io/library/api-reference/widgets/st.file_uploaderLinks to an external site. 
  - **Color** - https://docs.streamlit.io/library/api-reference/widgets/st.color_pickerLinks to an external site. 
- You may include a progress bar for certain components of your application; however, this is not mandatory
- You may include media elements such as image, audio or video, which are not a requirement but can add to the overall harmony of the web application being developed
- Streamlit allows you to display a sidebar, insert containers laid out as side-by-side columns, insert a multi-element container that can be expanded/collapsed, among many other features:

  - **Sidebar** - https://docs.streamlit.io/library/api-reference/layout/st.sidebar
  - **Columns** - https://docs.streamlit.io/library/api-reference/layout/st.columns 
  - **Expander** - https://docs.streamlit.io/library/api-reference/layout/st.expander 

## Apply HCI design principles: 
Ensure your web app adheres to HCI design principles, such as visibility, feedback, consistency, flexibility, and error prevention. Consider the following aspects:
  1. **Information architecture:** Organize content and functionality to promote ease of use and understanding.
  2. **Navigation:** Provide clear and consistent navigation options.
  3. **User feedback:** Offer immediate and informative feedback to user actions.
  4. **Aesthetics:** Maintain a visually appealing and professional design.

## Test your web app: 
Conduct usability testing with a small group of users to identify any issues or areas for improvement. Make any necessary changes based on the feedback received.

## Document your work: 
Prepare a report that includes the following sections:
1. **Introduction:** Introduce your web app and its purpose.
2. **Usability goals:** Describe the usability goals you set for your web app and explain how you addressed each goal.
3. **Design process:** Discuss your design process, from sketching to implementation.
4. **API integration:** Explain how you utilized the APIs and discuss any challenges or limitations encountered.
5. **Interactive widgets:** Describe the widgets you incorporated and their purposes.
6. **HCI design principles:** Discuss how your web app adheres to HCI design principles.
7. **Testing and feedback:** Summarize the results of your usability testing and any changes made in response to feedback.
8. **Conclusion:** Reflect on your experience and discuss potential future improvements.

## Submission: 
Submit your web app's source code, along with your report and any supporting materials, such as sketches or user feedback.

### Requirements
The web application needs to be developed using Python programming languages version 3.9 (or later) and the open-source framework Streamlit. Your objective is to create a web application that manipulates data and displays information to the users.

The biggest HCI challenges will be the selection of appropriate layouts and containers. For example, you will need to study your target audience and the data being manipulated to decide, for example, whether to have 3 columns or 1 single column, or even whether an input data should be entered as a radio button or a text field, or whether to display a certain data output as a line chart or a map. For each project, you should think about the following structured design process:

- **User Research:** Identify and interview potential users to gather requirements.
- **Prototyping:** Create low-fidelity prototypes (e.g., wireframes) before coding.
- Usability Testing: Conduct usability tests with real users, iterating on design based on feedback.
- Accessibility: Ensure apps are designed with accessibility in mind, using guidelines such as the Web Content Accessibility Guidelines (WCAG)Links to an external site..
- Reflection: Write a reflection on the design process, user feedback, and iterations.

### Initial Steps
1. Choose a topic of interest to you (examples: sports, geology, music, cryptocurrency, farming, etc.)
2. Search for free and public datasets or free public APIs where you can request data to be manipulated and visualized in your web application
3. Start developing your web application:
    1. Download and install Python programming language version 3
    2. Download and Install PyCharm IDE Professional version by applying for a student license using your FIU email
    3. Create a new Python project in PyCharm IDE and:
    4. Install the necessary packages: pip install streamlit numpy pandas
    5. Import the above packages:
    ```
       import streamlit as st
       import pandas as pd
       import numpy as np
    ```
Include the components listed in **REQUIREMENTS** according to the goal of your web application and to the type of data being manipulated.
Distribute text elements in the form of title, header, subheader, caption or pre-formatted text across the web application so that the content of your web app engages readers and drives them to taken the necessary actions to fulfill your apps’s goals. Avoid dull, lifeless, and overlong prose. Try keeping text short and intriguing. This will encourage users to click through to other elements. Group content into cohesive categories by breaking it up into short paragraphs enriched with visual elements. This can help you make your web app have a light and engaging feel.

## Grading Criteria
Your project will be graded based on the following criteria:

1. Relevance and clarity of the chosen topic.
2. Successful integration of APIs and data visualization.
3. Inclusion and effective use of interactive widgets.
4. Adherence to HCI design principles.
5.Quality of testing and responsiveness to user feedback.
6.Thoroughness

| Criteria | Exemplary (10) | Proficient (8) | Adequate (6) | Insufficient (4) | pts |
|---|---|---|---|---|---|
Identification of target users | Users clearly identified and web app clearly caters for them | Users partially identified, but web app caters for this group | Users identified but web application does not necessarily cater for them | No users identified or mentioned in the project submission | 10 pts |
| Goal Identification | The web app's purpose is readily apparent to the user. | The web app has a firm purpose, but may occasionally digress from the purpose | The purpose is not always clear | The purpose is generally unclear | 10 pts |
|Link between the goal Identification and the target audience | The problem poses a novel perspective or a major opportunity for innovation | Web app provides firm support for the goal identification and displays evidence of a basic analysis of a sufficiently limited topic. User gains some insights | The problem is somewhat clear but solution feels like a hammer trying to find a nail | The problem is unclear, unimportant or not well-motivated. | 10 pts |
| Dataset properly identified | Dataset clearly identified and used either through pre-selected XML, CSV or JSON files or through API requests | Dataset is identified and used either through pre-selected XML, CSV or JSON files or through API requests, but insufficient for the goal of the application | Dataset not properly used for the web app’s goal | No dataset identified | 10 pts |
| Dataset properly manipulated | Data was correctly manipulated from the requested documents using the API | Data was correctly manipulated from the requested documents using the API; however, it did not match with the goal identified for this web app | The data was not properly managed from the JSON, CSV, or XML files. | No dataset identified | 10 pts |
| Execution | The web app is ready to be deployed and used | All relevant aspects of the project have been completed, but they have minor flaws | The basic elements of the research are complete, but either they are flawed or important aspects are still missing | The project has some complete components, but critical aspects are incomplete | 10 pts |
| Organization | The ideas are arranged logically to support the web app’s goal. They flow smoothly from one to another and are clearly linked to each other. User can follow line of reasoning. | The ideas are arranged logically to support the web app’s goal. They are usually clearly linked to each other. For the most part, user can follow line of reasoning. | The elements of the web app are not arranged logically. Frequently, ideas fail to make sense together. User can figure out what the developer probably intends but may not be motivated to do so. | The elements of the web application lacks any semblance of logical organization. The user cannot identify a line of reasoning and loses interest. | 10 pts |
| Streamlit properly used | All elements of Streamlit listed in the requirements were used | Not all elements of Streamlit listed in the requirements were used | Just some elements of Streamlit listed in the requirements were used | Just a few elements of Streamlit listed in the requirements were used | 10 pts |
| Submission | On time | 1 day late | 2 days late | 4 days late | 10 pts |
| Presentation | Web application was presented well with HCI elements clearly identified and correctly used | Web application was presented well, but HCI elements were not clearly identified or correctly used | Presentation lacked organization, identification of HCI elements, and did not meet the requirements | No presentation of the web application | 10 pts|
|---|---|---|---|---|**Total Points:** 100 |

