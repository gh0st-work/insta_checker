import asyncio
import json
import sys
from typing import Union, Dict, List

import aiohttp


def super_print(data, left: int = 0):
    """

    Debug stuff, prints data beautifully

    :param data: data to print
    :param left: offset left (int)
    :return: nothing, just prints

    """
    if isinstance(data, list):
        for item in data:
            try:
                super_print(item, left + 1)
            except:
                print('--' * (left + 1) + f' {data}')
    elif isinstance(data, dict):
        for k, v in data.items():
            print('--' * left + f' {k}')
            try:
                super_print(v, left + 1)
            except:
                print('--' * (left + 1) + f' {v}')
    else:
        print('--' * (left + 1) + ' ' + data)


class InstaChecker:

    def __init__(
            self,
            cookie: Union[str, None] = None,
            proxy: Union[str, None] = None,
            user_agent: Union[str, None] = None,
            timeout: float = 1,
            debug: bool = False
    ):

        """

        Initialize InstaChecker

        :param cookie: Instagram cookie, you must take it after auth, to get requests' statuses ok (str)
        :param proxy: Proxy, if needed (str) ex: http://user:pass@some.proxy.com
        :param user_agent: User-Agent header property (str)
        :param timeout: Sleep after request in seconds (float)
        :param debug: Show debug messages or not (bool)

        """

        self.ready = True
        self.debug = debug
        self.proxy = proxy
        self.timeout = timeout

        self.user_agent = user_agent
        if self.user_agent is None:
            self.user_agent = ''

        self.cookie = cookie
        if self.cookie is None:
            self.cookie = ''
            print('InstaChecker - No cookie provided')
            self.ready = False

        if len(self.timeout) < 1:
            print(f"InstaChecker - WARNING, your timeout ({self.timeout}) is less then 1 secound, it can be dangerous for your cookies")

        self.headers = {
            'cookie': self.cookie,
            'user-agent': self.user_agent,
            'User-Agent': self.user_agent
        }

    async def check_conf(self):

        """

        Checking provided cookie + user-agent + proxy configuration

        :return: Nothing, just changes ready param of instance

        """

        session = aiohttp.ClientSession()
        url = 'https://www.instagram.com/antonnechaev990/'
        response = await self.get_response(url, session)
        self.ready = response['success']
        await session.close()
        if self.ready:
            print(f"InstaChecker - Config OK")
        else:
            print(f"InstaChecker - Config FAIL, errors: {','.join(response['errors'])}")

    def run(
            self,
            urls: Union[List[str], None] = None,
            check: bool = True
    ) -> Union[list, str]:

        """

        Runs tasks

        :param urls: Urls to get data from (list of strings)
        :param check: To check provided cookie + user-agent + proxy configuration or not (bool)
        :return: Dictionary of results or error (dict or str)

        """

        if urls is None:
            urls = []
        if check:
            asyncio.run(self.check_conf())
        if self.ready:
            responses = asyncio.run(self.get_responses(urls))
            return responses
        else:
            print('InstaChecker - not ready, config FAILed')
            return 'Not ready'

    def deserialize_user(
            self,
            user: dict
    ) -> dict:

        """

        Translates raw user page dict to pretty info dict

        :param user: Raw dict from user page
        :return: Prettified info

        """
        result = {
            'full': user
        }
        try:
            result = {
                'id': user['id'],
                'username': user['username'],
                'connected_fb_page': user['connected_fb_page'],
                'media_count': user['edge_owner_to_timeline_media']['count'],
                'biography': user['biography'],
                'followers': user['edge_followed_by']['count'],
                'follows': user['edge_follow']['count'],
                'full_name': user['full_name'],
                'avatar_url': user['profile_pic_url'],
                'avatar_url_hd': user['profile_pic_url_hd'],
            }
            recent_media = []
            for media_node in user['edge_owner_to_timeline_media']['edges']:
                media = media_node['node']
                recent_media.append(self.deserialize_media(media, full=False))
                recent_media.append({
                    'type': media['__typename'].replace('Graph', '').lower(),
                    'id': media['id'],
                    'shortcode': media['shortcode'],
                    'post_url': f"https://www.instagram.com/p/{media['shortcode']}/",
                    'src': media['display_url'],
                    'dimesions': media['dimensions'],
                    'thumbnail_src': media['thumbnail_src'],
                    'thumbnails': media['thumbnail_resources'],
                    'owner': media['owner'],
                    'is_video': media['is_video'],
                    'text': media['accessibility_caption'],
                    'comments': media['edge_media_to_comment']['count'],
                    'comments_disabled': media['comments_disabled'],
                    'likes': media['edge_liked_by']['count'],
                    'location': media['location'],
                    'timestamp': media['taken_at_timestamp'],
                    'full': media
                })
            result['recent_media'] = recent_media
        except BaseException as ex:
            result['errors'] = [f'User deserialization error at line {sys.exc_info()[-1].tb_lineno}. Maybe instagram changed  API, have returned only full']
        return result

    def deserialize_media(
            self,
            media: dict,
            full: bool = True
    ) -> dict:

        """

        Translates raw media page dict to pretty info dict

        :param media: Raw dict from media page
        :param full: Was the dict got directly from the page or not (bool)
        :return: Prettified info

        """
        result = {
            'full': media
        }
        try:
            if full:
                result = {
                    'type': media['__typename'].replace('Graph', '').lower(),
                    'id': media['id'],
                    'shortcode': media['shortcode'],
                    'post_url': f"https://www.instagram.com/p/{media['shortcode']}/",
                    'dimesions': media['dimensions'],
                    'src': media['display_url'],
                    'srcs': media['display_resources'],
                    'is_video': media['is_video'],
                    'text': media['accessibility_caption'],
                    'comments_disabled': media['comments_disabled'],
                    'likes': media['edge_media_preview_like']['count'],
                    'owner': {
                        'id': media['owner']['id'],
                        'profile_pic_url': media['owner']['profile_pic_url'],
                        'username': media['owner']['username'],
                        'media_count': media['owner']['edge_owner_to_timeline_media']['count'],
                        'full': media['owner']
                    },
                    'location': media['location'],
                    'timestamp': media['taken_at_timestamp']
                }
            else:
                result = {
                    'type': media['__typename'].replace('Graph', '').lower(),
                    'id': media['id'],
                    'shortcode': media['shortcode'],
                    'post_url': f"https://www.instagram.com/p/{media['shortcode']}/",
                    'src': media['display_url'],
                    'dimesions': media['dimensions'],
                    'thumbnail_src': media['thumbnail_src'],
                    'thumbnails': media['thumbnail_resources'],
                    'is_video': media['is_video'],
                    'text': media['accessibility_caption'],
                    'comments': media['edge_media_to_comment']['count'],
                    'comments_disabled': media['comments_disabled'],
                    'likes': media['edge_liked_by']['count'],
                    'owner': media['owner'],
                    'location': media['location'],
                    'timestamp': media['taken_at_timestamp']
                }
        except BaseException as ex:
            result['errors'] = [f'Media deserialization error at line {sys.exc_info()[-1].tb_lineno}. Maybe instagram changed  API, returned only full']
        return result

    def source_to_profile(
            self,
            response_result: dict
    ) -> Dict[str, Union[bool, str, List[str]]]:

        """

        Translate intagram profile HTML source to result data

        :param response_result: HTML source str
        :return: Parsed json dict

        """

        try:
            response_result['type'] = 'profile'
            shared_data_str = response_result['data']
            shared_data_str = shared_data_str.split('window._sharedData = ')[-1]
            shared_data_str = shared_data_str.split(';')[0]
            shared_data = json.loads(shared_data_str)
            response_result['data'] = shared_data
            if 'entry_data' in response_result['data'].keys():
                response_result['data'] = response_result['data']['entry_data']
                if 'ProfilePage' in response_result['data'].keys():
                    if len(response_result['data']['ProfilePage']):
                        response_result['data'] = response_result['data']['ProfilePage'][0]
                        if 'graphql' in response_result['data'].keys():
                            response_result['data'] = response_result['data']['graphql']
                            if 'user' in response_result['data'].keys():
                                if self.debug:
                                    super_print(response_result['data'])
                                response_result['data'] = response_result['data']['user']
                                response_result['data'] = self.deserialize_user(response_result['data'])
                            else:
                                response_result['success'] = False
                                response_result['errors'].append(
                                    f'No user in response body --> window.sharedData --> entry_data --> ProfilePage --> 0 --> graphql')
                        else:
                            response_result['success'] = False
                            response_result['errors'].append(
                                f'No graphql in response body --> window.sharedData --> entry_data --> ProfilePage --> 0')
                    else:
                        response_result['success'] = False
                        response_result['errors'].append(
                            f'ProfilePage is blank in response body --> window.sharedData --> entry_data')
                else:
                    response_result['success'] = False
                    response_result['errors'].append(
                        f'No ProfilePage in response body --> window.sharedData --> entry_data')
            else:
                response_result['success'] = False
                response_result['errors'].append(f'No entry_data in response body --> window.sharedData')
        except BaseException as ex:
            response_result['success'] = False
            response_result['errors'] = f"Can't fetch and parse the source of page. Error: '{ex}'. On line {sys.exc_info()[-1].tb_lineno}"

        return response_result

    def source_to_media(
            self,
            response_result: dict
    ) -> Dict[str, Union[bool, str, List[str]]]:

        """

        Translate intagram media HTML source to result data

        :param response_result: HTML source str
        :return: Parsed json dict

        """

        try:
            response_result['type'] = 'post'
            additional_data_str = response_result['data']
            additional_data_str = additional_data_str.split("window.__additionalDataLoaded('")[-1]
            additional_data_str = additional_data_str.split("/',")[1]
            additional_data_str = additional_data_str.split(');')[0]
            additional_data = json.loads(additional_data_str)
            response_result['data'] = additional_data
            if 'graphql' in response_result['data'].keys():
                response_result['data'] = additional_data['graphql']
                if 'shortcode_media' in response_result['data'].keys():
                    response_result['data'] = response_result['data']['shortcode_media']
                    if self.debug:
                        super_print(response_result['data'])
                    response_result['data'] = self.deserialize_media(response_result['data'], full=True)
                else:
                    response_result['success'] = False
                    response_result['errors'].append(f"No shortcode_media in response body --> window.__additionalDataLoaded --> graphql")
            else:
                response_result['success'] = False
                response_result['errors'].append(f"No graphql in response body --> window.__additionalDataLoaded")
        except BaseException as ex:
            response_result['success'] = False
            response_result['errors'] = f"Can't fetch and parse the source of page. Error: '{ex}'. On line {sys.exc_info()[-1].tb_lineno}"
        return response_result

    async def get_response(
            self,
            url: str,
            session: aiohttp.ClientSession
    ) -> Dict[str, Dict[str, Union[bool, str, List[str]]]]:

        """

        Fetches and parses the url

        :param url: Url to fetch
        :param session: aiohttp.ClientSession instance
        :return: Dict of fetch and parse result, ex: {'https://some-url.com': {'success': False, 'data': 'raw_html_data', 'errors': ['some_error']}}

        """

        response_result = {
            'success': False,
            'data': '',
            'errors': [],
        }
        try:
            if self.proxy and self.headers:
                response = await session.get(url, proxy=self.proxy, headers=self.headers)
            elif self.proxy:
                response = await session.get(url, proxy=self.proxy)
            elif self.headers:
                response = await session.get(url, headers=self.headers)
            else:
                response = await session.get(url)
            if response.status == 200:
                response_result['success'] = True
                response_result['data'] = await response.text()
                if "window.__additionalDataLoaded('" in response_result['data']:
                    response_result = self.source_to_media(response_result)
                elif 'window._sharedData = {' in response_result['data']:
                    response_result = self.source_to_profile(response_result)
                else:
                    response_result['success'] = False
                    response_result['errors'].append(f'No any window.(data) in response body')
            else:
                response_result['success'] = False
                text = await response.text()
                print(text)
                response_result['errors'].append(f'Response status is {int(response.status)}')
            if 'not-logged-in' in response_result['data']:
                response_result['success'] = False
                response_result['errors'].append('Not logged in, provide better headers')
        except BaseException as ex:
            response_result['success'] = True
            response_result['errors'].append(f"Can't fetch and parse the page. Error: '{ex}'. On line {sys.exc_info()[-1].tb_lineno}")
        await asyncio.sleep(self.timeout)
        return response_result

    async def get_responses(
            self,
            urls: List[str]
    ) -> Dict[str, Dict[str, Union[bool, str, List[str]]]]:

        """

        Asynchronously fetches and pareses the urls

        :param urls: List of urls to fetch (list of strings)
        :return: Dict of results (dict)

        """

        urls = list(set(urls))
        if len(urls) > 10:
            print("InstaChecker - WARNING, you're trying to fetch more then 10 urls, it can be dangerous for your cookies")
        session = aiohttp.ClientSession()
        async_tasks = {self.get_response(url, session) for url in urls}
        responses = await asyncio.gather(*async_tasks)
        responses_dict = {urls[i]: response for i, response in enumerate(responses)}
        await session.close()
        if self.debug:
            super_print(responses_dict)
        return responses_dict
