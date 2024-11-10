import pandas as pd
from haversine import haversine

def getDistance(latitude_longtitude_1, latitude_longtitude_2):
    '''https://mizykk.tistory.com/21
       latitude, longigude 두개 넣으면 거리 계산해주는'''
    return haversine(latitude_longtitude_1, latitude_longtitude_2, unit='m')

def getCoordinatesFromData(dataframe):
    '''데이터프레임에서 좌표만 뽑아서 (lat,longitude)들의 리스트를 만들어주는
    dataframe_original의 구조는 (latitude, longitutde, city_name)'''
    coordinates = []
    row_len = len(dataframe)
    for row in range(row_len):
        latitude = dataframe.iloc[row,0]
        longitude = dataframe.iloc[row,1]
        coordinates.append((latitude, longitude))
    return coordinates

def isThereLessThanConst(list, const):
    for distance in list:
        if distance < const:
            return True
    return False

def distancesOfNearestCoordinate(coordinates):
    '''좌표들의 리스트에서 가장 가까운 곳을 추출해주는'''
    distance_of_minimums = []
    for index in range(len(coordinates)):
        '''리스트의 인덱스는 0부터 시작하는 것 주의'''
        target = coordinates[index]
        distances_from_target = []

        for one_coordinate in coordinates:
            distances_from_target.append(getDistance(target, one_coordinate))

        # 지들끼리 몰켜있는 경우가 많아서 데이터가 과소추정된다!
        while isThereLessThanConst(distances_from_target, ):
            distances_from_target.remove(min(distances_from_target))

        distance_of_minimums.append(min(distances_from_target))
    return distance_of_minimums

def lib():
    df = pd.read_csv('./raw_data/library_data.csv', usecols=['LBRRY_LA','LBRRY_LO','LBRRY_NM', 'LBRRY_ADDR', 'ONE_AREA_NM'])
    df = df[df['ONE_AREA_NM']=="부산광역시"]
    df=df.sort_values('LBRRY_ADDR')
    df['minimum_library'] = "none"
    df['distance'] = 0
    df = df.dropna(axis=0)

    print(df)

    for row in range(len(df)):
        target_latitude = df.iloc[row,2]
        target_longitude = df.iloc[row,3]
        distances_name = {}
        for one_row in range(len(df)):
            cor1 = [target_latitude, target_longitude]
            cor2 = [df.iloc[one_row,2], df.iloc[one_row,3]]
            dist = getDistance(cor1, cor2)
            distances_name[dist] = df.iloc[one_row,0]
        distance = list(distances_name.keys())
        distance.remove(min(distance))
        #distance.remove(min(distance))
        #distance.remove(min(distance))
        minimum_distance = min(distance)
        name = distances_name[minimum_distance]
        df.iloc[row,5]=name
        df.iloc[row,6]=minimum_distance
    #df.head()

    #df=df.sort_values('distance')
    df = df[['LBRRY_NM', 'minimum_library', 'distance']]
    df=df.sort_values('distance')
    print()
    print(df['distance'].mean())
    
    df.to_csv('test3.csv', index=False, header=True)

def tht():
    df = pd.read_csv('./raw_data/theater_data.csv', usecols=['LC_LA','LC_LO','POI_NM','BHF_NM', 'RDNMADR_NM', 'CTPRVN_NM'])
    df = df[df['CTPRVN_NM']=="서울특별시"]
    df['name'] = df['POI_NM']+' ' +df['BHF_NM']
    df['minimum'] = "none"
    df['distance'] = 0
    df = df.dropna(axis=0)

    print(df)

    for row in range(len(df)):
        target_latitude = df.iloc[row,5]
        target_longitude = df.iloc[row,4]
        distances_name = {}
        for one_row in range(len(df)):
            cor1 = [target_latitude, target_longitude]
            cor2 = [df.iloc[one_row,5], df.iloc[one_row,4]]
            dist = getDistance(cor1, cor2)
            distances_name[dist] = df.iloc[one_row,6]
        distance = list(distances_name.keys())
        distance.remove(min(distance))
        distance.remove(min(distance))
        distance.remove(min(distance))
        minimum_distance = min(distance)
        name = distances_name[minimum_distance]
        df.iloc[row,7]=name
        df.iloc[row,8]=minimum_distance
    #df.head()

    #df=df.sort_values('distance')
    df = df[['name', 'minimum', 'distance']]
    df=df.sort_values('distance')
    
    df.to_csv('tht.csv', index=False, header=True)



if __name__ == "__main__":
    lib()
