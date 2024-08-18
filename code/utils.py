import os
import re
import requests
from typing import Dict


def get_xml_url(
        url: str,
        headers: Dict[str, str]
) -> str:

    bv = re.findall(r'(BV.{10})', url)[0]

    response = requests.get(
        url='https://www.bilibili.com/video/' + bv,
        headers=headers
    )

    content = response.text
    cid = re.findall(r'"cid":(\d+),', content)[0]
    xml_url = f'https://comment.bilibili.com/{cid}.xml'

    return xml_url


def set_path(
        path: str
) -> str:
    if path is None:
        path = os.getcwd()
        print('The current working directory is:', path)
        print(
            'If you want to use the current path, please enter\'0\'.'
            'And if you want to use another path, please enter the path.'
        )
        input_info = eval(input('Please enter:'))
        if input_info == 0:
            path = path
        else:
            path = input_info
    else:
        path = path

    return path
