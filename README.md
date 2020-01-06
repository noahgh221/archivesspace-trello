# archivesspace-trello
aspace-to-trello.py creates Trello cards based on ArchivesSpace accession records. It is designed to be run as a cron job to identify recently updated accession records and then create Trello cards for them.

Script is written in Python 3 and uses [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) and [py-trello](https://github.com/sarumont/py-trello).

## Use Case:
- You use [ArchivesSpace](https://archivesspace.org) to create and manage accession records. 
- You use [Trello](https://trello.com) for project management and workflow tracking. 
- You're lazy, and don't want to copy/paste info about new accessions from ASpace into Trello.

## Getting Started 
1. Download the python script (aspace-to-trello.py). Ideally, you'll want to save the script to a location that has Python installed and can also execute cron jobs. I run the script from a Linux virtual machine where I've installed [Anaconda](https://www.anaconda.com/distribution/).

2. [Install ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake#installation) (assuming you already have Python installed)

3. [Install py-trello](https://pypi.org/project/py-trello/)

4. Create a Trello account (if you don't have one), and get your Trello API key, API secret, and token.  See: https://trello.com/app-key

5. Create a Trello board (if you don't have one) and a Trello list to hold the cards that the script will create.

6. Modify aspace-to-trello.py to supply your Trello API credentials, Trello board name, and Trello list name. Altenatively, you can supply the board ID and list IDs (see comments in code for "Option 1").

7. Modify aspace-to-trello.py to supply your ArchivesSpace backend URL, username, and password as well as the ID of your target repository (e.g. /repositories/2/accessions/). Your ArchivesSpace user must have permission to view accession records in this repository.

8. Determine how often you want to search for new accessions and create Trello cards. The script currently assumes you will run the script every 24 hours.

9. Cron job stuff coming soon...


## Things to consider:
- Trello cards are only a snapshot of ArchivesSpace data (nothing is synced). Updating Trello cards has no effect in ArchivesSpace and vice versa.
- Trello cards only contain a subset of metadata in an accession record (if you're feeling ambitious, you can modify the script to add more fields)

## Screenshots:
Add some Trello card screenshots

Add snippet of command line output
