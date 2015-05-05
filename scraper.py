import requests
import json
import pprint
import sys
import codecs


TOKEN = 'CAACEdEose0cBAME32F1iq1SL2uKEEt57XEwmzTgtWfRhmT4w4ZBJMcNmfRjKTNucE90GcKUY1SC0Vc0ZAdd7gwy5QXfvbvV32tZC6hvHPznKrqwBf8G5hKaW263Mejy44xjzltLZAavYQZBLXZBP6qu0XrNZBOkklCAvLoKcf7Gz6ZAy8W3m9y6c4mZBO5LitiBmVXYVqctIveFdVOVfcG2THedYAFeusE0sZD'

def get_posts():
    """
        Returns the list of posts on my timeline
    """

    parameters = {'access_token': TOKEN}
    r = requests.get('https://graph.facebook.com/SistemaDeLectoYEscrituraDelIdiomaNgabe?fields=posts.limit(20)', params=parameters)
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
    # print posts 
    nodes = [] 
    links = []

    #Initial CoreNode
    coreNode = {'name' :'Sistema de lecto y escritura del Idioma Ngabe',
                'id' : '1',
                'nodeType':'coreNode'
                }
    
    nodes.append(coreNode)

    for p in posts:
        # postNode parsing    
        postNode = {}
        postNode['nodeType'] = 'postNode'
        postNode['id'] = p['id']
        if  'name' in p:
            postNode['name'] = p['name'] #relationship event actor. 
        if  'message' in p:
            postNode['message'] = p['message']
        if  'description' in p:
            postNode['description'] = p['description']
        if 'type' in p:
            postNode['media_type'] = p['type']

        # postNode Size Calculation: 
        like_count = 0
        if 'likes' in p:
            likedata =  p['likes']['data']
            for i in likedata:
                #likerNode parsing
                likerNode = {}
                likerNode['nodeType'] = 'likerNode'
                likerNode['id'] = i['id']
                likerNode['name'] = i['name']
                likerNode['size'] = 1 
                like_count = like_count + 1
                #add likerNode
                nodes.append(likerNode)

                # add link from likerNode to post. 
                likeLink = {}
                likeLink['source'] = i['id']
                likeLink['target'] = p['id']
                likeLink['type'] = 'likeLink'
                links.append(likeLink)

        share_count = 0
        if 'shares' in p: 
            share_count = int ( p['shares']['count'])

        size = 1 + like_count + share_count #adding 1 to offset the zero
        
        postNode['size'] = size
        # add postNode 
        nodes.append(postNode)

        # taggedNode
        taggedNode = {}
        if 'message_tags' in p: 
            tags = p['message_tags']
            # print tags
            for key in tags.items():
                taggedNode = {} 
                taggedNode['nodeType'] = 'taggedNode'
                taggedNode['id'] = key[1][0]['id']
                taggedNode['name'] = key[1][0]['name']
                taggedNode['size'] = 1

                # link taggedNode to post. 
                tagLink = {}
                tagLink['source'] = key[1][0]['id']
                tagLink['target'] = p['id']
                tagLink['type'] = 'tagLink'
                links.append(tagLink)

        # Add taggedNode  
        nodes.append(taggedNode)






        # Link
        coreLink = {}
        # coreLink evert PostNode to CoreNode (All posts linked to core node).
        coreLink['source'] = '1'   # all being set to initial node for now. 
        coreLink['target'] = p['id']
        coreLink['type'] = 'coreLink'
        links.append(coreLink)

result = {}
result['nodes'] = nodes
result['links'] = links

print json.dumps(result)
# res = json.dumps(result, ensure_ascii=False)

# string = unicode(res, 'utf8')
# output = string.encode('utf8', 'replace')
# f = open('panama.json', 'w+')
# f.write(output)

# f = codecs.open('file.txt', encoding='utf-8')
# f.write(res)


# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(result)


# Node 0, core  
# Node 1, post  (All posts linked to core Node.)
# Node 2, person who tags
# Node 3, person who likes 


# JSON structure. 
#   "nodes": [
#     {
#       "name": "node 1",
#       "artist": "artist name",
#       "id": "unique_id_1",
#       "playcount": 123
#     },
#     {
#       "name": "node 2",
#       # ...
#     }
#   ],
#   "links": [
#     {
#       "source": "unique_id_1",
#       "target": "unique_id_2"
#     },
#     {
#       # ...
#     }
#   ]
# }


# "story_tags": {
#   "0": [
#     {
#       "id": "560058540683250", 
#       "name": "Sistema de lecto y escritura del Idioma Ngabe", 
#       "type": "page", 
#       "offset": 0, 
#       "length": 45
#     }
#   ], 
#   "53": [
#     {
#       "id": "333272283404404", 
#       "name": "Movimiento 10 De Abril .m-10", 
#       "type": "page", 
#       "offset": 53, 
#       "length": 28
#     }
#   ], 
#   "84": [
#     {
#       "id": "675130919218537", 
#       "name": "", 
#       "offset": 84, 
#       "length": 5
#     }
#   ]
# },