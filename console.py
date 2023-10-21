#!/usr/bin/python3
""" Module for HBNB console """
import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
from models.engine.file_storage import FileStorage
import json


class HBNBCommand(cmd.Cmd):
    """ The class for the command interpreter"""

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """EOF (End Of File) to exit program"""
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """an empty line doesn't do anything on Enter"""
        pass

    def errors(self, line, cmd):
        """manages error message for user input"""

        cls_list = [
                "BaseModel", "User", "State", "City",
                "Amenity", "Place", "Review"
                ]
        cmd_list = ["create", "show", "all", "destroy", "update"]

        if line == "":
            print("** class name missing **")
            return 1
        args = line.split()
        if args[0] not in cls_list and cmd in cmd_list:
            print("** class doesn't exist **")
            return 1
        elif cmd in ["create", "all"]:
            return
        if len(args) < 2 and cmd in ["show", "destroy", "update"]:
            print("** instance id missing **")
            return 1
        instances_dict = storage.all()
        args = self.remove_quot(args)
        k = args[0] + '.' + args[1]
        if k not in instances_dict and cmd in ["show", "destroy", "update"]:
            print("** no instance found **")
            return 1
        elif cmd in ["show", "destroy"]:
            return 0

        if len(args) < 3 and cmd == "update":
            print("** attribute name missing **")
            return 1
        if len(args) < 4 and cmd == "update":
            print("** value missing **")
            return 1
        return 0

    def do_create(self, line):
        """create an instance."""
        if (self.errors(line, "create") == 1):
            return False
        instance = eval(line)()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        """Print the string rpresentation of an instance"""
        if (self.errors(line, "show") == 1):
            return False

        args = line.split()
        instances_dict = storage.all()
        args = self.remove_quot(args)
        print(instances_dict[args[0] + '.' + args[1]])

    def do_destroy(self, line):
        """ Delete an instance :destroy <class> <id>"""
        if (self.errors(line, "destroy") == 1):
            return False
        instances_dict = storage.all()
        args = line.split()
        args = self.remove_quot(args)
        del instances_dict[args[0] + '.' + args[1]]
        storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances"""
        d_list = []
        instances_dict = storage.all()
        if line == "":
            d_list = [str(i) for i in instances_dict.values()]
            print(d_list)
            return False
        args = line.split()
        if (self.errors(line, "all") == 1):
            return False
        for i in instances_dict.values():
            if i.__class__.__name__ == args[0]:
                d_list.append(str(i))
        print(d_list)

    def do_count(self, cls_name):
        """This counts the instance of a class"""
        num_inst = 0
        instances_dict = storage.all()
        for inst in instances_dict.values():
            if inst.__class__.__name__ == cls_name:
                num_inst += 1
        print(num_inst)

    def remove_quot(self, arg):
        """remove the quotations and commas from the arguments"""
        for i in range(len(arg)):
            if arg[i][0] in ('"', "'"):
                arg[i] = arg[i].replace('"', "").replace("'", "")
        return arg

    def do_update(self, line):
        """Update " certain object with new info"""
        if (self.errors(line, "update") == 1):
            return False

            args = line.split()
            instances_dict = storage.all()
            args = self.remove_quot(args)
            x = args[0] + '.' + args[1]
            new_key = args[2]
            if args[3].isdigit():
                new_value = eval(args[3])
            else:
                new_value = args[3]
            setattr(instances_dict[x], new_key, new_value)
            storage.save()

    def default(self, line):
        """the default function """

        cls = ["BaseModel", "User", "State", "City",
               "Amenity", "Palce", "Review"
               ]
        cmd_list = {
                "show": self.do_show, "all": self.do_all,
                "destroy": self.do_destroy, "update": self.do_update,
                "create": self.do_create, "count": self.do_count
                }
        ln = line.maketrans(";.(),{}:", "        ")
        line = line.translate(ln)
        try:
            cls_name, cmd, *arg = line.split()
        except Exception as e:
            print("** Unknown syntax", file=sys.stderr)
            return False

        if cls_name in cls:
            for key, val in cmd_list.items():
                if cmd == key:
                    if cmd == "count":
                        val(cls_name)
                    elif cmd == "update":
                        for i in range(1, len(arg), 2):
                            x = cls_name + ' ' + arg[0] + ' ' +\
                                    arg[i] + ' ' + arg[i + 1]
                            val(x)
                    else:
                        val(cls_name + ' ' + (" ".join(arg)))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
