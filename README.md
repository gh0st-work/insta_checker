# insta_checker

## **Python Instagram API checker / scrapper / wrapper 2021. Fast and asynchronously scrapes instagram profiles and posts, powered by aiohttp.**

My needs for one project included scraping likes, the number of subscribers and so on from Instagram. When I wrote this library, I've cheked out a huge bunch (about 30) of other scrapping libraries in Python or JavaScript. There was only one abandoned library, but it died after a month of use. Actually, I wrote my own library, which is this repository.

### Working with this library, you are expected:

- Fully works in 2021
- The fastest library for requests - aiohttp
- Fully asynchronous
- Bunch of try except, which, if anything goes wrong, will return the available data
- Adequate informational messages and error messages
- Timeouts
- Typing


# Installation
`pip install insta-checker`

or

`pip install --index-url https://pypi.org/simple/ insta-checker==0.2.2` (please provide latest version)

[Here is PyPi](https://pypi.org/project/insta-checker/)


# Usage
### Create instance of InstaChecker with keywords:
- cookie: Instagram cookie, you must take it after auth, to get requests' statuses ok (str)
- proxy: Proxy, if needed (str) ex: http://user:pass@some.proxy.com
- user_agent: User-Agent header property (str)
- timeout: Sleep after request in seconds (float)
- max_async_requests_count: Maximum count of async requests (int)
- Show debug messages or not (bool)

Example:

```python
checker = InstaChecker(
    cookie='cookie_string',
    proxy='http://user:pass@some.proxy.com',
    user_agent='user_agent_string',
    timeout=1,
    max_async_requests_count=10,
    debug=False
)
```

### To use in default mode run function "run" in InstaChecler isntance with params:
 - urls: List of urls

Example:

```python
urls_list = [
    'https://www.instagram.com/antonnechaev990/'
]
responses = checker.run(urls_list)
for url in urls_list:
    print(responses[url])
```

### To scrape one url run function "get_response" in InstaChecler isntance with params:
 - url: Url to scrape

Example:

```python
url = 'https://www.instagram.com/antonnechaev990/'
task = checker.get_response(url)
data = asyncio.run(task)
url_data = data[url]
```

### To scrape data from source run function "source_to_data" in InstaChecler isntance with params:
 - response_result: Dict like in the example

Example:

```python
source = 'Instagram HTML source string'
response_result = {
    'success': True,
    'data': source,
    'errors': []
}
data = checker.source_to_data(response_result)
data = data['data']
```

# Examples
### run.py
```python
from insta_checker import InstaChecker, super_print
import asyncio

cookie = 'ds_user_id=48743733271;mid=YQgRZwAAAAEPjPkWIONy9q0lPPdu;sessionid=48743733271%3AJRUhxoYZxBh4BX%3A6;ig_nrcb=1;ig_did=A446BA65-9920-462A-BAA8-F85FEAC0AB98;csrftoken=iD5MZwMnXZHgNzm8H5kACrNHKVBIvpDz;rur="CLN\05448743733271\0541659454776:01f7e7cbc38f962c9fbe9fe015e28ac99145941e231df3769a1682f8ce14b2a8ca254ddf";'
checker = InstaChecker(
    cookie=cookie,
    timeout=1,
)

is_cong_ok = asyncio.run(checker.check_conf())  # if you need
if is_cong_ok:
    print('Conf is ok, making stuff')
    # stuff

some_wrong_url = 'https://www.instagram.com/antonnechaev990123123213213132/'
profile1_url = 'https://www.instagram.com/antonnechaev990/'
post1_url = 'https://www.instagram.com/p/CQlptixpNQq/'
urls_to_scrape = [
    some_wrong_url,
    profile1_url,
    post1_url
]
data = checker.run(urls_to_scrape)

"""
    returns
    {
        'your-url': {
            'success': (bool),
            'data': (dict),
            'errors': (dict of strings)
        }
    }
"""

wrong_success = data[some_wrong_url]['success']
print(f"{wrong_success = }")  # f string with = is easy format
if not wrong_success:
    print(f"{data[some_wrong_url]['errors'] = }")

profile1_success = data[profile1_url]['success']
print(f"{profile1_success = }")
if profile1_success:
    profile1_data = data[profile1_url]['data']
    print(f"{data[profile1_url]['type'] = }")
    print(f"{profile1_data['id'] = }")
    print(f"{profile1_data['avatar_url'] = }")
    print(f"{profile1_data['followers'] = }")
    print(f"{profile1_data['follows'] = }")
    print(f"{profile1_data['media_count'] = }")
    print(f"{profile1_data['recent_media'][0]['text'] = }")

post1_success = data[post1_url]['success']
print(f"{post1_success = }")
if post1_success:
    post1_data = data[post1_url]['data']
    print(f"{data[post1_url]['type'] = }")
    print(f"{post1_data['id'] = }")
    print(f"{post1_data['likes'] = }")
    super_print(post1_data['owner'])

```

Output:
```python
InstaChecker - Config OK
InstaChecker - Config OK
wrong_success = False
data[some_wrong_url]['errors'] = ['Response status is 404']
profile1_success = True
data[profile1_url]['type'] = 'profile'
profile1_data['id'] = '48335815772'
profile1_data['avatar_url'] = 'https://scontent-prg1-1.cdninstagram.com/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=scontent-prg1-1.cdninstagram.com&_nc_ohc=3gLNeob
svhoAX_plAkf&edm=ABfd0MgBAAAA&ccb=7-4&oh=90600e50e103e5965c11c95e09984a6c&oe=6111E10F&_nc_sid=7bff83&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'
profile1_data['followers'] = 1
profile1_data['follows'] = 2
profile1_data['media_count'] = 1
profile1_data['recent_media'][0]['text'] = "Photo by Testing on June 26, 2021. May be an image of text that says 'x 6 Game Over × WINNER! Restart game GAMES & TOYS TOOLS'."
post1_success = True
data[post1_url]['type'] = 'post'
post1_data['id'] = '2604671409127216170'
post1_data['likes'] = 1
-- id
---- 48335815772
-- profile_pic_url
---- https://instagram.ftlm1-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.ftlm1-1.fna.fbcdn.net&_nc_ohc=3gLNeobsvhoAX9AC-mS&edm=ALlQn9MBAAA
A&ccb=7-4&oh=1b06c2d085eb2df02df724b681a45906&oe=6111E10F&_nc_sid=48a2a6&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4
-- username
---- antonnechaev990
-- media_count
-- 1
-- full
---- id
------ 48335815772
---- is_verified
---- False
---- profile_pic_url
------ https://instagram.ftlm1-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.ftlm1-1.fna.fbcdn.net&_nc_ohc=3gLNeobsvhoAX9AC-mS&edm=ALlQn9MBA
AAA&ccb=7-4&oh=1b06c2d085eb2df02df724b681a45906&oe=6111E10F&_nc_sid=48a2a6&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4
---- username
------ antonnechaev990
---- blocked_by_viewer
---- False
---- restricted_by_viewer
---- False
---- followed_by_viewer
---- False
---- full_name
------ Testing
---- has_blocked_viewer
---- False
---- is_private
---- False
---- is_unpublished
---- False
---- requested_by_viewer
---- False
---- pass_tiering_recommendation
---- False
---- edge_owner_to_timeline_media
------ count
------ 1
---- edge_followed_by
------ count
------ 1
```

### get_response.py
```python
from insta_checker import InstaChecker, super_print
import asyncio

cookie = 'ds_user_id=48743733271;mid=YQgRZwAAAAEPjPkWIONy9q0lPPdu;sessionid=48743733271%3AJRUhxoYZxBh4BX%3A6;ig_nrcb=1;ig_did=A446BA65-9920-462A-BAA8-F85FEAC0AB98;csrftoken=iD5MZwMnXZHgNzm8H5kACrNHKVBIvpDz;rur="CLN\05448743733271\0541659454776:01f7e7cbc38f962c9fbe9fe015e28ac99145941e231df3769a1682f8ce14b2a8ca254ddf";'
checker = InstaChecker(
    cookie=cookie
)

url = 'https://www.instagram.com/antonnechaev990/'
task = checker.get_response(url)
data = asyncio.run(task)

"""
    returns
    'your-url': {
        'success': (bool),
        'data': (dict),
        'errors': (dict of strings)
    }
"""

data = data[url]
success = data['success']
errors = data['errors']
data = data['data']
print(f"{success = }")
if success:
    print(f"{data['id'] = }")
    print(f"{data['avatar_url'] = }")
    print(f"{data['followers'] = }")
    print(f"{data['follows'] = }")
    print(f"{data['media_count'] = }")
    print(f"{data['recent_media'][0]['text'] = }")

```

Output:
```python
success = True
data['id'] = '48335815772'
data['avatar_url'] = 'https://instagram.fdoh5-2.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fdoh5-2.fna.fbcdn.net&_nc_ohc=3gLNeobsvhoAX9hnS1
N&edm=AId3EpQBAAAA&ccb=7-4&oh=bb06ca18255a19cc24b1540c54299049&oe=6111E10F&_nc_sid=705020&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'
data['followers'] = 1
data['follows'] = 2
data['media_count'] = 1
data['recent_media'][0]['text'] = "Photo by Testing on June 26, 2021. May be an image of text that says 'x 6 Game Over × WINNER! Restart game GAMES & TOYS TOOLS'."
```

### source_to_data.py
```python
import sys
from insta_checker import InstaChecker, super_print
import asyncio
import aiohttp

cookie = 'ds_user_id=48743733271;mid=YQgRZwAAAAEPjPkWIONy9q0lPPdu;sessionid=48743733271%3AJRUhxoYZxBh4BX%3A6;ig_nrcb=1;ig_did=A446BA65-9920-462A-BAA8-F85FEAC0AB98;csrftoken=iD5MZwMnXZHgNzm8H5kACrNHKVBIvpDz;rur="CLN\05448743733271\0541659454776:01f7e7cbc38f962c9fbe9fe015e28ac99145941e231df3769a1682f8ce14b2a8ca254ddf";'
checker = InstaChecker(
    cookie=cookie
)

url = 'https://www.instagram.com/antonnechaev990/'

# You can make it yourself in the way you prefer
async def get_source(url):
    session = aiohttp.ClientSession()
    response_result = {
        'success': False,
        'data': '',
        'errors': [],
    }
    try:
        if checker.proxy and checker.headers:
            response = await session.get(url, proxy=checker.proxy, headers=checker.headers)
        elif checker.proxy:
            response = await session.get(url, proxy=checker.proxy)
        elif checker.headers:
            response = await session.get(url, headers=checker.headers)
        else:
            response = await session.get(url)
        if response.status == 200:
            response_result['success'] = True
            response_result['data'] = await response.text()
        else:
            response_result['success'] = False
            response_result['errors'].append(f'Response status is {int(response.status)}')
        if 'not-logged-in' in response_result['data']:
            response_result['success'] = False
            response_result['errors'].append('Not logged in, provide better headers')
    except BaseException as ex:
        response_result['success'] = True
        response_result['errors'].append(
            f"Can't fetch and parse the page. Error: '{ex}'. On line {sys.exc_info()[-1].tb_lineno}")
    return {url: response_result}


source_response_result = asyncio.run(get_source(url))
data = checker.source_to_data(source_response_result[url])
success = data['success']
errors = data['errors']
data = data['data']
print(f"{success = }")
if success:
    print(f"{data['id'] = }")
    print(f"{data['avatar_url'] = }")
    print(f"{data['followers'] = }")
    print(f"{data['follows'] = }")
    print(f"{data['media_count'] = }")
    print(f"{data['recent_media'][0]['text'] = }")

```

Output:
```python
success = True
data['id'] = '48335815772'
data['avatar_url'] = 'https://scontent-dfw5-1.cdninstagram.com/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=scontent-dfw5-1.cdninstagram.com&_nc_ohc=3gLNeobsvhoAX-Wg
2rP&edm=AL4D0a4BAAAA&ccb=7-4&oh=a1d508e1249422ca6858b6684c23cd5d&oe=6111E10F&_nc_sid=712cc3&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'
data['followers'] = 1
data['follows'] = 2
data['media_count'] = 1
data['recent_media'][0]['text'] = "Photo by Testing on June 26, 2021. May be an image of text that says 'x 6 Game Over × WINNER! Restart game GAMES & TOYS TOOLS'."
```
