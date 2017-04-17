#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import urllib.request
import logging
import logging.handlers
from time import sleep

from conf import mastodon


# logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - %(message)s')
handler = logging.handlers.TimedRotatingFileHandler(
    filename='downloads.log',
    when='D',
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


def download(url, dir_name='tmp'):
    filename = ''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    try:
        res = urllib.request.urlopen(url)
        filename = os.path.join(dir_name, os.path.basename(url))
        with open(filename, 'wb') as f:
            f.write(res.read())
    except Exception as e:
        logging.error(str(e, 'utf-8'))
    return filename


def tags(toot):
    tags = []
    for tag in toot['tags']:
        name = tag['name']
        tags.append(name)
    return ','.join(tags)


def main():
    tl = mastodon.timeline_local()
    for row in tl:
        dir_name = 'tmp'
        if row['sensitive'] is True:
            dir_name = 'dl'

        attachments = row['media_attachments']
        for attachment in attachments:
            url = attachment['url'].split('?')[0]
            filename = download(url, dir_name)
            log = {
                'text_url': attachment['text_url'],
                'url': url,
                'tags': tags(row),
                'username': row['account']['username'],
                'account_url': row['account']['url'],
                'sensitive': row['sensitive'],
                'file': filename
            }
            logger.info(json.dumps(log))


if __name__ == '__main__':
    while True:
        main()
        sleep(5)
