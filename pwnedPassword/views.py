from django.shortcuts import render
import requests
import hashlib


def index(request):
    message = 'Don\'t be shy free to try'
    context = {
        'message': message
    }
    if request.method == 'POST':
        password = request.POST['pass']
        pwnedpassword = [password]
        for password in pwnedpassword:
            count = pwned_api_check(password)
            if count:
                # print(f'{password} was found {count} times... you should probably change your password!')
                message = f'\'{password}\' was found {count} times... you should probably change your password!'
            else:
                # print(f'{password} was NOT found. Carry on!')
                message = f'\'{password}\' was NOT found. Carry on!'
        context = {
            'message': message
        }
    return render(request, 'pwnedpassword.html', context)


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)
