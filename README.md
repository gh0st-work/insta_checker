# insta_checker

**Python Instagram checker / scrapper 2021. Fastly and asynchronously scrapes Instagram profiles and posts, powered by aiohttp.**

My needs for one project included scraping likes, the number of subscribers and so on from Instagram. When I wrote this library, I copied a huge bunch (about 30) of other scrapping libraries in Python or JavaScript. There was one abandoned library, but it died after a month of use. Actually, I wrote my own library, which is this repository.

Working with this library, you are expected:

- Fully works in 2021
- The fastest library for requests - aiohttp
- Fully asynchronous
- Bunch of try except, which, if anything goes wrong, will return the available data
- Adequate informational messages and error messages
- Timeouts
- Typing


# Installation
`pip install insta-checker`

[Here is PyPi](https://pypi.org/project/insta-checker/)

# Work
```python
from insta_checker import InstaChecker, super_print

cookie = 'ds_user_id=48743733271;mid=YQgRZwAAAAEPjPkWIONy9q0lPPdu;sessionid=48743733271%3AJRUhxoYZxBh4BX%3A6;ig_nrcb=1;ig_did=A446BA65-9920-462A-BAA8-F85FEAC0AB98;csrftoken=iD5MZwMnXZHgNzm8H5kACrNHKVBIvpDz;rur="CLN\05448743733271\0541659454776:01f7e7cbc38f962c9fbe9fe015e28ac99145941e231df3769a1682f8ce14b2a8ca254ddf";'
checker = InstaChecker(
    cookie=cookie,
    timeout=1
)

is_cong_ok = checker.check_conf() # if you need
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
print(f"{wrong_success = }") # f string with = is easy format
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

Out:
```python
Conf is ok, making stuff
InstaChecker - Config OK
wrong_success = False
data[some_wrong_url]['errors'] = ['Response status is 404']
profile1_success = True
data[profile1_url]['type'] = 'profile'
profile1_data['id'] = '48335815772'
profile1_data['avatar_url'] = 'https://scontent-muc2-1.cdninstagram.com/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=scontent-muc2-1.cdninstagram.com&_nc_ohc=3gLNeobsvhoAX_K_riR&edm=AL4D0a4BAAAA&ccb=7-4&oh=5ea262b16460f499fdac8bae2dacad42&oe=6111E10F&_nc_sid=712cc3&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'
profile1_data['followers'] = 1
profile1_data['follows'] = 2
profile1_data['media_count'] = 1
profile1_data['recent_media'][0]['text'] = "Photo by Testing on June 26, 2021. May be an image of text that says 'x 6 Game Over × WINNER! Restart game GAMES & TOYS TOOLS'."
post1_success = True
data[post1_url]['type'] = 'post'
post1_data['id'] = '2604671409127216170'
post1_data['likes'] = 1
 id
---- 48335815772
 profile_pic_url
---- https://instagram.ftas1-2.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.ftas1-2.fna.fbcdn.net&_nc_ohc=3gLNeobsvhoAX-d6uuw&edm=AM7KJZYBAAAA&ccb=7-4&oh=381ea8625050ab45526fd94a32cbb00d&oe=6111E10F&_nc_sid=d96ff1&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4
 username
---- antonnechaev990
 media_count
-- 1
 full
-- id
------ 48335815772
-- is_verified
---- False
-- profile_pic_url
------ https://instagram.ftas1-2.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.ftas1-2.fna.fbcdn.net&_nc_ohc=3gLNeobsvhoAX-d6uuw&edm=AM7KJZYBAAAA&ccb=7-4&oh=381ea8625050ab45526fd94a32cbb00d&oe=6111E10F&_nc_sid=d96ff1&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4
-- username
------ antonnechaev990
-- blocked_by_viewer
---- False
-- restricted_by_viewer
---- False
-- followed_by_viewer
---- False
-- full_name
------ Testing
-- has_blocked_viewer
---- False
-- is_private
---- False
-- is_unpublished
---- False
-- requested_by_viewer
---- False
-- pass_tiering_recommendation
---- False
-- edge_owner_to_timeline_media
---- count
------ 1
-- edge_followed_by
---- count
------ 1
```
