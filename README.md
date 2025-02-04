# upGIT
UpGit is a mini Desktop application that is bent at leveraging Git and GitHub technologies to resolve file backup and folder backup for its users, irrespective of their knowledge of these technologies

## Prerequisites
- Python 3.9+

## Getting Started
After being invited to the private repository,

1. Clone the repository
```bash
git clone https://github.com/afanyuy-caleb/upGIT-code.git .
cd upGIT-code
```

2. Create a virtual environment
```bash
py -m venv upgit_env
```

3. Activate the virtual environment
```bash
upgit_env\Scripts\activate
```

4. install the dependencies and packages
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```
Add and Edit `.env` with your specific github account configuration (token, username, email) and the chunk suffix.
```

6. Add the virtual environment and .env to the .gitignore file
```
Open the .gitignore file and type in 
.env
upgit_env (or the name of your virtual environment if differnt from this)
```

## Usage

1. Run the application
```bash
python app.py
```

## Development

- Install new packages (Add packages):
```bash
pip install <package_name> 
```
Or if the later doesn't work, you can run
```bash 
python -m pip install <package_name> 
```
- Add the package to the requirements.txt
```bash
pip freeze > requirements.txt
```

## Basic Project Structure
```
UpGit/
├── app/
│   ├── auth/
│   │   └── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── database.py
│   ├── controllers/
│   │   └── __init__.py
│   ├── crud/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── schema/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── tests/
│   │   └── __init__.py
│   ├── views/
│   │   └── __init__.py
│   ├── __init.py
│   └── demo.py
│   └── main.py
├── logs/
│   └── app.log
├── upgit_env/
│   ├── Include
│   ├── Lib
│   ├── Scripts
│   ├── .gitignore
│   └── pyvenv.cfg
├── .env
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

