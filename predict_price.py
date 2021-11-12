import pickle

from sklearn.linear_model import LinearRegression

import train_on_dataset


def load_model():
    model = None
    try:
        model = pickle.load(open('model.sav', 'rb'))
    except IOError:
        print('No regression model found')
    return model


def predict_price(model: LinearRegression, types: dict[str: int], regions: dict[str: int]):
    house_type = types.get(input('please enter type of the building: '))
    area = int(input('please enter area of the building: '))
    room = int(input('please enter number of rooms in the building: '))
    region = regions.get(input('please enter region of the building: '))
    if house_type is None:
        house_type = len(types) / 2 + 1
    if region is None:
        region = len(regions) / 2
    return model.predict([[house_type, area, room, region]])


def main():
    types = train_on_dataset.get_types()
    regions = train_on_dataset.get_regions()
    if types is None or regions is None:
        return
    model = load_model()
    print('predicted price: ' + str(predict_price(model, types, regions)[0]) + ' Billion tomans')


if __name__ == '__main__':
    main()
