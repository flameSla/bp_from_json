import base64
import collections
import json
import zlib
import hashlib
import math


#############################################
class position():
    def __init__(self, obj):
        self.data = obj

    @classmethod
    def new_position(cls, x, y):
        return cls({'x': x, 'y': y})

    @classmethod
    def from_dict(cls, d):
        return cls(d)

    def __packing_numbers(self, a):
        """ 100.0 -> 100(int) """
        """ 100.1 -> 100.1    """
        fractional, integer = math.modf(a)
        if fractional == 0:
            return int(integer)
        else:
            return a

    def __packing_pos(self):
        """ 100.0 -> 100(int) """
        """ 100.1 -> 100.1    """
        self.data['x'] = self.__packing_numbers(self.data['x'])
        self.data['y'] = self.__packing_numbers(self.data['y'])

    def __iadd__(self, other):
        self.data['x'] += other.data['x']
        self.data['y'] += other.data['y']
        self.__packing_pos()
        return self

    def __isub__(self, other):
        self.data['x'] -= other.data['x']
        self.data['y'] -= other.data['y']
        self.__packing_pos()
        return self

    def rotate(self, cent_x, cent_y, angle_degrees):
        cent = position.new_position(cent_x, cent_y)
        self -= cent

        angle_radians = angle_degrees * math.pi / 180.0
        x = self.data['x']*math.cos(angle_radians) - \
            self.data['y']*math.sin(angle_radians)
        y = self.data['x']*math.sin(angle_radians) + \
            self.data['y']*math.cos(angle_radians)

        self.data['x'] = x
        self.data['x'] = y
        self += cent
        self.__packing_pos()

    def __str__(self):
        return "{{'x': {0}, 'y': {1}}}".format(self.data['x'],
                                               self.data['y'])

    def read_x(self):
        return self.data['x']

    def read_y(self):
        return self.data['y']


#############################################
class entity():
    def __init__(self, obj):
        self.data = obj

    @classmethod
    def new_entity(cls, name, pos_x, pos_y,
                   direction=None, orientation=None):
        entity = dict()
        entity['entity_number'] = 0
        entity['name'] = name
        entity['position'] = position.new_position(pos_x, pos_y).data
        if direction is not None:
            entity['direction'] = direction
        if orientation is not None:
            entity['orientation'] = orientation
        return cls(entity)

    def update_items(self, item, name_verification=True):
        entity_may_contain_items = (
            'artillery-turret',
            'artillery-wagon',
            'assembling-machine-1',
            'assembling-machine-2',
            'assembling-machine-3',
            'beacon',
            'boiler',
            'burner-inserter',
            'burner-mining-drill',
            'cargo-wagon',
            'centrifuge',
            'chemical-plant',
            'electric-furnace',
            'electric-mining-drill',
            'gun-turret',
            'iron-chest',
            'lab',
            'locomotive',
            'nuclear-reactor',
            'oil-refinery',
            'pumpjack',
            'roboport',
            'rocket-silo',
            'steel-chest',
            'steel-furnace',
            'stone-furnace',
            'wooden-chest')

        if self.data['name'] in entity_may_contain_items or\
           name_verification is False:
            if 'items' in self.data:
                self.data['items'].update(item)
            else:
                self.data['items'] = item
        else:
            print(f"Warning! '{self.data['name']}' cannot contain items")

    def set_inventory_filter(self, filtr):
        if 'inventory' not in self.data:
            self.data['inventory'] = dict()

        if 'filters' not in self.data['inventory']:
            self.data['inventory']['filters'] = list()

        self.data['inventory']['filters'].append(filtr)

    def read_name(self):
        return self.data['name']

    def read_entity_number(self):
        return self.data['entity_number']

    def set_entity_number(self, val):
        self.data['entity_number'] = val

    def set_station(self, val):
        self.data['station'] = val

    def read_items(self):
        return self.data.get('items', dict())

    def read_recipe(self):
        return self.data.get('recipe', None)

    def __eq__(self, other):
        a = self.data.copy()
        b = other.data.copy()
        a['entity_number'] = 0
        b['entity_number'] = 0
        return a == b

    def get_pos(self):
        return position(self.data['position'])


#############################################
def print_id(s, a):
    print(s, '\t', id(a), '\t', a, '\t', type(a))


#############################################
def get_items():
    # read json file
    with open('items.json', 'r') as read_file:
        json_items = json.load(read_file)

    # json -> dist()
    items = dict_bp()
    for i in json_items['items']:
        items[i['name']] = float(i['stack'])  # items["wooden-chest"] = 50.0

    return items


