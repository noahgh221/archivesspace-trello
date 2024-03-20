from asnake.client import ASnakeClient
from datetime import datetime, timedelta
from trello import TrelloClient
import trello
import json

#Script uses ArchivesSpace API and Trello API to lookup recent accession records in ASpace and create new Trello cards for them.
#Set up a cron job to execute the script at some interval (currently written to execute every day)

#uses py-trello: https://pypi.org/project/py-trello/
#See: https://github.com/sarumont/py-trello/blob/master/trello/trellolist.py
#See: https://buildmedia.readthedocs.org/media/pdf/py-trello-dev/latest/py-trello-dev.pdf
#Trello board, list, name ids can be obtained by adding .json to trello URLs

#Trello API Docs: https://developers.trello.com/reference#introduction


# "Monkey patching" to get this to work while we wait for library update
# from: https://github.com/sarumont/py-trello/issues/373
def patched_fetch_json(self,
                       uri_path,
                       http_method='GET',
                       headers=None,
                       query_params=None,
                       post_args=None,
                       files=None):
    """ Fetch some JSON from Trello """

    # explicit values here to avoid mutable default values
    if headers is None:
        headers = {}
    if query_params is None:
        query_params = {}
    if post_args is None:
        post_args = {}

    # if files specified, we don't want any data
    data = None
    if files is None and post_args != {}:
        data = json.dumps(post_args)

    # set content type and accept headers to handle JSON
    if http_method in ("POST", "PUT", "DELETE") and not files:
        headers['Content-Type'] = 'application/json; charset=utf-8'

    headers['Accept'] = 'application/json'

    # construct the full URL without query parameters
    if uri_path[0] == '/':
        uri_path = uri_path[1:]
    url = 'https://api.trello.com/1/%s' % uri_path

    if self.oauth is None:
        query_params['key'] = self.api_key
        query_params['token'] = self.api_secret

    # perform the HTTP requests, if possible uses OAuth authentication
    response = self.http_service.request(http_method, url, params=query_params,
                                            headers=headers, data=data,
                                            auth=self.oauth, files=files,
                                            proxies=self.proxies)

    if response.status_code == 401:
        raise trello.Unauthorized("%s at %s" % (response.text, url), response)
    if response.status_code != 200:
        raise trello.ResourceUnavailable("%s at %s" % (response.text, url), response)

    return response.json()


trello.TrelloClient.fetch_json = patched_fetch_json

#Authenticate with Trello (change credentials to your own)
trello_client = TrelloClient(
    api_key='[Trello API Key]',
    api_secret='[Trello API Secret]',
    token='[Trello API Token]',
    #token_secret='your-oauth-token-secret'
)


#Option 1: Get Trello Board by ID
#target_board = trello_client.get_board('[Trello Board ID]')

#Option2: Get Trello Board by Name
trello_boards = trello_client.list_boards()
for board in trello_boards:
    if board.name == '[Trello Board Name]': #board name lookup
        target_board = board
        print ("Target Board: " + target_board.name)

#Create empty lists for holding Trello board member objects (modify as needed)
ada_members = []
economics_members = []
franklin_members = []
hom_members = []
human_rights_members = []
hartman_members = []
ias_members = []
literature_members = []
bingham_members = []
general_members = []
university_archives_members = []

#Assign Trello Board members to different research center lists based on center affiliation. Currently disabled
#Could be useful for auto-assigning cards to users based on center affiliation or some other info present in Acc. recs.
board_members = target_board.get_members()
#for member in board_members:
#    #print(member.username)
#    if member.username == 'noahhuffman':
#        general_members.append(member)
#        bingham_members.append(member)
#    if member.username == 'meghanlion':
#        general_members.append(member)
#    if member.username == 'tracyj7':
#        university_archives_members.append(member)
#    if member.username == 'laurinpenland':
#        general_members.append(member)

#Create empty lists for center labels. Labels must already exist in Trello board with names provided in for loop.
human_rights_label = []
general_label = []
ada_label = []
bingham_label = []
econ_label = []
franklin_label = []
hartman_label = []
hom_label = []
ias_label = []
lit_label = []
ua_label = []

