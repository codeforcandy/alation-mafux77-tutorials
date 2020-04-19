import json
import time
from bs4 import BeautifulSoup

from zipfile import ZipFile
from contextlib import closing


from datetime import datetime as pydatetime
def to_unix_time(dt):
    epoch = pydatetime.fromtimestamp(0, dt.tzinfo)
    delta = dt - epoch
    return delta.total_seconds()



def extract_files(base_path):
    with closing(ZipFile(base_path + 'ABOK_media_files.zip', 'r')) as myzip:
        x = myzip.extractall()


def list_files(base_path):
    try:
        with closing(ZipFile(base_path + 'ABOK_media_files.zip', 'r')) as myzip:
            return myzip.NameToInfo.keys()
    except:
        return []

def log_me(txt):
    try:
        print ("{} {}".format(
            time.strftime(u"%Y-%b-%d %H:%M:%S", time.localtime()),
            txt))
    except:
        print ("{} Formatting issue with a log message.".format(
            time.strftime(u"%Y-%b-%d %H:%M:%S", time.localtime())))


def parse_t_metadata(r):
    if r.status_code==200:
        t = json.loads(r.content)
        return t
    else:
        return r.content


def parse_bulk_medata(r):
    if r.status_code==200:
        t = json.loads(r.content)
        if t['error'] == '':
            t="Created {}, updated {}".format(t['new_objects'], t['updated_objects'])
        else:
            t="Error: {}".format(t['error_objects'])
        return t
    else:
        return r.content


def unpack_children(c):
    if len(c)>0:
        return [child['id'] for child in c]
    else:
        return None

def unpack_id(x):
    if len(x)>0:
        return x[0]['id']
    else:
        return None


def unpack_title(x):
    if len(x)>0:
        return x[0]['title']
    else:
        return None

def get_user(u):
    return "<{}> {}".format(u['username'], u['display_name'])

def get_users(u):
    return ["<{}> {}".format(u['username'], u['display_name']) for x in u]

def unlist(s):
    try:
        r = s['userid']
    except:
        pass

def unpack(s):
    try:
        log_me("Called on {}".format(s))
    except:
        log_me("Called on something unformattable")
    if isinstance(s, dict):
        if 'download_url' in s:
            return(s['download_url'])
        elif 'username' in s:
            return(s['username'])
        else:
            return(s)
    elif isinstance(s, list):
        r = []
        for s0 in s:
            if 'download_url' in s0:
                r.append(s0['download_url'])
            elif 'username' in s0:
                r.append(s0['username'])
            elif 'otype' in s0:
                r.append(s0['url'])
            elif 'field_name' in s0:
                try:
                    r.append("{}:{}={}".format(s0['value_type'], s0['field_name'], s0['value']))
                except:
                    r.append(s0['value_type']+':'+s0['field_name']+'='+s0['value'])
            else:
                r.append(s0)
        return r
    else:
        return s

def touch_each(DataFrame): # a different col as a Series in each call
    d = DataFrame.apply(unpack)
    return d

def convert_references_for_any_string(text):
    soup = BeautifulSoup(text, "html5lib")
    # Find all Anchors
    match = soup.findAll('a')
    for m in match:
        # We only care about Alation anchors, identified by the attr data-oid
        if 'data-oid' in m.attrs:
            m.string = m.get_text()
            m['data-oid'] = 0
            del m['href']
            m['title'] = m.string
    return soup.prettify()
