import xml.etree.ElementTree as ET
import requests
import math
import pandas as pd
import numpy as np
import time

# Create a session
session = requests.Session()

# Create an adapter with connection pool settings
adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=1)

# Mount the adapter to the session
session.mount('http://', adapter)
session.mount('https://', adapter)


def read_xml_from_url(url):
    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 429:
            print(f"Received 429 status code. Retrying in 5 seconds...")
            time.sleep(10)
            return read_xml_from_url(url)  # Retry the request
        else:
            print(f"Error: Unable to fetch data from {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None



def parse_xml(xml_data):
    """parses the xml data into an Element Tree

    Args:
        xml_data (bytes): get request content

    Returns:
        Element: Element tree xml structure
    """    
    try:
        root = ET.fromstring(xml_data)
        return root
    except ET.ParseError as e:
        print(f"Error: Unable to parse XML data. {e}")
        return None


def game_reviews_dict(root_element):
    comments = root_element.find('.//item/comments')
    dict_list = [{'username': comment.get('username'), 'rating': comment.get('rating')}
                 for comment in comments.findall('comment')]
    return dict_list







id = 1
page = 1
base_url = "https://boardgamegeek.com//xmlapi2/thing?id={}&ratingcomments=1&page={}&pagesize=100"
review_df_list=[]
game_dict_list=[]


for id in range(1,10):
    page=1
    big_dict_list = []
    dict_list=[np.nan]
    while len(dict_list)>0:
        format_url = base_url.format(id, page)
        xml_data = read_xml_from_url(format_url)

        if xml_data is None:
            break

        root_element = parse_xml(xml_data)

        if root_element is None:
            break

        if page == 1:
            title = next(name_element.attrib['value'] for name_element in root_element.findall('.//item/name') if name_element.attrib['type'] == 'primary')
            year_pub = int(root_element.find('.//item/yearpublished').attrib['value'])
            game_dict={'title':title, 'year_pub':year_pub, 'game_id':id}

        
        dict_list = game_reviews_dict(root_element)
        big_dict_list.extend(dict_list)

        print(page)
        page += 1

    review_df = pd.DataFrame(big_dict_list)
    review_df['rating']=review_df['rating'].astype(float)
    review_df['rating']=review_df['rating'].round()
    review_df['rating']=review_df['rating'].astype(int)

    game_dict['num_of_reviews']=len(review_df)

    review_df_list.append(review_df)
    game_dict_list.append(game_dict)


game_df=pd.DataFrame(game_dict_list)