#Get label objects by label name
board_labels = target_board.get_labels()
for label in board_labels:
    #print (label.id + " | " + label.name)
    if label.name == 'Human Rights':
        human_rights_label.append(label)
    elif label.name == 'General':
        general_label.append(label)
    elif label.name == 'ADA':
        ada_label.append(label)
    elif label.name == 'Econ':
        econ_label.append(label)
    elif label.name == 'JHF':
        franklin_label.append(label)
    elif label.name == 'Hartman':
        hartman_label.append(label)
    elif label.name == 'HOM':
        hom_label.append(label)
    elif label.name == 'IAS':
        ias_label.append(label)
    elif label.name == 'Lit':
        lit_label.append(label)
    elif label.name == 'UA':
        ua_label.append(label)
    elif label.name == 'Bingham':
        bingham_label.append(label)


#Option 1: Get Trello List by ID
#target_list = trello_client.get_list('[Trello List ID]')

#Option 2: Get Trello List by Name
for trello_list in target_board.list_lists():
    if trello_list.name == 'New Accessions': #board name
        target_list = trello_list
        print("Target List: " + target_list.name)

#Sample code for working with cards in lists
#card_list = target_list.list_cards()
#for card in card_list:
    #print(card.name)

#What Time is is? Trello Time! Set time to now
current_time= datetime.utcnow()

#Set time interval here (to get accessions created in last 24 hours)
current_time_minus_day = current_time - timedelta(hours=24)

#Convert time to ISO format for comparing to create dates in ASpace
current_time_minus_day = current_time_minus_day.isoformat()

print("Getting all Accessions created since: " + str(current_time_minus_day))

#ASNAKE
#Log Into ASpace and set repo to RL
aspace_client = ASnakeClient(baseurl="[ArchivesSpace backend API URL]",
                      username="[AS Username]",
                      password="[AS Password]")
aspace_client.authorize()
#Set Target Repository
repo = aspace_client.get("repositories/2").json()
print(repo['name'])

accessions_list = aspace_client.get("repositories/2/accessions?all_ids=true").json()
#Sort accessions by ASpace ID (e.g. repositories/2/accessions/1234)
accessions_sorted = sorted(accessions_list)

#Just get the last 20 created accessions in ASpace (based on IDs, not create time)
#assuming we won't create more than 20 accessions in time interval between cron jobs
#get last 20 accessions in list (most recent accession will be last in list)
last_20_accessions = accessions_sorted[-20:]

print("Examining last 20 accessions created in ASpace...")

