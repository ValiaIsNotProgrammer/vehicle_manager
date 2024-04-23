import requests

from model import Vehicle



class VehicleManager:

    resource_mapping = ...

    """
    Получение списка автомобилей
    Получение списка автомобилей по заданным параметрам (фильтрация)
    Получение информации об автомобиле по id
    Добавление нового автомобиля
    Изменение информации об автомобиле
    Удаление автомобиля
    Расчет расстояние между двумя автомобилями (в метрах)
    Нахождение ближайшего автомобиля к заданному

    GET /vehicles
    POST /vehicles
    GET /vehicels/{id}
    PUT /vehicles/{id} # у вас тут опечатка в описании
    DELETE /vehicles/{id}
    """

    def __init__(self, url):
        "в конце кодинга добавил, чтобы соответствовать примеру"
        self.url = url

    def get_api_root(self) -> str:
        api_root = "https://test.tspb.su/test-task/"
        return api_root

    def __get(self, endpoint: str, params: dict = None) -> requests.Response.json:
        url = self.get_api_root() + endpoint
        response = requests.get(url, params=params)
        return response.json()

    def __post(self, endpoint: str, params: dict = None) -> requests.Response.json:
        url = self.get_api_root() + endpoint
        response = requests.post(url, json=params)
        return response.json()

    def __put(self, endpoint: str, params: dict = None) -> requests.Response.json:
        url = self.get_api_root() + endpoint
        response = requests.put(url, json=params)
        return response.json()

    def __delete(self, endpoint: str, params: dict = None) -> requests.Response:
        url = self.get_api_root() + endpoint
        response = requests.delete(url, params=params)
        return response

    def get_vehicles(self) -> list[Vehicle]:
        response = self.__get("vehicles")
        objects = self.__from_json_list_to_vehicles(response)
        return objects

    def filter_vehicles(self, params) -> list[Vehicle]:
        response = self.__get("vehicles", params=params)
        filtered_json_list = self.__get_from_json_by_params(response, params)
        objects = self.__from_json_list_to_vehicles(filtered_json_list)
        if len(objects) == 1:
            return objects[0]
        return objects

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        response = self.__get("vehicles/" + str(vehicle_id))
        object = Vehicle(**response)
        return object

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        response = self.__post("vehicles", params=vehicle.to_dict())
        return Vehicle(**response)

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        response = self.__put(f"vehicles/{vehicle.id}", params=vehicle.to_dict())
        return Vehicle(**response)

    def delete_vehicle(self, vehicle_id: int) -> requests.Response:
        response = self.__delete(f"vehicles/{vehicle_id}")
        return response

    def get_distance(self, id1: int, id2: int) -> float: # кстати, погрешность при формуле говерсинуса 0.5 % т.к Земля - неидеальная сфера
        v1, v2 = self.get_vehicle(id1), self.get_vehicle(id2)
        lat1, lon1 = v1.latitude, v1.longitude
        lat2, lon2 = v2.latitude, v2.longitude
        from utils import calculate_distance
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        return distance

    def find_close_vehicle(self, vehicle_id: int) -> Vehicle:
        vehicles = self.get_vehicles()
        reference_vehicle = None
        for vehicle in vehicles:
            if vehicle.id == vehicle_id:
                reference_vehicle = vehicle
                vehicles.remove(vehicle)
                break

        reference_points = reference_vehicle.latitude, reference_vehicle.longitude
        points = self.__get_points_from(vehicles)

        from utils import find_closest_point
        closet_points = find_closest_point(reference_points, points)
        return self.get_vehicle_from_point(vehicles, closet_points)

    def get_vehicle_from_point(self, vehicles: list[Vehicle], reference_point: tuple[float, float]) -> Vehicle:
        for vehicle in vehicles:
            if vehicle.latitude == reference_point[0] and vehicle.longitude == reference_point[1]:
                return vehicle

    def __get_points_from(self, vehicles: list[Vehicle]) -> list[tuple[float, float]]:
        points = list()
        for vehicle in vehicles:
            points.append((vehicle.latitude, vehicle.longitude))
        return points

    def __get_from_json_by_params(self,json_list: list,  params: dict) -> list:
        filtered_json_list = []
        counter = 0 # если параметров более 1-го ожидаются, то нужно считать, все ли подходят по параметрам
        for json in json_list:
            for key, value in params.items():
                if json.get(key) == value:
                    counter += 1
                    if counter == len(params):
                        filtered_json_list.append(json)
            counter = 0
        return filtered_json_list

    def __from_json_list_to_vehicles(self, json_list: list) -> list[Vehicle]:
        vehicles = []
        for json in json_list:
            vehicles.append(Vehicle(**json))
        return vehicles




# v = Vehicle(
#     id=1,
#     name='Toyota',
#     model='Camry',
#     year=2021,
#     color='black',
#     price=21000,
#     latitude=55.753215,
#     longitude=37.620393
# )
# manager = VehicleManager("https://test.tspb.su/test-task/")
# print(manager.get_vehicles())
# print(manager.filter_vehicles(params={"name": "Toyota"}))
# print(manager.get_vehicle(vehicle_id=1))
# print(manager.add_vehicle(vehicle=Vehicle(
#                           id=1,
#                           name='Toyota',
#                           model='Camry',
#                           year=2021,
#                           color='red',
#                           price=21000,
#                           latitude=55.753215,
#                           longitude=37.620393
# )))
# print(manager.update_vehicle(vehicle=v))
# print(manager.delete_vehicle(1))
# print(manager.get_distance(1,2))
# print(manager.find_close_vehicle(1))