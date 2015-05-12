# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import json
import pprint
import codecs
import operator

from datetime import datetime


TOKEN = 'CAACEdEose0cBALAoZCQ3wZCUei8nErgfqc6DklBQkTTnhES36auv02aFZA3OGUopDlMChPjWJd9kGZBRZBrrXEZAf0d9zTbA0fAbs9dtoEOFwlXGhpqZCEKVaRS6ITVNVZC2BXbBXCuydL6O7damdlJ0WXL8KlqPdiPz7h7XdSZA0LTm0Yjlc9HYzaZA1SWciD4YOHn00JIi1qj1W5Y4Q1Ikj3VCcertKjZCfsZD'

def get_request():
    parameters = {'access_token': TOKEN}
    r = requests.get('https://graph.facebook.com/SistemaDeLectoYEscrituraDelIdiomaNgabe?fields=posts.limit(20)', params=parameters)
    return r.text

def get_posts():
    """
        Returns the list of posts on my timeline
    """

    parameters = {'access_token': TOKEN}
    r = requests.get('https://graph.facebook.com/SistemaDeLectoYEscrituraDelIdiomaNgabe?fields=posts.limit(500)', params=parameters)
    result = json.loads(r.text)
    return result['posts']['data']

# posts = get_request();
# print posts

# with open('fb.data', 'r') as content_file:
#     content = content_file.read()

# posts = json.loads(content)['posts']['data']

posts = get_posts()

nodes = []
links = []

likers = {} #set of all the people and what they like. 

node_id_counter = 0; 

#####################################################################
#####################  ADDING CORE NODE
#####################################################################

# coreNode = {'name' :'Sistema de lecto y escritura del Idioma Ngabe',
#             'xid' : 0,
#             'nodeType':'coreNode',
#             'group' : 0
#             }
# node_id_counter = node_id_counter + 1 
# nodes.append(coreNode)


#####################################################################
#####################  ADDING ALL POST NODES
#####################################################################

# Add all the postNodes first
for p in posts: 
    postNode = {}
    # assign an id to postNode
    postNode['xid'] = node_id_counter
    #increment node_id_counter
    node_id_counter = node_id_counter + 1

    postNode['nodeType'] = 'postNode'

    postNode['fb_id'] = p['id']
    if  'name' in p:
        postNode['name'] = p['name'] 
    if  'message' in p:
        postNode['message'] = p['message']
    if  'description' in p:
        postNode['description'] = p['description']
    if  'type' in p:
        postNode['media_type'] = p['type']
    if 'link' in p: 
        postNode['url'] = p['link']
    if 'created_time' in p:
        datestring =  p['created_time']
        dt = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S+0000')
        postNode['created_date'] = str(dt.year) +'-' + str(dt.month) + '-' + str(dt.month)
        postNode["year"] = dt.year
    nodes.append(postNode)

#####################################################################
#####################  YEAR NODES
#####################################################################
years = {} 
#set
for n in nodes:
    if 'year' in n:
        if n['year'] not in years:
            years[n['year']]= {} 
            years[n['year']]['year']= n['year']
            years[n['year']]['count'] = 1
        else:
            years[n['year']]['count'] = years[n['year']]['count'] + 1
#node 
for key in years:
    yearNode = {}
    yearNode["nodeType"] = "yearNode"
    yearNode["name"] = key
    yearNode["size"] = years[key]["count"]
    yearNode["xid"] = node_id_counter
    node_id_counter = node_id_counter + 1
    nodes.append(yearNode)


def getYearXIDbyYear(yr):
    for n in nodes:
        if n["nodeType"] == "yearNode":
            if yr == n['name']:
                return n['xid']
    return 0 #default to core node

#link  year -> posts
for key in years:
    for n in nodes:
        if 'year' in n:
            if key == n['year']:
                link = {} 
                link['source'] = getYearXIDbyYear(key)
                link['target'] = n['xid']
                link['linkType'] = "yearLink"
                links.append(link)


