#
# calculating the mall for a cell
#

import argparse
import base64
import json
import os
import sys
import zlib
from bp_from_json import blueprint
from bp_from_json import dict_bp
from fractions import Fraction
# from urllib.parse import quote, unquote


productivity = {'iron-gear-wheel': Fraction(1.4),
                'iron-stick': Fraction(1.4),
                'processing-unit': Fraction(1.4),
                'advanced-circuit': Fraction(1.4),
                'electronic-circuit': Fraction(1.4),
                'sulfuric-acid': Fraction(1.3),
                'sulfur': Fraction(1.3),
                'lubricant': Fraction(1.3),
                'copper-cable': Fraction(1.4),
                'plastic-bar': Fraction(1.3),
                'steel-plate': Fraction(1.2),
                'iron-plate': Fraction(1.2),
                'copper-plate': Fraction(1.2),
                'stone-brick': Fraction(1.2),

                'stack-inserter': Fraction(1.0),
                'fast-inserter': Fraction(1.0),
                'inserter': Fraction(1.0),

                'fast-transport-belt': Fraction(1.0),
                'transport-belt': Fraction(1.0),
                'fast-underground-belt': Fraction(1.0),
                'underground-belt': Fraction(1.0),
                'fast-splitter': Fraction(1.0),
                'splitter': Fraction(1.0),

                'steel-chest': Fraction(1.0),

                'assembling-machine-2': Fraction(1.0),
                'assembling-machine-1': Fraction(1.0),

                'speed-module': Fraction(1.0),
                'pipe': Fraction(1.0),

                'engine-unit': Fraction(1.4),
                'electric-engine-unit': Fraction(1.4),

                'concrete': Fraction(1.0)}


nuclear_power_plant_1120MW = {'accumulator': 4,
                              'heat-exchanger': 112,
                              'heat-pipe': 200,
                              'landfill': 4701,
                              'logistic-chest-active-provider': 8,
                              'logistic-chest-requester': 8,
                              'medium-electric-pole': 8,
                              'nuclear-reactor': 8,
                              'offshore-pump': 12,
                              'pipe': 12,
                              'pipe-to-ground': 4,
                              'pump': 10,
                              'radar': 1,
                              'roboport': 2,
                              'solar-panel': 4,
                              'stack-inserter': 16,
                              'steam-turbine': 224,
                              'substation': 22}


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


#############################################
# https://stackoverflow.com/questions/46351275/using-pako-deflate-with-python
#
def pako_inflate_raw(data):
    decompress = zlib.decompressobj(-15)
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    return decompressed_data


def pako_deflate_raw(data):
    compress = zlib.compressobj(
        zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,
        strategy=zlib.Z_DEFAULT_STRATEGY)
    # compressed_data = compress.compress(js_string_to_byte(js_encode_uri_component(data)))
    compressed_data = compress.compress(js_string_to_byte(data))
    compressed_data += compress.flush()
    return compressed_data


def js_encode_uri_component(data):
    return quote(data, safe='~()*!.\'')


def js_decode_uri_component(data):
    return unquote(data)


def js_string_to_byte(data):
    return bytes(data, 'iso-8859-1')


def js_bytes_to_string(data):
    return data.decode('iso-8859-1')


def js_btoa(data):
    return base64.b64encode(data)


def js_atob(data):
    return base64.b64decode(data)


########################################
def input_def(text, default):
    str = input(text + '[' + default + ']:')
    if str:
        return str
    else:
        return default


#############################################
def get_recipes():
    # read json file
    with open('Factorio 1.1 Vanilla.json', 'r') as read_file:
        json_all = json.load(read_file)

    # json -> dist()
    recipes = dict()
    for recipe in json_all['recipes']:
        if len(recipe['products']) == 1:
            for ingredient in recipe['ingredients']:
                ingredient['amount'] = Fraction(ingredient['amount'],
                                                recipe['products'][0]['amount'])
            recipes[recipe['name']] = recipe['ingredients']

    return recipes


#############################################
def get_all_ingredients(ingredient, amount, final_ingredients):
    res = dict_bp()
    debug('recurcive')
    debug('\t', ingredient, amount)
    if isinstance(ingredient, dict):
        if not ingredient['name'] in final_ingredients\
           and ingredient['name'] in recipes:
            res += dict_bp({ingredient['name']: amount * ingredient['amount']})
            if ingredient['name'] in productivity:
                k = productivity[ingredient['name']]
            else:
                k = Fraction(1)
                print("'{}': Fraction(1.0),".format(ingredient['name']))
            for i in recipes[ingredient['name']]:
                res += get_all_ingredients(i,
                                           ingredient['amount'] * amount / k,
                                           final_ingredients)
        else:
            res = dict_bp({ingredient['name']: amount * ingredient['amount']})

    return res


#############################################
def print_dict(d, dimension=None):
    if dimension is None:
        dimension = ''
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        print('{:34} = {:10.3f} {}'.format(k, float(v), dimension))


