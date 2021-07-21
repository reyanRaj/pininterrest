from flask import Flask
from flask import request
import requests
from flask import url_for
from markupsafe import escape
import bs4, json, re, requests
app = Flask(__name__)

@app.route('/get/<url>')
def show_url(url):
	return getRespone(url)
	
@app.route('/')
def get():
	url = request.args['url']
	return getRespone(url)


def getJson(html):
    soup = bs4.BeautifulSoup(html, "html.parser")

    # Get json script
    scriptTag = soup.find(
                'script',
                {
                    'id': 'initial-state',
                    'type': 'application/json'
                }
            )

    # Extract json inside script
    return json.loads(re.findall(r'>(.*)<', str(scriptTag))[0])

def getHtml(url):
    # Redirect to main pin if shortened
    if 'pin.it' in url:
        url = requests.get(url).url
    
    _id = re.findall(r'/pin/(\d+)', url)[0]
    
    return _id, requests.get(url).text

def decideType(jsonData):
    response = jsonData['resourceResponses'][0]['response']
    
    # Handle if 404
    if response['status'] != 'success':
        return None, None
    
    data = response['data']
    
    # Get Video
    if data['videos']:
        return 0, data['videos']['video_list']['V_720P']['url']
    
    # Get Gif
    if data['embed']:
        return 1, data['embed']['src']
    
    # Get Image
    return 2, data['images']['orig']['url']


def unshorten_url(url):
   

	session = requests.Session()  # so connections are recycled
	resp = session.head(url, allow_redirects=True)
	print(resp.url)
	return(resp.url)
        
def getRespone(url):
	
	TYPES = [
	    'Video',
	    'GIF',
	    'Image',
	    ]
	link = unshorten_url(url)
	if link.find('sent') != -1:
    		print(link.find('sent'))
    		link = link[0:link.find('sent')]
    		print(link)
	ID, HTML           =      getHtml(link)
	JSON               =      getJson(HTML)
	TYPE, MEDIA_URL    =      decideType(JSON)

	if TYPE == None:
	    return ('Nothing Found!')
	    exit(0)
	return (MEDIA_URL)


	
	
