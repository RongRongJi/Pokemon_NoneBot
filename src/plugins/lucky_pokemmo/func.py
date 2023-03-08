import json
import os


def make_rand_arr():
    with open('src/plugins/lucky_pokemmo/data.json', 'r') as f:
        data = json.load(f)
    return data
