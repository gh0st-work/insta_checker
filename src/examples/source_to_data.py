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
