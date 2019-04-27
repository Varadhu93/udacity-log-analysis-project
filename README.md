># Logs Analysis Project

>## About the Project
You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

>## Analysis to be done
To write SQL queries to answer the following questions about a PostgreSQL database containing the logs of a fictional newspaper website.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

>## Running the application

>### Pre-requisites
* [Python3](https://www.python.org/)
* [vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)
*   PostgreSQL

>### Application contents

* `loganalysis.py` - Python script that connects to the PostgreSQL database, executes the SQL queries and displays the results.
* `newsdata.zip` - Zip file containing a file that populates the `news` PostgreSQL database.
* `README.md` - README.md file
* `output.txt` - Contains the results of all the three analysis.

>### Steps to run the Project

Download the project zip file to your computer and unzip the file or clone this repository to your desktop.

Open the text-based interface for your operating system (e.g. the terminal window in Linux, the Git Bash/command prompt in Windows) and navigate to the project directory.

>### Bringing the VM up

Bring up the VM with the following command:
`vagrant up`

The first time you run this command, it will take awhile, as Vagrant needs to download the VM image.

You can then log into the VM with the following command:
`vagrant ssh`

Once inside the VM, navigate to the tournament directory with this command:
`cd /vagrant`

>### Load the data into database

First, unzip the zip file with the command:
`unzip newsdata.zip`

Run the following command to load the data into the database:
`psql -d news -f newsdata.sql`

>### Running the application
`python loganalysis.py`

>### Output
Output results can be found in `output.txt`

>### Shutting the VM down
When you are finished with the VM, press Ctrl-D to log out of it and shut it down with this command:

`vagrant halt`
