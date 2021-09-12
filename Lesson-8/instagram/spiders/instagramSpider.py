import scrapy
import json
import re
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem
import logindetail.txt



class InstagramSpider(scrapy.Spider):
    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    link = 'https://www.instagram.com/accounts/login/ajax/'
    
    
    with open('logindetail.txt', 'r') as detail:
        inst_login = detail.readline().replace('\n', '')
        inst_password = detail.readline().replace('\n', '')

    user = 'tommydate0'
    url = 'https://i.instagram.com/api/v1/friendships/'
   


    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_token(response.text)
        yield scrapy.FormRequest(self.link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_password},
                                 headers={'x-csrftoken': csrf_token})

    def user_login(self, response: HtmlResponse):
        response_to_json = response.json()
        if response_to_json['authenticated']:
            yield response.follow(f'/{self.user}', callback=self.user_parsing,
                                  cb_kwargs={'username': self.user})

    def user_parsing(self, response: HtmlResponse, username):
        user_id = self.fetch_user(response.text, username)        
        variables = {'count': 12,
                     'search_surface': "follow_list_page"}
        url_posts = self.url + f'{user_id}/followers/?{urlencode(variables)}'
        
        yield response.follow(url_posts,
                              callback=self.user_data,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)})

    def user_data(self, response: HtmlResponse, username, user_id, variables):
        response_json = response.json()
        
        info = response_json.get('next_max_id')
        if info:
            variables['max_id'] = info
            url_posts = self.graphql_url + f'{user_id}/followers/?{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_data,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)})

 
        users = response_json.get('users')
        for user in users:
            item = InstagramItem(user_id=user_id,
                                   follow_id=user.get('pk'),
                                   follow_name=user.get('username'),
                                   follow_fullname=user.get('full_name'),
                                   pic_follow=user.get('profile_pic_url'))
            yield item


    def fetch_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    def fetch_user(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')