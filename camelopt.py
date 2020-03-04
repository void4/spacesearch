import requests
import re
import time
from itertools import product
from hyperopt import hp, tpe, fmin, Trials
import numpy as np
from time import time
import json

# Headers for request to server
headers = {
            'authority': 'kamelrechner.eu',
            'method': 'POST',
            'path': '/en/result',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'he,en-US;q=0.9,en;q=0.8,he-IL;q=0.7',
            'cache-control': 'max-age=0',
            'content-length': '93',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': '__cfduid=d6242d07e762c2bbf4dacfea3643648aa1582985884; _ga=GA1.2.1196108495.1582985885; _gid=GA1.2.734670141.1582985885; _gat_gtag_UA_423721_8=1',
            'origin': 'https://kamelrechner.eu',
            'referer': 'https://kamelrechner.eu/en/male',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
}

male_parameters = {
    'age': list(range(14, 71)),
    'height': list(range(140, 221)),
    'haircolor': ['blonde', 'brown', 'black', 'red', 'gray'],
    'hair': ['long', 'middle', 'short',' bald'],
    'eyecolor': ['blue', 'green', 'brown', 'grey'],
    'beard': ['none', 'small', 'middle', 'large'],
    'body': ['muscle', 'normal', 'chubby']
}

female_parameters = {
    'age': list(range(14, 71)),
    'height': list(range(140, 221)),
    'haircolor': ['blonde', 'brown', 'black', 'red', 'gray'],
    'hair': ['long', 'middle', 'short'],
    'eyecolor': ['blue', 'green', 'brown', 'grey'],
    'boobs': ['a', 'b', 'c', 'd'],
    'body': ['thin', 'sporty', 'normal', 'chubby', 'fat']
}

def generate_male_request(age, height, haircolor, hair, eyecolor, beard, body):
    data = f'age={age}&height={height}&haircolor={haircolor}&hair={hair}&eyecolor={eyecolor}&beard={beard}&body={body}&gender=male'
    return requests.post('https://kamelrechner.eu/en/result', headers=headers, data=data, verify=True)

def generate_female_request(age, height, haircolor, hair, eyecolor, boobs, body):
    data = f'age={age}&height={height}&haircolor={haircolor}&hair={hair}&eyecolor={eyecolor}&boobs={boobs}&body={body}&gender=female'
    return requests.post('https://kamelrechner.eu/en/result', headers=headers, data=data, verify=True)

def parse_request(request):
    match = re.search('<span class="result">(\d+)</span>', request.text)
    result = int(match.group(1))
    return result

def generate_perms(options_dict):
    keys, values = zip(*options_dict.items())
    for perm in product(*values):
        yield dict(zip(keys, perm))

parameters = female_parameters

print(len(list(generate_perms(parameters))), "permutations")

male_space = {
    'age': hp.choice('age', list(range(14, 71))),
    'height': hp.choice('height', list(range(140, 221))),
    'haircolor': hp.choice('haircolor', ['blonde', 'brown', 'black', 'red', 'gray']),
    'hair': hp.choice('hair', ['long', 'middle', 'short',' bald']),
    'eyecolor': hp.choice('eyecolor', ['blue', 'green', 'brown', 'grey']),
    'beard': hp.choice('beard', ['none', 'small', 'middle', 'large']),
    'body': hp.choice('body', ['muscle', 'normal', 'chubby'])
}

female_space = {
    'age': hp.choice('age', list(range(14, 71))),
    'height': hp.choice('height', list(range(140, 221))),
    'haircolor': hp.choice('haircolor', ['blonde', 'brown', 'black', 'red', 'gray']),
    'hair': hp.choice('hair', ['long', 'middle', 'short']),
    'eyecolor': hp.choice('eyecolor', ['blue', 'green', 'brown', 'grey']),
    'boobs': hp.choice('boobs', ['a', 'b', 'c', 'd']),
    'body': hp.choice('body', ['thin', 'sporty', 'normal', 'chubby', 'fat'])
}

space = female_space

cache = {} # Cache for downloaded scores

def get_camel_loss(params):
	#hash()
    hashed_params = str(json.dumps(params))
    if hashed_params in cache:
        return cache[hashed_params]

    req = generate_female_request(**params)
    score = parse_request(req)#TODO negate here!
    cache[hashed_params] = score
    return score

bayesian_opt_trials = Trials()

# Optimize using Bayesian optimization
#random.suggest
best_params = fmin(get_camel_loss, space, algo=tpe.suggest,
max_evals=10, trials=bayesian_opt_trials, rstate=np.random.RandomState(2000))

print("Best Results")
print("===================")
print(f"Score is {-bayesian_opt_trials.best_trial['result']['loss']}")
for key, value in best_params.items():
    print(f"{key}: {parameters[key][value]}")



with open("cache-"+str(int(time()*1000)), "w+") as cachefile:
	cachefile.write(json.dumps(cache))
