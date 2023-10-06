import xml.etree.ElementTree as ET
import requests
import math
import pandas as pd
import numpy as np

import cProfile

def read_xml_from_url(url):
    """Makes a get request to the given url if the address is good (status code == 200) 
    Args:
        url (str): URL of xml data
    Returns:
        bytes: content of the get request in bytes
    """    
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





def game_reviews_df(root_element, title, year_pub):
    comments = root_element.find('.//item/comments')

    dict_list = [{'title': title, 'year_pub': year_pub, 'game_id': id, 'username': comment.get('username'), 
                  'rating': comment.get('rating')}
                 for comment in comments.findall('comment')]

    return dict_list

id = 1
page = 1
base_url = "https://boardgamegeek.com//xmlapi2/thing?id={}&ratingcomments=1&page={}&pagesize=100"
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

    dict_list = game_reviews_df(root_element, title, year_pub)
    big_dict_list.extend(dict_list)

    print(page)
    page += 1

game_df = pd.DataFrame(big_dict_list)



