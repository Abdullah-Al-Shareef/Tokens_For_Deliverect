# Tokens_For_Deliverect

## Overview
This project provides a refresh token function for Deliverect and saves tokens to the cloud for automated use.

## Setup
1. Clone the repository:
	```sh
	git clone https://github.com/Abdullah-Al-Shareef/Tokens_For_Deliverect.git
	cd Tokens_For_Deliverect
	```
2. Create and activate a Python virtual environment:
	```sh
	python3 -m venv env
	source env/bin/activate
	```
3. Install dependencies:
	```sh
	pip install -r requirements.txt
	```

## Usage
Run the authorization script:
```sh
env/bin/python Authorizations/auth.py
```

## Notes
- The `.gitignore` file excludes environment folders, cache, logs, and secrets.
- Make sure to select the correct Python interpreter in your IDE (see documentation for VS Code).

## License
MIT
