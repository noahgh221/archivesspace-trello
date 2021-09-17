# archivesspace-trello
aspace-to-trello.py creates Trello cards based on ArchivesSpace accession records. The script is designed to be run as a scheduled cron job. When executed, the script will first query the ArchivesSpace API to identify recently created accession records and then it will create Trello cards for those accession records on a specified Trello board and list.

Script is written in Python 3 and uses [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) and [py-trello](https://github.com/sarumont/py-trello).

## Use Case
- You use [ArchivesSpace](https://archivesspace.org) to create and manage accession records. 
- You use [Trello](https://trello.com) for project management and workflow tracking. 
- You're lazy, and don't want to copy/paste info about new accessions from ASpace into Trello.

## Getting Started 
### Download the python script (aspace-to-trello.py): 
Ideally, you'll want to save the script to a location where you have Python installed and can also execute cron jobs. For example, I run the script from a Linux virtual machine where I've installed the [Anaconda](https://www.anaconda.com/distribution/) distribution.

### [Install ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake#installation) (assuming you already have Python installed)

### [Install py-trello](https://pypi.org/project/py-trello/)

### Create a Trello account (if you don't have one), and get your Trello API key, API secret, and token: 

See: https://trello.com/app-key

### Create a Trello board and a Trello list to hold the cards that the script will create:

Or, if you already have a Trello account, board, and list, skip to the step below. 

### Supply your Trello API credentials:

Modify aspace-to-trello.py to supply your Trello API credentials, a Trello board name, and a Trello list name. Altenatively, you can supply the board ID and list IDs (see comments in code for "Option 1"). To get Trello board and list IDs, you can add .json to the end of any Trello URL and poke around in the JSON to locate the IDs.

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
    
### Authenticate with your ArchivesSpace instance:
Modify aspace-to-trello.py to supply your ArchivesSpace backend URL, username, and password as well as the ID of your target repository (e.g. /repositories/2/accessions/). Your ArchivesSpace user must have permission to view accession records in this repository.

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

Provide the ID for your target ASpace repository (e.g. change /2 in snippet below to the ID of your target repository):
  ```
  repo = aspace_client.get("repositories/2").json()
  print(repo['name'])
  accessions_list = aspace_client.get("repositories/2/accessions?all_ids=true").json()
  ```

### Assigning labels and members to Trello cards:
Modify aspace-to-trello.py to assign custom labels to Trello cards or to assign cards to Trello board members (see code comments for details). To assign labels to cards, label values must already exist in the Trello board.

As written, the script applies custom Trello card labels based on related values in a user defined field in Duke's ASpace instance. These labels mostly correspond to collecting areas (e.g. economics, university archives, etc.). At Duke, certain processors are reponsible for processing collections in certain collecting areas, so Trello cards can be assigned to Trello board members (staff) based on the collecting area values stored in ASpace accession records. This is all very Duke-specific. You'll probably want to modify the behavior or comment out these sections. 

### Setting a time interval:
Determine how often you want to search ArchivesSpace for new accessions and auto-generate Trello cards. The script is currently configured to run every 24 hours and look for accessions created in the last 24 hours:
```
#Set time interval here (to get accessions created in last 24 hours)
current_time_minus_day = current_time - timedelta(hours=24)
```

### Create a cron job:
Create a cron job to execute the script every 24 hours at a specified time. Configure email notifications if you wan't to receive emails about the script's activity and to make sure it's still executing as expected.

On Linux, create a new crontab file using the command below:
```
~$ crontab -e
```

Add a line in the crontab file with an instruction to execute aspace-to-trello.py at some interval. Save the file. In the example below, the script will execute every day at 01:00 AM and the output will be emailed to the specified email address 

```
MAILTO=your.email@email.edu
# Every Day at 01:00 AM
0 1 * * * python3 /home/[user]/aspace-to-trello.py
```

## Some screenshots

### Sample Trello List:
![Sample Trello List](/screenshots/trello_card_list.JPG)

### Sample Trello Card created by aspace-to-trello.py:
![Sample Trello Card](/screenshots/trello_card_example2.JPG)

### Sample script output:
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

## Things to consider:
- Trello cards are only a snapshot of ArchivesSpace data (nothing is synced). This is a very loose integration. Updating Trello cards has no effect on ArchivesSpace data and vice versa.
- Trello cards only contain a subset of metadata in an accession record (if you're feeling ambitious, you can modify the script to add more ArchivesSpace fields to your Trello cards or otherwise manipulate the ASpace data)
- As written, the script only examines the last 20 accession records created in ASpace and then determines which of those 20 accessions were created in the last 24 hours. If you regularly create more than 20 accessions per day, stop collecting so much stuff. If you can't, you'll want to modify the script to account for more accessions records per day.

Please submit a Github Issue if you have any questions about the script or these instructions.
