#!/usr/bin/python3
"""
August 15, 2020
Author: Gregory Abrasaldo

prerequisites:
pip3 install todoist-python

https://todoist-python.readthedocs.io/en/latest/todoist.html
https://developer.todoist.com/sync/v8/?python#add-an-i
"""

from todoist.api import TodoistAPI
from datetime import date

conkydir = '~/'
conkyfile= '.conkyrc'

# Get your API token from https://todoist.com/prefs/integrations 
TodoistAPIkey = 'your api token'


# add a \n to the end of the string. just a workaround
# add the following lines to your .conkyrc so that the script knows
# where to place the todo items.
start_text_capture = '#python-conky-todoist insert here\n'
end_text_capture   = '#python-conky-todoist insert ends here\n'



def sync():
    """
    Uses official python TodoistAPI to sync the to-do items for the day
    """
    api = TodoistAPI(TodoistAPIkey,cache='/todoist-conky-cache/')
    api.reset_state()
    api.sync()

    #today = '2020-08-11' # must be 'YYYY-MM-DD'
    today = str(date.today())

    todoitem = [today+':']

    #api.state['items'] contains the entries
    for i in api.state['items']:
        try:
            if today in i['due']['date']:
                todoitem.append(i['content'])
        except TypeError:
            continue
    
    return([i+'\n' for i in todoitem])

def find_clear_write():
    #Find the text_captures
    with open(conkydir+conkyfile, 'r') as cfile:
        content = cfile.readlines()
    indexes = [i for i,x in enumerate(content) if x in (start_text_capture, end_text_capture)]
    
    #Clear the text within the text_captures
    del content[indexes[0]+1:indexes[1]]

    #Write the updated text in between text_captures
    content[indexes[0]+1:indexes[0]+1] = sync()
    with open(conkydir+conkyfile,'w') as output:
        output.writelines(content)

def main():
	find_clear_write()

if __name__=="__main__":
	main()