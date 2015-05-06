import requests
import json
import pprint
import sys
import codecs
import operator

TOKEN = 'CAACEdEose0cBAG0VbgX1ZB7DilLKfOk4V7CHWLah8XTbxHyMMTN4AVkohydTT8LzHf1XI1zDA0ngbOo1pLrNoIaJQ3hnfEiZADAGWlZCsxEeZBQbBwZBSkWMwGWI7cl20OkTHNlpMgM6Df1oIeAJHRlg5vU8ofdm8H5ty8pbZBRPh23nakwJBmdnfANNAyFIEqvz7lo8myAewx4FRmQLUE26XW1AcZC6XAZD'

def get_posts():
    """
        Returns the list of posts on my timeline
    """

    parameters = {'access_token': TOKEN}
    r = requests.get('https://graph.facebook.com/SistemaDeLectoYEscrituraDelIdiomaNgabe?fields=posts.limit(500)', params=parameters)
    result = json.loads(r.text)
    return result['posts']['data']

def comment_on_posts(posts):
    """Comments on all posts"""
    for post in posts:
        url = 'https://graph.facebook.com/%s/comments' % post['post_id']
        message = 'Commenting through the Graph API'
        parameters = {'access_token': TOKEN, 'message': message}
        s = requests.post(url, data = parameters)

if __name__ == '__main__':
    posts =  get_posts()
    nodes = [] 
    links = []

    id_count = 0
    #Initial CoreNode
    coreNode = {'name' :'Sistema de lecto y escritura del Idioma Ngabe',
                'id' : 0,
                'nodeType':'coreNode',
                'group' : 0
                }
    id_count = id_count + 1 

    nodes.append(coreNode)

    for p in posts:

        # postNode parsing    
        postNode = {}

        # assign an id to postNode
        postNode['id'] = id_count
        #increment id_count
        id_count = id_count + 1

        postNode['nodeType'] = 'postNode'
        postNode['fb_id'] = p['id']
        if  'name' in p:
            postNode['name'] = p['name'] #relationship event actor. 
        if  'message' in p:
            postNode['message'] = p['message']
        if  'description' in p:
            postNode['description'] = p['description']
        if 'type' in p:
            postNode['media_type'] = p['type']


        postNode['group'] = 1

        # postNode Size Calculation: 
        like_count = 0
        if 'likes' in p:
            likedata =  p['likes']['data']
            for i in likedata:
                # Check if liker exists already in the list of liker nodes. 
                # If it does exsit, then add a link from that existing Liker Node to this new post. 
                # If it does not exist, add the liker node,  as usual. 

                likerExists = False 
                likerID = -1
                for n in nodes:
                    if 'fb_id' in n:
                        # print n['fb_id'], i['id']
                        if n['fb_id'] == i['id']:
                            likerExists = True
                            likerID = n['id'] #save that id which exists. 


                if likerExists == True:
                    likeLink = {} 
                    likeLink['source'] = likerID
                    likeLink['target'] = postNode['id'] # links to current Node. 
                    likeLink['type'] = 'likeLink'
                    likeLink['value'] = 1
                    likeLink['debugsource'] = likerID
                    likeLink['debugtarget'] = postNode['id']                    
                else:
                    ##### LIKER NODE
                    likerNode = {}
                    likerNode['nodeType'] = 'likerNode'
                    likerNode['fb_id'] = i['id']
                    likerNode['name'] = i['name']
                    likerNode['size'] = 1 
                    likerNode['group'] = 2
                    like_count = like_count + 1
                    # id 
                    likerNode['id'] = id_count
                    id_count = id_count + 1
                    #add likerNode

                    # print '----------id count----', id_count;
                    # print '***********************','Adding likerNode with id:', likerNode['id'], '***********************'
                    # print likerNode
                    # print '***********************','***********************','***********************'
                    nodes.append(likerNode)

                    # add link from likerNode to post. 
                    likeLink = {}
                    likeLink['source'] = likerNode['id']
                    likeLink['target'] = postNode['id']
                    likeLink['type'] = 'likeLink'
                    likeLink['value'] = 1
                    likeLink['debugsource'] = likerNode['id']
                    likeLink['debugtarget'] = postNode['id']

                    links.append(likeLink)

        share_count = 0
        if 'shares' in p: 
            share_count = int ( p['shares']['count'])

        size = 1 + like_count + share_count #adding 1 to offset the zero
        
        postNode['size'] = size
        
           
        # print '----------id count----', id_count;       
        # print  '***********************', 'Adding PostNode with id:', postNode['id'], '***********************'
        # print postNode
        # print '***********************','***********************','***********************'
        nodes.append(postNode)


        # TAGGED NODE ##3
        taggedNode = {}
        if 'message_tags' in p: 
            tags = p['message_tags']
            for key in tags.items():
                taggedNode = {} 
                taggedNode['nodeType'] = 'taggedNode'
                taggedNode['fb_id'] = key[1][0]['id']
                taggedNode['name'] = key[1][0]['name']
                taggedNode['size'] = 1
                taggedNode['group'] = 3
                #add id to taggedNOde
                taggedNode['id'] = id_count
                id_count = id_count + 1

                # link taggedNode to post. 
                tagLink = {}
                tagLink['source'] = taggedNode['id'] 
                tagLink['target'] = postNode['id']
                tagLink['type'] = 'tagLink'
                tagLink['value'] = 1
                links.append(tagLink)

                # Add taggedNode    
                if taggedNode != {}:
                    # print "appending TAGGED", taggedNode, id_count
                    # print '----------id count----', id_count;
                    # print '***********************', 'Adding taggedNode with id:', postNode['id'],'***********************'
                    # print taggedNode
                    # print '***********************','***********************','***********************'
                    nodes.append(taggedNode)


        # Link
        # coreLink = {}
        # # coreLink evert PostNode to CoreNode (All posts linked to core node).
        # coreLink['source'] = 0   # all being set to initial node for now. 
        # coreLink['target'] = postNode['id']
        # coreLink['value'] = 1 
        # coreLink['debugsource'] = 0
        # coreLink['debugtarget'] = postNode['id']
        # coreLink['type'] = 'coreLink'
        # links.append(coreLink)



nodes.sort(key=operator.itemgetter('id'))


result = {}
result['nodes'] = nodes
result['links'] = links

print json.dumps(result)
