import argparse
import json
try:
    from urllib.parse import urlencode, parse_qsl
except ImportError:  # works for Python 2 and 3
    from urllib import urlencode
    from urlparse import parse_qsl


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('url')
    parser.add_argument('-X', '--request', default=None)
    parser.add_argument('-d', '--data', default=None)
    parser.add_argument('-G', '--get', action='store_true', default=False)
    parser.add_argument('-b', '--cookie', default=None)
    parser.add_argument('-H', '--header', action='append', default=[])
    parser.add_argument('-A', '--user-agent', default=None)
    parser.add_argument('--data-binary', default=None)
    parser.add_argument('--compressed', action='store_true')

    parsed_args = parser.parse_args()

    method = 'get'
    if parsed_args.request:
        method = parsed_args.request

    base_indent = ' ' * 4
    post_data = parsed_args.data or parsed_args.data_binary or ''
    if post_data:
        if not parsed_args.request:
            method = 'post'
        try:
            post_data = json.loads(post_data)
        except ValueError:
            try:
                post_data = dict(parse_qsl(post_data))
            except:
                pass

    cookies_dict = {}

    if parsed_args.cookie:
        cookies = parsed_args.cookie.split(';')
        for cookie in cookies:
            key, value = cookie.strip().split('=')
            cookies_dict[key] = value

    data_arg = 'data'
    headers_dict = {}
    for header in parsed_args.header:
        key, value = header.split(':', 1)
        if key.lower().strip() == 'content-type' and value.lower().strip() == 'application/json':
            data_arg = 'json'

        if key.lower() == 'cookie':
            cookies = value.split(';')
            for cookie in cookies:
                key, value = cookie.strip().split('=')
                cookies_dict[key] = value
        else:
            headers_dict[key] = value.strip()
    if parsed_args.user_agent:
        headers_dict['User-Agent'] = parsed_args.user_agent

    qs = ''
    if parsed_args.get:
        method = 'get'
        try:
            qs = '?{}'.format(urlencode(post_data))
        except:
            qs = '?{}'.format(str(post_data))
        print(post_data)
        post_data = {}

    result = """requests.{method}('{url}{qs}',{data}\n{headers},\n{cookies},\n)""".format(
        method=method.lower(),
        url=parsed_args.url,
        qs=qs,
        data='\n{}{}={},'.format(base_indent, data_arg, post_data) if post_data else '',
        headers='{}headers={}'.format(base_indent, headers_dict),
        cookies='{}cookies={}'.format(base_indent, cookies_dict),
    )
    print(result)
