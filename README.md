# archivesspace-trello [IN PROGRESS]
aspace-to-trello.py creates Trello cards based on ArchivesSpace accession records. It is designed to be run as a cron job to identify recently updated accession records and then create Trello cards for them.

Script is written in Python 3 and uses [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) and [py-trello](https://github.com/sarumont/py-trello).

## Use Case
- You use [ArchivesSpace](https://archivesspace.org) to create and manage accession records. 
- You use [Trello](https://trello.com) for project management and workflow tracking. 
- You're lazy, and don't want to copy/paste info about new accessions from ASpace into Trello.

## Getting Started 
#### Download the python script (aspace-to-trello.py). Ideally, you'll want to save the script to a location that has Python installed and can also execute cron jobs. I run the script from a Linux virtual machine where I've installed [Anaconda](https://www.anaconda.com/distribution/).

#### [Install ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake#installation) (assuming you already have Python installed)

#### [Install py-trello](https://pypi.org/project/py-trello/)

#### Create a Trello account (if you don't have one), and get your Trello API key, API secret, and token.  See: https://trello.com/app-key

#### Create a Trello board (if you don't have one) and a Trello list to hold the cards that the script will create.

#### Modify aspace-to-trello.py to supply your Trello API credentials, Trello board name, and Trello list name. Altenatively, you can supply the board ID and list IDs (see comments in code for "Option 1")

Replace brackets with your Trello API credentials: 
  ```
    #Authenticate with Trello (change credentials to your own)
    trello_client = TrelloClient(
        api_key='[Trello API Key]',
        api_secret='[Trello API Secret]',
        token='[Trello API Token]',
    )
  ```

Replace brackets with your Trello Board name (string must match exactly):
  
  ```
  #Option 1: Get Trello Board by ID
  #target_board = trello_client.get_board('[Trello Board ID]')

  #Option2: Get Trello Board by Name
  trello_boards = trello_client.list_boards()
  for board in trello_boards:
      if board.name == '[Trello Board Name]': #board name lookup
          target_board = board
          print ("Target Board: " + target_board.name)
  ```
 
Replace 'New Accessions' with your Trello list name:

    ```
    #Option 1: Get Trello List by ID
    #target_list = trello_client.get_list('[Trello List ID]')
        
    #Option 2: Get Trello List by Name
    for trello_list in target_board.list_lists():
        if trello_list.name == 'New Accessions': #list name
            target_list = trello_list
            print("Target List: " + target_list.name)
    ```
    
#### Modify aspace-to-trello.py to supply your ArchivesSpace backend URL, username, and password as well as the ID of your target repository (e.g. /repositories/2/accessions/). Your ArchivesSpace user must have permission to view accession records in this repository.

Replace brackets with ASpace API URL, username, and password:
  ```
  #ASNAKE
  #Log Into ASpace and set repo
  aspace_client = ASnakeClient(baseurl="[ArchivesSpace backend API URL]",
                        username="[AS Username]",
                        password="[AS Password]")
  aspace_client.authorize()
  #Set Target Repository
  ```

Provide ID for target ASpace repository (change 2 in snippet below to your target repository ID):
  ```
  repo = aspace_client.get("repositories/2").json()
  print(repo['name'])
  accessions_list = aspace_client.get("repositories/2/accessions?all_ids=true").json()
  ```

#### Modify aspace-to-trello.py to assign custom labels to Trello cards or to assign cards to Trello board members (see code comments for details). To assign labels to cards, label values must already exist in the Trello board.

#### Determine how often you want to search for new accessions and create Trello cards for them. The script is currently configured to look for accessions created in the last 24 hours:
```
#Set time interval here (to get accessions created in last 24 hours)
current_time_minus_day = current_time - timedelta(hours=24)
```

#### Set up a cron job to execute the script every 24 hours at a specified time. Configure email notifications if you wan't to keep tabs on the script.

## Some screenshots
#### Sample Trello List
![Sample Trello List](/screenshots/trello_card_list.JPG)

#### Sample Trello Card created by aspace-to-trello.py
![Sample Trello Card](/screenshots/trello_card_example.JPG)

#### Sample script output
```
nh48@vm:~$ python aspace-to-trello.py
Target Board: Accession_to_Trello_test
Target List: New Accessions
Getting all Accessions created since: 2020-01-05T21:45:27.457600
David M. Rubenstein Rare Book & Manuscript Library
Examining last 20 accessions created in ASpace...
UA2019-0112 not entered in last 24 hours
UA2019-0113 not entered in last 24 hours
UA2019-0114 not entered in last 24 hours
2019-0190 not entered in last 24 hours
2019-0191 not entered in last 24 hours
2019-0192 not entered in last 24 hours
2019-0193 not entered in last 24 hours
2019-0194 not entered in last 24 hours
2019-0195 not entered in last 24 hours
2019-0196 not entered in last 24 hours
2019-0197 not entered in last 24 hours
2019-0198 not entered in last 24 hours
2019-0199 not entered in last 24 hours
2019-0200 not entered in last 24 hours
2019-0201 not entered in last 24 hours
2019-0202 not entered in last 24 hours
2020-0001 not entered in last 24 hours
UA2019-0115 not entered in last 24 hours
Creating New Trello Card for: UA2020-001: East Campus Library blueprints | entered on: 2020-01-06T19:25:35Z | university_archives
Creating New Trello Card for: UA2020-0002: Richard Nixon and John Bradway correspondence | entered on: 2020-01-06T19:49:25Z | university_archives
All Done!
nh48@vm:~$
```

## Things to consider
- Trello cards are only a snapshot of ArchivesSpace data (nothing is synced). Updating Trello cards has no effect in ArchivesSpace and vice versa.
- Trello cards only contain a subset of metadata in an accession record (if you're feeling ambitious, you can modify the script to add more fields)


