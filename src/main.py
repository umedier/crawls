import re
from loguru import logger

from douyin import douyin

def parse_url(url):
    url = re.findall('[a-zA-z0-9]+:\/\/[^\s]*', url)
    if 'douyin.com' in url[0]:
        logger.info('抖音')
        douyin(url[0])
    else :
        logger.error('不支持该链接!')
    