#####################################################################
#####################  LINKING ALL YEARS TO CORE NODE
#####################################################################
# Add all the links for the existing postNodes to the coreNode
# for pn in nodes:
#     if pn['nodeType'] == "yearNode":
#         link = {} 
#         link['source'] = coreNode['xid']
#         link['target'] = pn['xid']
#         link['linkType'] = "coreLink"
#         link['value'] = 1
        # links.append(link)



#####################################################################
#####################  LIKER NODES
#####################################################################
## SET CREATION
likers = {} 
for p in posts: 
    if 'likes' in p: 
        for li in p['likes']['data']:
            if li['name'] in likers: 
                likers[li['name']]['count'] = likers[li['name']]['count'] + 1
                likers[li['name']]['likes'].append(p['id'])
            else:
                likers[li['name']] = {}
                likers[li['name']]['name'] = li['name']
                likers[li['name']]['count'] = 1
                likers[li['name']]['likes'] = [p['id']] #fbid


## NODE CREATION 
for key in likers.items():
    likeNode = {}
    likeNode["nodeType"] = "likerNode"
    likeNode["name"] = key[1]['name']
    likeNode["size"] = key[1]['count']
    likeNode["xid"] = node_id_counter
    node_id_counter = node_id_counter + 1
    nodes.append(likeNode)



def getPostXIDbyFbID(fbID):
    for n in nodes:
        if 'fb_id' in n:
            if n['fb_id'] == fbID:
                return n["xid"]
    return 0 #default to core node

def getLikerXIDbyName(name):
    for n in nodes:
        if n["nodeType"] == "likerNode":
            if n['name'] == name:
                return n['xid']
    return 0 #default to core node

## LINK CREATION ( liker -> post).
for key in likers.items():
    for postFbID in  key[1]['likes']:
        likeLink = {}
        likeLink["linkType"] = "likeLink"
        likeLink["source"] = getLikerXIDbyName(key[1]['name'])
        likeLink["target"] = getPostXIDbyFbID(postFbID)
        likeLink["value"] = 1
        links.append(likeLink)


#####################################################################
#####################  TAGGED NODES
#####################################################################

## SER CREATION 
tagged = {}
for p in posts:
    if 'message_tags' in p:
        for key in p['message_tags'].items():
            if key[1][0]['name'] in tagged:
                tagged[key[1][0]['name']]['count'] = tagged[key[1][0]['name']]['count'] + 1
                tagged[key[1][0]['name']]['post_tags'].append(p['id'])
            else: 
                tagged[key[1][0]['name']] = {}
                tagged[key[1][0]['name']]['name'] = key[1][0]['name']
                tagged[key[1][0]['name']]['count'] = 1
                tagged[key[1][0]['name']]['post_tags'] = [p['id']] #fbid

## NODE CREATION
for key in tagged.items():
    taggedNode = {} 
    taggedNode["nodeType"] = "taggedNode"
    taggedNode["name"] = key[1]['name']
    taggedNode["size"] = key[1]['count']
    taggedNode["xid"] = node_id_counter
    node_id_counter = node_id_counter + 1
    nodes.append(taggedNode)


def getTaggedXIDbyName(name):
    for n in nodes:
        if n["nodeType"] == "taggedNode":
            if n['name'] == name:
                return n['xid']
    return 0 #default to core node

## LINK CREATION ( post -> taggedNode).
for key in tagged.items():
    for postFbID in key[1]['post_tags']:
        taggedLink = {}
        taggedLink["linkType"] = "taggedLink"
        taggedLink["source"] = getPostXIDbyFbID(postFbID) 
        taggedLink["target"] = getTaggedXIDbyName(key[1]['name'])
        taggedLink["value"] = 1
        links.append(taggedLink)




result = {}
result['nodes'] = nodes
result['links'] = links

print json.dumps(result)



