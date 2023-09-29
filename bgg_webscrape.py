import xml.etree.ElementTree as ET
import requests


def read_xml_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        return root
    except ET.ParseError as e:
        print(f"Error: Unable to parse XML data. {e}")
        return None


id=1


url = f"https://boardgamegeek.com//xmlapi2/thing?id={id}&ratingcomments=1&page=1&pagesize=100"  # Replace with your XML URL
xml_data = read_xml_from_url(url)

if xml_data is not None:
    root_element = parse_xml(xml_data)
    if root_element is not None:
        
        #get the title of the boardgame
        for name_element in root_element.findall('.//item/name'):
            if name_element.attrib['type'] == 'primary':
                title=name_element.attrib['value']
        #get the publication year
        year_pub=int(root_element.find('.//item/yearpublished').attrib['value'])
        
        #get the ratings and usernames
        comments = root_element.find('.//item/comments')
        total_num_comments=int(comments.attrib['totalitems'])
        for comment in comments.findall('comment'):
            rank = comment.get('rating')
            username = comment.get('username')
            print(username, rank)
        













