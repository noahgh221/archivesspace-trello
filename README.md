# archivesspace-trello
aspace-to-trello.py auto-generates Trello cards from ArchivesSpace accession records. It is intended to be run as a daily cron job.

Script is written in Python 3 and uses [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) and [py-trello](https://github.com/sarumont/py-trello).

## Use Case:
- You use [ArchivesSpace](https://archivesspace.org) to create and manage accession records. 
- You use [Trello](https://trello.com) for project management and workflow tracking. 
- You're lazy, and don't want to copy/paste info about new accessions from ASpace into Trello.

## Getting Started:
In progress...

## Things to consider:
- Trello cards are only a snapshot of ASpace data (nothing is synced). Updating Trello cards has no effect in ASpace and vice versa.
- Trello cards only contain a subset of metadata in an accession record (if you're feeling ambitious, you can modify the script to add more fields)

## Screenshots:
Add some Trello card screenshots

Add snippet of command line output
