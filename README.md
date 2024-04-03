# Sands of Time (Treasure Hunt Organised by 8Bit - Magazine Club of IIITB)

## About
A website which helped 8Bit, the magazine club of IIITB in conducting a treasure hunt event for Synergy (Techfest of IIITB)

## TechStack
1. **Django**
2. **SQL**
3. **Python**
4. **JavaScript**
5. **HTML**
6. **CSS**


## Description
This project contains a Django application that handles user authentication. It includes a login page where users can enter their email and password to access the system. You can enter passcodes to gain sand (points) and time. The website uses sql database to identify which codes are sand and which are time and increase the timer/points accordingly. The database also ensures that one won't gain points for entering the same code more than once. Finally you can also see a leaderboard once you login. 

The website was used by around 25% students to enter codes. 

## Installation
1. Clone the repository: `git clone https://github.com/Sarvesh521/Sands-Of-Time.git`
2. Navigate into the project directory: `cd game`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the server: `python manage.py runserver`

## Usage
Open your web browser and navigate to `localhost:8000\login` to access the login page.

## Deployment
Go to `https://sarvesh521.pythonanywhere.com/participant` to checkoout the site!!

## Next Steps
Using django channels to implement websockets will be a good step forward. It will help in solving the issue of reloading the page evertime one has to look at the leaderboard for any changes. Using websockets this problem will be solved and it will give more user-friendly experience. 
