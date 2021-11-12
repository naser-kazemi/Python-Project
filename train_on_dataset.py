import json
import pickle

import mysql.connector as db_connector
from sklearn.linear_model import LinearRegression



class House:
    count = 0
    houses = []

    def __init__(self, house_type, area, room, region, price):
        self.house_type = house_type
        self.area = area
        self.room = room
        self.region = region
        self.price = price
        House.houses.append(self)
        House.count += 1


def get_data(types, regions):
    try:
        cnx = db_connector.connect(user='root', password='naser2002ka', host='localhost', database='Practice',
                                   connect_timeout=1)
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM house")
        for (house_id, house_type, area, room, region, price) in cursor:
            House(types.get(house_type), int(area), int(room), regions.get(region), float(price))
    except db_connector.Error as err:
        print("Error:", format(err), sep='\n')
        return


def get_types():
    types = None
    try:
        types = json.load(open('house_type.json', 'r'))
    except IOError:
        print('no such file named house_type.json')
    return types


def get_regions():
    regions = None
    try:
        regions = json.load(open('region.json', 'r'))
    except IOError:
        print('no such file named region.json')
    return regions


def train():
    x = list(map(lambda _: [_.house_type, _.area, _.room, _.region], House.houses))
    y = list(map(lambda _: _.price, House.houses))
    model = LinearRegression()
    model = model.fit(x, y)
    return model


def logistic_regression_to_json(model, file=None):
    if file is not None:
        serialize = lambda x: json.dump(x, file)
    else:
        serialize = json.dumps
    data = {'init_params': model.get_params()}
    data['model_params'] = mp = {}
    for p in ('coef_', 'intercept_', 'classes_', 'n_iter_'):
        mp[p] = getattr(model, p).tolist()
    return serialize(data)


def main():
    types = get_types()
    regions = get_regions()
    if types is None or regions is None:
        return
    get_data(types, regions)
    model = train()
    with open("model.sav", "wb") as outfile:
        pickle.dump(model, outfile)


if __name__ == '__main__':
    main()
