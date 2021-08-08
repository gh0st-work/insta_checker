from insta_checker import InstaChecker, super_print
import asyncio


async def main():
    cookie = 'ds_user_id=48743733271;mid=YQgRZwAAAAEPjPkWIONy9q0lPPdu;sessionid=48743733271%3AJRUhxoYZxBh4BX%3A6;ig_nrcb=1;ig_did=A446BA65-9920-462A-BAA8-F85FEAC0AB98;csrftoken=iD5MZwMnXZHgNzm8H5kACrNHKVBIvpDz;rur="CLN\05448743733271\0541659454776:01f7e7cbc38f962c9fbe9fe015e28ac99145941e231df3769a1682f8ce14b2a8ca254ddf";'
    checker = InstaChecker(
        cookie=cookie
    )

    url = 'https://www.instagram.com/antonnechaev990/'

    print(f"{checker.ready = }")
    await checker.check_conf()
    print(f"{checker.ready = }")
    if checker.ready:
        print('Conf is ok, making stuff')
        # stuff

    data = await checker.get_response(url)

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
        print('')
        print('Printing all data:')
        super_print(data)


asyncio.run(main())
