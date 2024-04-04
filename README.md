# CommuniData

## Description

# CommuniData

CommuniData is a data visualization dashboard tool designed specifically for community organizations in Chicago. It provides an intuitive and user-friendly interface for analyzing and presenting data related to various aspects of community development. With CommuniData, organizations can easily visualize and explore data to gain valuable insights, make informed decisions, and effectively communicate their findings to stakeholders. Whether it's tracking crime rates, analyzing demographic trends, or monitoring community resources, CommuniData empowers organizations to harness the power of data for positive change in their communities.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

This guide will help you get CommuniData up and running on your local development machine. 

### Prerequisites

Before you begin, ensure you have the following installed:
- Python (version 3.8 or newer)
- pip (Python package installer) 
- PostgreSQL (version 12 or newer)

### Clone the Repo

Clone the repo to your local machine

```
git clone https://github.com/wesordonez/CommuniData.git 

```

### Activate the Virtual Environment

It's recommended to use a virtual environment for Python projects to manages dependencies efficiently.

### Installing Dependencies

Install all required Python packages specified in the 'requirements.txt' file:

```python
pip install -r requirements.txt
```

### Configuring PostgreSQL and PGAdmin4

Create a new PostgreSQL database for CommuniData and update the settings.py file:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdatabasename',
        'USER': 'yourdatabaseuser',
        'PASSWORD': 'yourdatabasepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Apply the Django database migrations

```python
python manage.py migrate
```

## Usage

To run the project (in it's current state), start the Django development server:
python manage.py runserver

You can now access the web interface at 
'http://127.0.0.1:8000/'
or 
'localhost:8000/'

### Creating a Superuser

Create an admin user for accessing the Django admin interface:

```
python manage.py createsuperuser
```

## Contact

- Email: wesordonez1@gmail.com
- GitHub: [wesordonez](https://github.com/wesordonez)

- Collaborators: Benjamin Quezada, Cesar Ordonez

### Thanks!!