######################################
#
# main
if __name__ == "__main__":

    # kirkmcdonald.github.io
    # zip -> settings
    # zip=r'lVTbktowDP2bPMUDBNjZ0snHGEcJHnyrbLNsv77Kjdy823ZgmEE6R5KPLhUPvDww+vzItDTlMbuCCiU8HYL3LCA33lkMrDVnlS7dMXtIX17tM5MBtC+FNT5gFEFaw9Bebbjg5e2cK9tIH6SY2zgGqRTgJ/M3UKo17nPFPSALERFa2Om8O+VNNJOlKM6797xWXEO4of3YoF1n46gtMn0vyHzYFfmVh9CmIguDX1E6DaalHPI6+q5Y4CIQZeEkogP01nDF+soqqMF4WMV4gdrndQpt8lAo72QFGNCajgRP6++gIFD2NZQHq0mtq9XX9s2H3WGfR5JfRs3qCIqJXrHiNNnRRlN5pnnDf0sDbaTjOTdRKODYscj0vj/tinMmG2MRSh+AYjnFA+RoxR1Ch8u0raICX/LqwY2AigmJIspw+emPl8PbpnUmbn4WT0j5h450IYvTq0GTEt+QVvKmkIlJTMMcNa+XoC9ln0NdA/EeMlCiTokkdQtjxb8Cj2mgIhySaGAa6iCLZpCc9Ol91pB31Yz0HCXjP52yXj6ACW4Mwb/uXi1pIVBP05QEJbaQahq/5P+UpunVZzUSeHzNl0uXSjPb/3l0SWqwpp3tjxuN8Ri6My/6ebcPjvAkVUnbW5uGOZp2OmkjZ3F15jlWdytVnbIfdBWMb7vbT1zE1zsX2zfY/npRUlm2F+Z/8X9fGScBRd+w5SVJgx0MOs2Mq9ubJPbSt3le801TjLzimCQMh4kWmuZfLZZicCkejbhBmu4d0AH7Zo/ngC82eHa5k+7pjI7P8VHVEcc6+380RlzIajRu7/nAHR2TUmvKukGzkZ1vAZ34aZRH7tz4Bw=='
    # print(js_bytes_to_string(pako_inflate_raw(js_atob(zip))).split('&')[5])

    exchange_str = ''
    parser = argparse.ArgumentParser(
        description="example: python construction_train.py")
    parser.add_argument("-d", "--debug", action="store_true", dest="d",
                        help="debug output on STDERR")
    opt = parser.parse_args()

    exchange_str = input_def('cell BP (string or filename.txt)',
                             'cell500spm.txt')
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    necessary_items_for_construction = bp.get_all_items()
    debug(json.dumps(necessary_items_for_construction,
          indent=4, sort_keys=True))
    if 'speed-module-3' in necessary_items_for_construction:
        necessary_items_for_construction1 = dict_bp()

        print()
        speed_modules_per_minute = Fraction(input_def('How many speed modules are produced per minute?', '49.4'))
        construction_time = necessary_items_for_construction['speed-module-3']/speed_modules_per_minute
        print('Construction time = {:.3f} min.'.format(float(construction_time)))

        power_consumption = Fraction(input_def('What is the power consumption?', '3400'))
        print('Number of power plants: {:10.3f}'.format(float(power_consumption/1120)))
        temp = dict_bp()
        necessary_items_for_construction_nuclear = dict_bp()
        for k, v in nuclear_power_plant_1120MW.items():
            temp += dict_bp({k: float(power_consumption / 1120 * v)})
            new_val = power_consumption / 1120 * v / construction_time
            necessary_items_for_construction_nuclear += dict_bp({k: new_val})
        debug(json.dumps(necessary_items_for_construction + temp,
                         indent=4, sort_keys=True))

        recipes = get_recipes()
        exclusion = ('speed-module-3', 'productivity-module-3')
        for item_name, amount in necessary_items_for_construction.items():
            if item_name not in exclusion:
                necessary_items_for_construction1[item_name] = necessary_items_for_construction[item_name] / construction_time
        necessary_items_for_construction1 += necessary_items_for_construction_nuclear

        print()
        print_dict(necessary_items_for_construction1, '/minute')
        print()

        """
        final_ingredients = ('iron-plate', 'copper-plate', 'steel-plate', 'plastic-bar', 'stone-brick', 'lubricant')
        ingredients = dict_bp()
        for item_name, amount in necessary_items_for_construction1.items():
            if item_name in recipes:
                #print(recipes[item_name])
                #print(item_name)
                for i in recipes[item_name]:
                    #print(i)
                    #ingredients += get_all_ingredients(i, 1, final_ingredients)
                    ingredients += get_all_ingredients(i, amount, final_ingredients)
        print_dict(ingredients)
        """

        # creating a link
        settings = r'data=1-1-19&min=3&belt=express-transport-belt&dm=p3&db=s3&dbc=24&items='
        additional_parameters = r'construction-robot:r:65,logistic-robot:r:65,artillery-shell:r:60,laser-turret:r:45/4,gun-turret:r:225/8,flamethrower-turret:r:45/4,power-armor-mk2:r:1/2,battery-mk2-equipment:r:1,fusion-reactor-equipment:r:1/2,personal-laser-defense-equipment:r:1,personal-roboport-mk2-equipment:r:1/2,spidertron:r:1,exoskeleton-equipment:r:1/2,atomic-bomb:r:21/10,uranium-fuel-cell:r:240,uranium-rounds-magazine:r:135,nuclear-fuel:r:804/25'
        for item_name, performance in necessary_items_for_construction1.items():
            par = '{}:r:{},'.format(item_name, performance)
            settings += par
        settings += additional_parameters

        # print(settings)
        zip = js_bytes_to_string(js_btoa(pako_deflate_raw(settings)))
        link = 'kirkmcdonald.github.io/calc.html#zip={}'.format(zip)
        print(link)
