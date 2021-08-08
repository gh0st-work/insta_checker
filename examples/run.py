from insta_checker import InstaChecker, super_print
import asyncio


async def main():
    cookie = 'ds_user_id=48743733271;mid=YQgRZwAAAAEPjPkWIONy9q0lPPdu;sessionid=48743733271%3AJRUhxoYZxBh4BX%3A6;ig_nrcb=1;ig_did=A446BA65-9920-462A-BAA8-F85FEAC0AB98;csrftoken=iD5MZwMnXZHgNzm8H5kACrNHKVBIvpDz;rur="CLN\05448743733271\0541659454776:01f7e7cbc38f962c9fbe9fe015e28ac99145941e231df3769a1682f8ce14b2a8ca254ddf";'
    checker = InstaChecker(
        cookie=cookie,
        timeout=1,
    )

    some_wrong_url = 'https://www.instagram.com/antonnechaev990123123213213132/'
    profile1_url = 'https://www.instagram.com/antonnechaev990/'
    post1_url = 'https://www.instagram.com/p/CQlptixpNQq/'
    urls_to_scrape = [
        some_wrong_url,
        profile1_url,
        post1_url
    ]
    data = await checker.run(urls_to_scrape)

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
        print(data[profile1_url])
        profile1_data = data[profile1_url]['data']
        print(f"{data[profile1_url]['type'] = }")
        print(f"{profile1_data['id'] = }")
        print(f"{profile1_data['avatar_url'] = }")
        print(f"{profile1_data['followers'] = }")
        print(f"{profile1_data['follows'] = }")
        print(f"{profile1_data['media_count'] = }")
        print(f"{profile1_data['recent_media'][0]['text'] = }")
        print('')
        print('Printing all profile1 data:')
        super_print(profile1_data)

    post1_success = data[post1_url]['success']
    print(f"{post1_success = }")
    if post1_success:
        post1_data = data[post1_url]['data']
        print(f"{data[post1_url]['type'] = }")
        print(f"{post1_data['id'] = }")
        print(f"{post1_data['likes'] = }")
        super_print(post1_data['owner'])
        print('')
        print('Printing all post1 data:')
        super_print(post1_data)


asyncio.run(main())
