# Accounts API

This is a simple API project that is able to handle events such as:
- Account creation
- Deposits
- Withdraws
- Transfers 

## Architecture

The project is made in a single module with two layers.

### endpoints

The **endpoints** layer is responsible for handling the HTTP requests. 


### services

The **services** layer is responsible for handling the business logic of the API. 

---

## How to run the project

### 1. Install Python

- **Windows:** Download and install Python from [python.org](https://www.python.org/downloads/). During installation, ensure the option "Add Python to PATH" is checked.
- **macOS/Linux:** Python is usually pre-installed. You can check by typing python3 --version in the terminal. If not installed, you can use a package manager like brew on macOS (brew install python) or apt on Linux (sudo apt-get install python3). 

### 2. Set Up a Virtual Environment (Optional but Recommended)
```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Requirements
Install the required dependencies from requirements.txt:
```
pip install -r requirements.txt
```

### 4. Running the project 
Once you've installed the dependencies, you can run the project using:
```
python app.py
```
