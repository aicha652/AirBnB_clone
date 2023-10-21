#!/usr/bin/python3
"""Module for FileStorage class"""
import json
import datetime


class FileStorage:

    """serializes instances and deserializes JSON file to instances
    Attributes:
        __file_path (str): string - path to the JSON file
        __objects (dict): dictionnary to store all objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj class name>.id"""
        key = obj.__class__.__name__
        self.__objects["{}.{}".format(key, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        obj = self.__objects
        dictio = {o: obj[o].to_dict() for o in obj.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as fl:
            json.dump(dictio, fl)

    def reload(self):
        """ deserializes the JSON file to __objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                   'BaseModel': BaseModel, 'User': User, 'State': State,
                   'City': City, 'Amenity': Amenity, 'Place': Place,
                   'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, "r") as fl:
                temp = json.load(fl)
            for key, val in temp.items():
                self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
