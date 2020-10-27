# Koala

## Introduction

Koala is an Exciting new **Learning Platform** (not a VLE) for teaching.
It gets rid of all the stuff that things like moodle has and replaces it with
the same thing but **100% more shiny**.

##  Actual Introduction

Koala is an example vulnerable application Built for the 6005-CEM module at
Coventry University.  Any similarities to learning managment systems are purely
co-incidental.


## Instructions for Setup

NOTE FOR STUDENTS:  For the assessment.  Treat these as the Actual Install Instructions.

- Unzip the source code  (You must have done that to read this)

## Instructions for Setup

!!! important

    For the assessment.  Treat these as the Actual Install Instructions.

- Unzip the source code  (You must have done that to read this)

- Change directory into your newly created project.
 
    ```cd koala```

- Create a Python virtual environment.

    ```python3 -m venv env```

- Activate the environment

    - In Windows  ```env/scripts/activate```
    - In Linux    ```source env/bin/activate```


- Install the project in editable mode with its testing requirements.

    ```python setup.py develop```

- Initialize and upgrade the database using Alembic.

	!!! note

		If alembic says it cant find the a directory you need to create one in 
		```koala\alembic\versions```

    - Generate your first revision.

        ```alembic -c development.ini revision --autogenerate -m "init"```

    - Upgrade to that revision.

        ```alembic -c development.ini upgrade head```

- Load default data into the database using a script.

    ``initialize_koala_db development.ini``

- Run your project.

    ```pserve development.ini``

- Access the code

  You now have an empty Koala project at (127.0.0.1:6543)
  You can login using the default admin credentials

  - Username:  admin@coventry.ac.uk
  - Password:  swordfish

### Getting a Demo Site running

I have also created a script to generate a demonstration site.
You can add this by running

```
create_koala_demo  development.ini
```

This will create some example Modules, and Posts
You will also get users

  - teacher@coventry.ac.uk   (Password teacher)
  - student@coventry.ac.uk   (password student)

## Running After Setup

You shouldn't need to do any of the setup instructions after the first time
Just start the site with 

```
pserve development.ini
```

