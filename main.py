import json
import requests


def main():
    runs = int(input('specify required number of tests on your endpoint: '))
    if runs < 1:
        # default to 1 in such cases
        load_test(1)
    else:
        load_test(runs)


def validate_json_fields(*args):
    return all(arg is not None for arg in args)


def run(method, endpoint, status_code):
    response = requests.request(method.upper(), endpoint)

    if response.status_code != int(status_code):
        print('somethings off')
    else:
        print('all good!')


def load_test(runs):
    with open('configs/app1/apptest.json', 'r') as file:
        data = json.load(file)

    endpoint = data.get('endpoint')
    method = data.get('method')
    expected_status_code = data.get('expected_status_code')

    if validate_json_fields(endpoint, method, expected_status_code):
        while runs != 0:
            run(method, endpoint, status_code=expected_status_code)
            runs-=1
    else:
        print('field validation failed')


# start the program
main()