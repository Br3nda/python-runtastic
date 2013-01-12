import sqlite3
import urllib
import logging
import json
import urllib2
import re

logger = logging.getLogger('runtastic')
_URL = 'http://www.runtastic.com/api/'

def request(path, postfields):
    headers = {}

    params = urllib.urlencode(postfields)
    url = _URL + path
    logger.debug("Url = {url}".format(url=url))

    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req, params)
    
    logger.debug(response)

    #parse from json
    return json.loads(response.read())


class Statistics(object):
    def __init__(self, user_id):
        self.user_id = user_id
        
    def week(self, weeks_ago=0):
        response = request('statistics/week.json', postfields={
            'weeks_ago': weeks_ago,
            'user_id': self.user_id})
        print response
        
        for data in response:
            print data
        return response
    
class TrainingHistory(object):
    
    def __init__(self, user_id):
        self.user_id = user_id
        
    def month(self, month):
        activities = []
        for data in request('statistics/training_history/month',  postfields={'compare': None,	
            'field':	'count',
            'js_timezone_offset':	-780,
            'kind':	1,
            'locale':	'en',
            'period':	'month',
            'period_end':	month,
            'sport_types':	3,
            'user_id':	self.user_id,
            'users': None}):
            
            a = Activity(activity_id=data[0])
            a.populate(data)
            activities.append(a)
        return activities
    
class Activity(object):
    def __init__(self, activity_id):
        self.activity_id = activity_id
        
    def populate(self, data):
        """
        Populate with data from runtastic query
        """
        self.data = data
        
    def __str__(self):
        return "{id} {data}".format(id=self.activity_id, data=self.data)
        


