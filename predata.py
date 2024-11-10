import pandas as pd
from haversine import haversine
from pyproj import Proj, transform

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
        '''while isThereLessThanConst(distances_from_target, ):
            distances_from_target.remove(min(distances_from_target))'''
        
        #그냥 앞에서 세개씩 빼보자!
        distances_from_target.remove(min(distances_from_target))
        distances_from_target.remove(min(distances_from_target))
        distances_from_target.remove(min(distances_from_target))

        distance_of_minimums.append(min(distances_from_target))
    return distance_of_minimums

def distancesOfNearestByCity(raw_data, city_name):
    '''각 도서관별 다른 도서관과의 거리 중 최소들의 리스트
       raw_data = libraray_data자료, 필히 [latitude, longitude, city] 구조여야함
       cityname(열 이름이 필이 city여야 함)
       '''
    data_of_city = raw_data[raw_data['city']== city_name]
    '''https://ctkim.tistory.com/entry/Pandas-%EA%B0%95%EC%A2%8C-%E2%80%93-3-Pandas%ED%8C%90%EB%8B%A4%EC%8A%A4-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%A1%B0%ED%9A%8C-%EB%B0%8F-%EC%84%A0%ED%83%9D-loc-iloc
       데이터프레임에서 특정 도시만 추출해주는'''
    coordinates = getCoordinatesFromData(data_of_city)
    return distancesOfNearestCoordinate(coordinates)
        
def libraryDataPreprocessing():
    df = pd.read_csv('./raw_data/library_data.csv', usecols=['LBRRY_LA', 'LBRRY_LO', 'ONE_AREA_NM'])
    df.columns = ['latitude', 'longitude', 'city']
    df = df.dropna(axis=0) #결측치 있는 열 제거
    df.to_csv('library_preprocessed.csv', index = False, header = True)

def theaterDataPreprocessing():
    df = pd.read_csv('./raw_data/theater_data.csv', usecols=['LC_LA', 'LC_LO', 'CTPRVN_NM'])
    df = df[['LC_LA', 'LC_LO', 'CTPRVN_NM']]
    df.columns = ['latitude', 'longitude', 'city']
    df = df.dropna(axis=0)
    df.to_csv('theater_preprocessed.csv', index = False, header = True)

def gymDataPreprocessing():
    df = pd.read_csv('./raw_data/gym_raw.csv', usecols=['영업상태구분코드', '도로명전체주소', '좌표정보(x)', '좌표정보(y)'])
    df.columns = ['status', 'city', 'X-coordinate', 'Y-coordinate']
    df = df[df['status']==1] # 영업중인 헬스장만 남기기
    df = df.dropna(axis=0) # 결측치 제거
    
    # 주소를 도시 이름으로 변경
    for row in range(len(df)):
        address = df.iat[row, 1]
        city = address.split()[0]
        df.iat[row,1] = city
    
    # 좌표를 위도, 경도로 변환
    # https://dabid.tistory.com/3
    proj_1 = Proj(init='epsg:2097')
    proj_2 = Proj(init='epsg:4326')
    converted = transform(proj_1, proj_2, df['X-coordinate'].values, df['Y-coordinate'].values)
    df['latitude'] = converted[1] 
    df['longitude'] = converted[0]
    
    df = df[['latitude', 'longitude', 'city']]
    result = df[df['city'].isin(['서울특별시', '광주광역시', '부산광역시', '울산광역시', '대구광역시', '대전광역시', '인천광역시'])]
    result.to_csv('gym_preprocessed.csv', index=False, header = True)

def main():
    library = pd.read_csv('library_preprocessed.csv')
    theater = pd.read_csv('theater_preprocessed.csv')
    gym = pd.read_csv('gym_preprocessed.csv')
    
    ''' 도시별 데이터
    nearest type
    1092    gym
    12039   library
    이런 느낌
    '''
    city = {"서울특별시":"seoul", "광주광역시":"gwangju", "대구광역시":"daegu", "울산광역시":"ulsan", "인천광역시":"incheon",
            "대전광역시":"daejeon", "부산광역시":"busan"}
    for hangeul_city in city:
        nearest_library = distancesOfNearestByCity(library, hangeul_city)
        nearest_theater = distancesOfNearestByCity(theater, hangeul_city)
        nearest_gym = distancesOfNearestByCity(gym, hangeul_city)

        print(hangeul_city)
        df1 = pd.DataFrame({'nearest_distance':nearest_library, 'type':'library'})
        df2 = pd.DataFrame({'nearest_distance':nearest_theater, 'type':'theater'})
        df3 = pd.DataFrame({'nearest_distance':nearest_gym, 'type':'gym'})
        result = pd.concat([df1, df2, df3])
        filename = './results/'+city[hangeul_city] + ".csv"
        result.to_csv(filename, index=False, header=True)

if __name__ == '__main__':
    libraryDataPreprocessing()
    theaterDataPreprocessing()
    gymDataPreprocessing()
    main()
