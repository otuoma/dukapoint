# Debian/Ubuntu QuickStart
These instructions are for quickly testing the system on Linux (Ubuntu or Debian ) systems

1. **Install Python**
    
    Dukapoint is built using Django version 2.1.4. Django 2 and above requires python 3.

    **Update and upgrade your OS packages**
    
    ```
    sudo apt-get update && sudo apt-get upgrade -y
    ```
     
     **Install python**
    ```
    sudo apt-get install python3 -y
    ```
2. **Set-up a virtual environment**

    Python 3 has `pip` installed.
    
     **Virtualenv**
    
    Open the terminal and run the command:
    ```
    pip install virtualenv
    ```    
    Create a directory for the project at a location of your choice e.g. `/opt/dukapoint`. 
    This is where the dukapoint source code will be downloaded to.
    
    Go inside the directory with the command:
    ```
    cd /opt/dukapoint
    ``` 
    Now create a virtual environment with:
    ```
    virtualenv env
    ```
    Then activate the virtual env with:
    
    ```
     ./env/Scripts/activate
    ```    
    
3. **Download and install dukapoint**

    Download dukapoint source code from [github](https://github.com/otuoma/dukapoint)
    
    Extract the file contents into `/opt/dukapoint/` so that its contents are:
    
```    
    --branches
    
    --customers
    
    --deliveries
    
    --dukapoint
    
    --media
    
    --products
    
    --sales
    
    --staff
    
    --static
    
    --suppliers
    
    --templates
    
    --.gitattributes
    
    --.gitignore
    
    --manage.py
    
    --README.md
    
    --requirements.txt     
```

Next, you need to install django and all the packages required by dukapoint.
You can do this with the command below:

```
pip install -r requirements.txt
```

### Create database and migrations
In this instance, we will run the application using SQLite database.
Issue the following command to create migrations:

```
python manage.py makemigrations
```
This will also create ` db.sqlite3` file that will serve for now as our database for testing the system.

Then `migrate` to create database tables
```
python manage.py migrate
```

### Run the server
Django comes with a testing server (not fit for production purposes). Since this is only for testing,
we can go ahead and run our system using django's server

```
python manage.py runserver
```

This will run the application on port 8000, if you need to run it on a different port number such as 
the default port 80 and make it accessible on the server's IP address, use:

```
python manage.py runserver 0.0.0.0:80
``` 

Now you should see the login page if you access [http://localhost:8000](http://localhost:8000) 
or [http://localhost](http://localhost) if you used port 80.

### Create `superuser`

Before you can login, you must create a superuser.

Stop the server by pressing `ctrl + C` then run the command:

```
python .\manage.py createsuperuser
``` 

Answer all the questions and press `enter` after each question to proceed to the next.

When finished, run the server again as shown above to login and start using the system.

### Using the system in summary
Perform the following tasks preferably in the sequence listed below:

1. Create branches `System->branches->add new`

2. Set superuser branch - on the top-right of the page, click on the user name and select 
   `Change branch` to set the logged-in user's branch.

3. Add suppliers `Suppliers->Add new`

4. Add products `Products->add new`. You can add as many products as you want.

5. Add stock `Products->Deliveries->add stock`. Add as many as you want.

6. Go to `POS` to start selling. On the top-right of the page, click on `POS`. Then start typing
the name of a product to start selling.

7. View sales reports `Sales->reports`


# Windows QuickStart
These instructions are for quickly testing the system on a windows 
system (tested on Windows 10)

1. **Install Python**
    
    Dukapoint is built using Django version 2.1.4. Django 2 and above requires python 3.

    Download and install the correct version of python 3.7 for your 
    operating system the normal way from python.org releases page for windows
    [here](https://www.python.org/downloads/windows/) 
     
     Ensure to add python to windows path during installation.
2. **Set-up a virtual environment**

    Python 3 has `pip` installed.
    
     Virtualenv
    
    Open windows powershell (or any other terminal you use) run the command:
    ```
    pip install virtualenv
    ```    
    Create a folder for the project at a location of your choice e.g. `C:\dukapoint`. This is where the dukapoint 
    source code will be downloaded to.
    
    Go inside the folder with the command:
    ```
    cd C:\dukapoint
    ``` 
    Now create a virtual environment with:
    ```
    virtualenv env
    ```
    Then activate the virtual env with:
    
    ```
     .\env\Scripts\activate
    ```
    This should work fine if you're using powershell
    
3. **Download and install dukapoint**

    Download dukapoint source code from [github](https://github.com/otuoma/dukapoint)
    
    Extract the file contents into `C:\dukapoint` so that its contents are:
    
```    
    --branches
    
    --customers
    
    --deliveries
    
    --dukapoint
    
    --env
    
    --media
    
    --products
    
    --sales
    
    --staff
    
    --static
    
    --suppliers
    
    --templates
    
    --.gitattributes
    
    --.gitignore
    
    --manage.py
    
    --README.md
    
    --requirements.txt     
```
Next, you need to install django and all the packages required by dukapoint.
You can do this with the command below:

```
pip install -r .\requirements.txt
```

### Create database and migrations
In this instance, we will run the application using SQlite database.
Issue the following command to create migrations:

```
python .\manage.py makemigrations
```
This will also create ` db.sqlite3` file that will serve for now as our database for testing the system.

Then `migrate` to create database tables
```
python .\manage.py migrate
```

### Run the server
Django comes with a testing server not fit for production purposes. Since this is only for testing,
we can go ahead and run our system using django's server

```
python manage.py runserver
```

This will run the application on port 8000, if you need to run it on a different port number such as 
the default port 80, use:

```
python manage.py runserver 0.0.0.0:80
``` 

Now you should see the login page if you access [http://localhost:8000](http://localhost:8000) 
or [http://localhost](http://localhost) if you used port 80.

### Create `superuser`

Before you can login, you must create a superuser.

Stop the server by pressing `ctrl + C` then run the command:

```
python .\manage.py createsuperuser
``` 

Answer all the questions and press `enter` after each question to proceed to the next.

When finished, run the server again as shown above to login and start using the system.

### Using the system in summary
Perform the following tasks preferably in the sequence listed below:

1. Create branches `System->branches->add new`

2. Superuser branch - is now set automatically when the first branch is created.

3. Add suppliers `Suppliers->Add new`

4. Add products `Products->add new`. You can add as many products as you want.

5. Add stock `Products->Deliveries->add stock`. Add as many as you want.

6. Go to `POS` to start selling. On the top-right of the page, click on `POS`. Then start typing
the name of a product to start selling.

7. View sales reports `Sales->reports`

##TO DO
1. Finish transfers module
2. Write tests
3. Remove current branch in products.forms.SetTransferToForm
4. Use transactions for multiple tbl updates


