# Flask Authentication App

A flask authentication application made to allow users register on, log in to and log out of a webiste.

## Requirements:

NOTE: For any installation you do not know yet, please check YouTube for a video tutorial.

You should have installed:

- Python 3.13.2 (or any version)
- Visual Studio Code (or any other IDE e.g Pycharm, Atom)

## Process:

1. Create a folder to contain the entire project. Here, I used the name "my-flask-auth-app".

2. Access the folder "my-flask-auth-app" in the terminal and create a virtual environment by running the syntax below:

   `python -m venv virtual_env`

3. Activate the virtual environment. If you are currently within the main directory (the "my-flask-auth-app" folder) in your terminal, then run:

   `.\virtual_env\Scripts\activate`

4. After activating your virtual environment, install the necessary libraries by running the code below:

   `pip install requirements.txt`

5. Now run the following:

   `python app.py`

## Suggestions for Improvement:

1. Utilize flask.session to ensure only one user can be logged in at a time.