#############################################
class dict_bp(dict):
    def __add__(self, other):
        temp = dict_bp(self)
        for key, value in other.items():
            if key in temp:
                temp[key] += value
            else:
                temp[key] = value
        return temp

    def __iadd__(self, other):
        for key, value in other.items():
            if key in self:
                self[key] += value
            else:
                self[key] = value
        return self

    def __str__(self):
        s = str()
        for k, v in self.items():
            s += '"{}" = {}\n'.format(k, v)
        return s


#############################################
class blueprint:
    def __init__(self, data):
        self.data = data
        if 'blueprint_book' in self.data:
            self.obj = self.data['blueprint_book']
        elif 'blueprint' in self.data:
            self.obj = self.data['blueprint']
        else:
            self.data = None
            self.obj = None

    @classmethod
    def new_blueprint(cls):
        bp_json = collections.OrderedDict()
        bp_json['blueprint'] = collections.OrderedDict()
        # bp_json['blueprint']['description'] = str()
        # bp_json['blueprint']['icons'] = list()
        # [{'signal': {'type': 'virtual', 'name': 'signal-a'}, 'index': 1}]
        bp_json['blueprint']['entities'] = list()
        # bp_json['blueprint']['tiles'] = list()
        # bp_json['blueprint']['schedules'] = list()
        bp_json['blueprint']['item'] = 'blueprint'
        # bp_json['blueprint']['label'] = str()
        # bp_json['blueprint']['label_color']
        bp_json['blueprint']['version'] = 281479275937792

        return cls(bp_json)

    @classmethod
    def from_string(cls, str):
        version_byte = str[0]
        if version_byte == '0':
            json_str = zlib.decompress(base64.b64decode(str[1:]))
            bp_json = json.loads(json_str,
                                 object_pairs_hook=collections.OrderedDict)
        else:
            print('Warning! The version byte is currently 0 '
                  '(for all Factorio versions through 1.1)')
            print('Warning! Unsupported version: {0}'.format(version_byte))
            bp_json = None

        return cls(bp_json)

    @classmethod
    def from_file(cls, filename):
        exchange_str = ''
        with open(filename, 'r') as f:
            exchange_str = f.read()

        return cls.from_string(exchange_str)

    def to_str(self):
        json_str = json.dumps(self.data,
                              separators=(",", ":"),
                              ensure_ascii=False).encode("utf8")
        exchange_str = '0' + base64.b64encode(zlib.compress(json_str,
                                                            9)).decode('utf-8')
        return exchange_str

    def __get_all_items_parse(self, bp, items):
        if bp.is_blueprint_book():
            for b in bp.read_blueprints():
                self.__get_all_items_parse(blueprint(b), items)
        elif bp.is_blueprint():
            for entity in bp.get_entities():
                if entity.read_name() == 'curved-rail':
                    items += {"rail": 4}
                elif entity.read_name() == 'straight-rail':
                    items += {"rail": 1}
                else:
                    items += {entity.read_name(): 1}
                items += entity.read_items()

    def get_all_items(self):
        items = dict_bp()
        self.__get_all_items_parse(self, items)
        return items

    def __get_all_tiles_parse(self, bp, tiles):
        if bp.is_blueprint_book():
            for b in bp.read_blueprints():
                self.__get_all_tiles_parse(blueprint(b), tiles)
        elif bp.is_blueprint():
            for t in bp.read_tiles():
                tiles += {t['name']: 1}

    def get_all_tiles(self):
        tiles = dict_bp()
        self.__get_all_tiles_parse(self, tiles)
        return tiles

    def __get_all_bp_parse(self, bp, bps, current_directory):
        if bp.is_blueprint_book():
            md5 = bp.get_md5()
            current_directory += md5 + '\\'
            bps.append([bp, md5, current_directory])
            for b in bp.read_blueprints():
                self.__get_all_bp_parse(blueprint(b), bps, current_directory)
        elif bp.is_blueprint():
            md5 = bp.get_md5()
            bps.append([bp, md5, current_directory])

    def get_all_bp(self,
                   onedimensional=False,
                   blueprint_only=False):
        bps = list()
        self.__get_all_bp_parse(self, bps, '')

        if onedimensional is False:
            return bps
        elif onedimensional is True:
            temp = list()
            for a in bps:
                if blueprint_only is False:
                    temp.append(a[0])
                else:
                    if a[0].is_blueprint():
                        temp.append(a[0])
            return temp
        else:
            return list()

    def is_blueprint_book(self):
        if self.data is not None:
            return 'blueprint_book' in self.data

    def is_blueprint(self):
        if self.data is not None:
            return 'blueprint' in self.data

    def read_blueprints(self):
        return self.obj.get('blueprints', list())

    def append_entity(self, e):
        e.set_entity_number(len(self.obj['entities']) + 1)
        self.obj['entities'].append(e.data)

    def get_entities(self):
        return list(map(lambda x: entity(x), self.obj['entities']))

    def print_entities(self):
        for e in self.get_entities():
            print(e.data)
            # print(e.get_pos(), " ", e.data)

    def normalize_entities(self):
        # position -= pos_min
        x = list()
        y = list()
        entities = self.get_entities()
        for e in entities:
            x.append(e.get_pos().read_x())
            y.append(e.get_pos().read_y())

        pmin = position.new_position(min(x), min(y))
        for e in entities:
            e.get_pos().__isub__(pmin)
        return pmin

    def denormalization_entities(self, p):
        for e in self.get_entities():
            e.get_pos().__iadd__(p)
        pass

    def read_tiles(self):
        return self.obj.get('tiles', list())

    def read_label(self):
        return self.obj.get('label', 'untitled')

    def set_label(self, str):
        self.obj['label'] = str

    def read_description(self):
        return self.obj.get('description', 'description is missing')

    def set_description(self, str):
        self.obj['description'] = str

    def read_label_color(self):
        return self.obj.get('label_color', None)

    def set_label_color(self, r, g, b):
        self.obj['label_color'] = {"r": r, "g": g, "b": b}

    def read_icons(self):
        return self.obj.get('icons', None)

    def read_schedules(self):
        return self.obj.get('schedules', list())

    def read_version(self):
        return self.obj.get('version', '')

    def set_icons(self, index, icon_type, name):
        new_icon = {'signal': {'type': icon_type, 'name': name},
                    'index': index}
        if index >= 1 and index <= 4:
            if 'icons' in self.obj:
                if index in [icon['index'] for icon in self.obj['icons']]:
                    for i in range(len(self.obj['icons'])):
                        if self.obj['icons'][i]['index'] == index:
                            self.obj['icons'][i] = new_icon
                            break
                else:
                    self.obj['icons'].append(new_icon)
            else:
                self.obj['icons'] = [new_icon]

    def read_item(self):
        return self.obj['item']

    def __md5(self, data):
        return hashlib.md5(json.dumps(data,
                           sort_keys=True).encode('utf-8')).hexdigest()

    def get_md5(self):
        return self.__md5(self.data)

    def __compare_entities(self, bp, debug):
        e1 = sorted(self.get_entities(),
                    key=lambda a: (a.data['position']['x'],
                                   a.data['position']['y']))
        e2 = sorted(bp.get_entities(),
                    key=lambda a: (a.data['position']['x'],
                                   a.data['position']['y']))
        if e1 == e2:
            return True
        else:
            '''
            print("len1={} len2={}".format(len(e1), len(e2)))
            for i in range(len(e1)):
                print(f"{i} ", e1[i].data)
                print(f"{i} ", e2[i].data)
            '''
            return False

    def __compare_bp_bp(self, bp, debug):
        result = dict()
        if debug:
            print("blueprint vs bplueprint")
        result['md5'] = self.get_md5() == bp.get_md5()
        if result['md5'] and debug:
            print('md5 are equal')
        result['label'] = self.read_label() == bp.read_label()
        if result['label'] and debug:
            print('label are equal')
        result['label_color'] = \
            self.read_label_color() == bp.read_label_color()
        if result['label_color'] and debug:
            print('label_color are equal')
        result['description'] = \
            self.read_description() == bp.read_description()
        if result['description'] and debug:
            print('description are equal')
        pmin_self = self.normalize_entities()
        pmin_bp = bp.normalize_entities()
        result['entities'] = self.__compare_entities(bp, debug)
        if result['entities'] and debug:
            print('entities are equal')
        self.denormalization_entities(pmin_self)
        bp.denormalization_entities(pmin_bp)
        result['tiles'] = self.read_tiles() == bp.read_tiles()
        if result['tiles'] and debug:
            print('tiles are equal')
        result['icons'] = self.read_icons() == bp.read_icons()
        if result['icons'] and debug:
            print('icons are equal')
        result['schedules'] = self.read_schedules() == bp.read_schedules()
        if result['schedules'] and debug:
            print('schedules are equal')
        result['version'] = self.read_version() == bp.read_version()
        if result['version'] and debug:
            print('version are equal')
        return [self.get_md5(), bp.get_md5(), result]

    def __compare_bp_book(self, bp, debug):
        result = list()
        if debug:
            print("blueprint vs book")
        for b in bp.get_all_bp(onedimensional=True, blueprint_only=True):
            result.append(self.__compare_bp_bp(b, debug))
        return result

    def compare(self, bp, debug=False):
        if self.is_blueprint() and bp.is_blueprint():
            return self.__compare_bp_bp(bp, debug)
        elif self.is_blueprint_book() and bp.is_blueprint_book():
            return {}
        else:
            if self.is_blueprint():
                return self.__compare_bp_book(bp, debug)
            else:
                return bp.__compare_bp_book(self, debug)