for accession in last_20_accessions:
    accession_json = aspace_client.get("repositories/2/accessions/" + str(accession)).json()
    #get some metadata for each accession
    accession_createtime = accession_json['create_time']
    #Account for various identifier practices (eg. 2 part vs. 1 part - Duke uses 2 part)
    try:
        accession_identifier = accession_json['id_0'] + "-" + accession_json['id_1']
    except:
        accession_identifier = accession_json['id_0']
       #get only accessions with create dates since cron job last executed
    if accession_createtime > current_time_minus_day:
        #Get Some metadata from AS accession record to populate Trello Card (e.g. ID, Title, Extent, Description, etc.)
        #If no data in ASpace, supply some placeholder data
        try:
            accession_title = accession_json['title']
        except:
            accession_title = 'NO TITLE in ASPACE'
        try:
            accession_date = accession_json['accession_date']
        except:
            accession_date = 'NO ACC DATE IN ASPACE'
        try:
            accession_acq_type = accession_json['acquisition_type']
        except:
            accession_acq_type = 'NO Acq. Type in ASPACE'
        try:
            content_description = accession_json['content_description']
        except:
            content_description = ''
        try:
            inventory_text = accession_json['inventory']
        except:
            inventory_text = ''
        try:
            special_media_format_text = accession_json['user_defined']['text_1']
        except:
            special_media_format_text = ''
        try:
            notes_for_processor_text = accession_json['collection_management']['processing_plan']
        except:
            notes_for_processor_text = ''
        #Get related resources
        related_resources_list = []
        #This is probably not the best way...but seems to work
        try:
            if 'ref' in accession_json['related_resources'][0]:
                for resource in accession_json['related_resources']:
                    resource_uri = resource['ref']
                    resource_json = aspace_client.get(resource_uri).json()
                    resource_text = resource_json['title'] + " | " + resource_uri
                    related_resources_list.append(resource_text)
                related_resources_text = ''.join(related_resources_list)
            else:
                related_resources_text = 'NONE listed in ASpace'
        except:
            related_resources_text = 'NONE listed in ASpace'
        try:
            provenance_note = accession_json['provenance']
        except:
            provenance_note = ''

        try:
            #Research center is a User Defined Field (enum2) in Duke's ASpace instance
            accession_research_center = accession_json['user_defined']['enum_2']
        except:
            accession_research_center = 'NO CENTER ASSIGNED'
        try:
            accession_extent = accession_json['extents'][0]['number'] + " " + accession_json['extents'][0]['extent_type']
        except:
            accession_extent = 'NO EXTENT IN ASPACE'
        try:
            accession_container_summary = " (" + accession_json['extents'][0]['container_summary'] + ")"
        except:
            accession_container_summary = ''
        accession_extent = accession_extent + accession_container_summary
        #Concat Accession ID and Title for Trello Card Titles (e.g. 2020-0001: John Doe Papers)
        card_title = accession_identifier + ": " + accession_title
        #concat a bunch of fields to card_description variable and add some linebreaks, add some markdown too for bolding field labels
        card_description = "**Acq Type**: " + accession_acq_type + "\n" + "**Accn Date**: " + accession_date + "\n" "**Extent**: " + accession_extent + "\n\n" + "**Provenance**: " + provenance_note + "\n\n" + "**Note for Processor**: " + notes_for_processor_text + "\n\n" + "**Inventory**: " + inventory_text + "\n\n" + "**Special Media Formats**: " + special_media_format_text + "\n\n" + "**Related Resource(s)**: " + related_resources_text + "\n\n" + "**Description**: \n\n" + content_description
        print("Creating New Trello Card for: " + card_title + " | entered on: " + str(accession_createtime) + " | " + accession_research_center)
        #create cards in target_list, assign labels and assign members based on center names in ASpace accession records
        #new cards are added to top of list (position = top)
        if accession_research_center == 'ada':
            target_list.add_card(card_title, desc=card_description, labels=ada_label, position="top", assign=ada_members)
        elif accession_research_center == 'bingham':
            target_list.add_card(card_title, desc=card_description, labels=bingham_label, position="top", assign=bingham_members)
        elif accession_research_center == 'economics':
            target_list.add_card(card_title, desc=card_description, labels=econ_label, position="top", assign=economics_members)
        elif accession_research_center == 'franklin':
            target_list.add_card(card_title, desc=card_description, labels=franklin_label, position="top", assign=franklin_members)
        elif accession_research_center == 'general':
            target_list.add_card(card_title, desc=card_description, labels=general_label, position="top", assign=general_members)
        elif accession_research_center == 'hartman':
            target_list.add_card(card_title, desc=card_description, labels=hartman_label, position="top", assign=hartman_members)
        elif accession_research_center == 'hom':
            target_list.add_card(card_title, desc=card_description, labels=hom_label, position="top", assign=hom_members)
        elif accession_research_center == 'human_rights':
            target_list.add_card(card_title, desc=card_description, labels=human_rights_label, position="top", assign=human_rights_members)
        elif accession_research_center == 'ias':
            target_list.add_card(card_title, desc=card_description, labels=ias_label, position="top", assign=ias_members)
        elif accession_research_center == 'literature':
            target_list.add_card(card_title, desc=card_description, labels=lit_label, position="top", assign=literature_members)
        elif accession_research_center == 'university_archives':
            target_list.add_card(card_title, desc=card_description, labels=ua_label, position="top", assign=university_archives_members)
        #If No Center Assigned
        else:
            target_list.add_card(card_title, desc=card_description, position="top")
    else:
        print(accession_identifier + " not entered in last 24 hours")

print("All Done!")
