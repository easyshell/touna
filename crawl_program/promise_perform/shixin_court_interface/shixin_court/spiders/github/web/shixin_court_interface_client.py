#!/usr/bin/python
#-*-coding:utf-8-*-
import re
import sys
import json
import time
import copy
import scrapy
import requests
import urlparse
import ConfigParser
from scrapy import Request
from datetime import datetime
from bs4 import BeautifulSoup
from main.main_1 import code
from scrapy.conf import settings
from scrapy.selector import Selector
from collections import defaultdict
from scrapy.http import HtmlResponse
from bottle import run, post, request

def get_shixin_execute_information(name="", cardnum="", province=0):
	url = "http://localhost:8080/execute_info"
	try:
		form_data = {
			"name":name,
			"cardnum":cardnum
		}
		r = requests.post(url, data=form_data)
		print(r.content)
	except Exception as e:
		print(e)

get_shixin_execute_information("王茂旭")



