# Team SH06 Main Project - Team Project 3 Course 2024

## Project Name

Cold Case Management System

## Description

**This is a proof of concept product, and is not ready for market deployment**  
The AI analysis in this system is reviewed by a human user, but is not guaranteed to be perfectly truthful.  

### Our goal

This project has been developed as part of a University of Glasgow module, Professional Software Development.

It is aimed at reducing the time taken in order for detectives to collate, analyse and connect evidence.  
This is achieved by digitizing various types of cold case evidence, using AI to extract and summarize information found within it and providing tools for collaboration between detectives and visual representation of the data.  
The project also organises evidence in an ordered, logical manner.  

### Features of this project

Document Analysis Features

1. Analysing cold case evidence data of various formats, including:

    - PDF, images (including handwritten documents) & .txt
    - Audio/Video file types may be available to upload and download from the software. However, there are no plans to have these be analysed

2. Using AI, extract information from documents, including:

    - People involved, place of events, time of events, case number referenced within document.
    - This will be a “text-based” relationship at first, and if possible, it can be built upon to create programmatic relationships.

Document Visualisation Features

1. View a summary of the document.
2. View the related documents of the current document.
3. An “Entities” view which highlights:  
    - People, Events, Evidence, Locations
4. View the changes made to a document, in a [who did / what / when] format.
5. Users can make comments on a document

Case Management

1. Search all cases assigned to user.  
    - Wildcard searching
    - Sort by recently updated/Date of last access
2. See a list of cases recently accessed by the user  
3. Manage cases:  
    - Assign a user to a case (general or reviewer type user)
4. View updates made to cases
5. System to review uploads  
    - A case can have a main reviewer assigned, who will verify and validate the output from the AI result. (persons involved, events and times etc.)

General System Features

1. Secure login system (username + password combo)
2. Sidebar for navigation between the "top level" pages
3. User types of the system  
    - Detective (general user)
    - Reviewer (can approve AI generated outputs before they are inserted into the case)
4. Ability to download the original, raw documents from the server.
5. AI generated content will have a disclaimer displayed to the user where it is used, to account for the lack of a 100% accurate output requirement.

## Installation

This project uses a Django backend, with a local SQLite database, and React frontend.

Packages for this system are installed using pip (<https://pip.pypa.io/en/stable/>) and npm (<https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>).  
We used virtual environments throughout development, these should be created within the sh06-main directory.  
Once you have activated your virtual environment, these are the steps to install the dependancies:

```bash
> sh06-main/sas-forensics/
pip install -r requirements.txt

> sh06-main/sas-forensics/frontend/
npm install --legacy-peer-deps
```

There may be some installation issues with node.js.  
To troubleshoot these, install nodeJS (<https://nodejs.org/en/download/>), verify your npm and node versions, then attempt "npm install" again.

## Usage

How to run this project locally:  

```bash
cd sh06-main
<name_of_env>\Scripts\activate
cd sasforensics/backend
python manage.py makemigrations
python manage.py migrate
python manage.py populate_test_data
cd  ../frontend
npm start
```

How to build docker images for this project:

```bash
cd sh06-main
<name_of_env>\Scripts\activate
cd sasforensics/backend
python manage.py makemigrations
python manage.py migrate
python manage.py populate_test_data
cd ..
docker-compose build
docker-compose up
```

This will run the project locally on localhost:3000.

## Support

Feel free to contact Matthew Ballantyne (<2774408B@student.gla.ac.uk>) for support for this project.

## Roadmap

Features which have been discussed:

- Creating programmatic relationships between entities, such as people, evidence, events etc.
  - This would allow for real links to be built between these giving more depth to the project.
- Commenting and annotations on documents and cases:
  - A user currently cannot highlight/comment on documents or leave comments on a case.  
    This feature would enable collaboration between users of the system

## Authors and acknowledgment

We have worked on this project as a team of 6 students,

- Matthew Ballantyne (<2774408B@student.gla.ac.uk>)
- Viktoriia Boiechko (<2833791B@student.gla.ac.uk>)
- Eduardo Flores Lopez (<2840598F@student.gla.ac.uk>)
- Edan Hynes (<2777195H@student.gla.ac.uk>)
- Yuan Kuang (<2672762K@student.gla.ac.uk>)
- Sophia Pollock (<2801049P@student.gla.ac.uk>)

With the help of our team coach,

- Boris Velinov (<2641360V@student.gla.ac.uk>)

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) for details.

## Project status

The university module which this project was being developed for has come to an end, so there are no current plans to continue development. However, we may continue development of features if requested by our customer.
