# AUTHOR : James Gadoury
# CONTACT: gadouryjames@gmail.com
# GUI application developed using Tkinter and Python3
# Dreams in Text : Text game with a fantastical setting
# relies on playgame.py, game.py, interactables.py, and items.py

from interactables import *

interactions = ['take', 'punch', 'kick', 'break', 'drop', 'climb', 'open', 'attack', 'shoot', 'pick up']

for action in interactions[:]:
    interactions.append(action + ' the')


class Inventory:
    def __init__(self):
        self._inventory = []

    def add_item(self, item):
        self._inventory.append(item)

    def remove_item(self, item):
        self._inventory.remove(item)

    @property
    def inventory(self):
        return [item for item in self._inventory]

    def show_inventory(self):
        if len(self.inventory) > 0:
            print("You are currently holding: ")
            for i, item in enumerate(self.inventory, 1):
                print(f'[{i}] {item}')
        else:
            print("You don't have anything!")


class Interactable:
    def __init__(self):
        pass

    def interact_with_object(self, ui):
        self._ui = ui.rsplit(' ', 1)[0]

    @property
    def ui(self):
        return self._ui.lower()


class Lamp(Interactable):
    lampInteractionList = ['take', 'break', 'punch', 'kick', 'drop', 'pick up']
    for i in range(len(lampInteractionList)):
        lampInteractionList.append(lampInteractionList[i] + ' the')

    def __init__(self):
        Interactable.__init__(self)
        self.usable = True

    def breaks(self, object_dictionary):
        self.usable = False
        object_dictionary['i'].remove_item('lamp')

    def engage_lamp(self, UI, object_dictionary):
        self.interact_with_object(UI)
        if self.ui in self.lampInteractionList:
            if self.ui == 'take' or self.ui == 'take the' or self.ui == 'pick up' or self.ui == 'pick up the':
                if 'lamp' not in object_dictionary['i'].inventory:
                    if self.usable:
                        print("You pick up the lamp.")
                        object_dictionary['i'].add_item('lamp')
                    else:
                        print("The lamp is broken. It is useless now.")
                else:
                    print("You are currently holding the lamp!")
            elif self.ui == 'drop' or self.ui == 'drop the':
                if 'lamp' in object_dictionary['i'].inventory:
                    print("You drop the lamp.")
                    print("It shatters on the ground.")
                    self.breaks()
                    object_dictionary['i'].remove_item('lamp')
                else:
                    print("You are not holding the lamp!")
            elif self.ui == 'break' or self.ui == 'break the':
                if 'lamp' in object_dictionary['i'].inventory:
                    print("You break the lamp.")
                    self.breaks()
                    object_dictionary['i'].remove_item('lamp')
                else:
                    print("You are not holding the lamp!")
            else:
                error()

        else:
            error()

    def use_lamp(self, ui, object_dictionary):

        self.interact_with_object(ui)

        if 'lamp' not in object_dictionary['i'].inventory:
            print("You are not holding the lamp!")
        else:
            if self.ui == 'break window with' or self.ui == 'break the window with':
                object_dictionary['w'].engage_window('break window with lamp x', object_dictionary)
            elif self.ui == 'break door with' or self.ui == 'break the door with':
                object_dictionary['d'].engageDoor('break door with lamp x', object_dictionary)
            elif self.ui == 'attack robot with' or self.ui == 'attack the robot with':
                object_dictionary['r'].engage_robot('attack robot with lamp x', object_dictionary)
            else:
                error()


class Gun(Interactable):

    def __init__(self):
        Interactable.__init__(self)
        self.usable = True
        self.bullet_count = 3

    def shoot_gun(self):
        self.bullet_count -= 1
        if not self.bullet_count:
            self.usable = False
        return self.bullet_count

    def engage_pistol(self, ui, object_dictionary):
        self.interact_with_object(ui)
        if self.ui in interactions:
            if self.ui == 'take' or self.ui == 'take the' or self.ui == 'pick up' or self.ui == 'pick up the':
                if object_dictionary['r'].awake:
                    print("You reach to take the pistol from the robot's side...")

                    if not object_dictionary['r'].can_be_commanded:
                        print("The robot covers the pistol with its large hand.")

                        print("'No...no. I can't let you take this. I may need it.', the robot patronizes.")
                    else:
                        self.take_pistol(object_dictionary)
                elif 'gun' not in object_dictionary['i'].inventory:
                    self.take_pistol(object_dictionary)
                else:
                    print("You are currently holding the pistol!")
            elif self.ui == 'drop' or self.ui == 'drop the':
                if 'pistol' in object_dictionary['i'].inventory:
                    print("You drop the pistol.")
                    object_dictionary['i'].remove_item('pistol')
                else:
                    print("You are not holding the pistol!")
            elif self.ui == 'break' or self.ui == 'break the':
                if 'pistol' in object_dictionary['i'].inventory:
                    print("You can't break the pistol.")
                else:
                    print("You are not holding the pistol!")
            else:
                error()

        else:
            error()

    def take_pistol(self, object_dictionary):
        if self.usable:
            print("You pick up the pistol.")

            print("It has two bullets in the clip and one in the chamber.")
            object_dictionary['i'].add_item('pistol')
        else:
            print("The pistol is out of bullets. It is useless now.")

    def use_pistol(self, UI, object_dictionary):

        self.interact_with_object(UI)

        if 'pistol' not in object_dictionary['i'].inventory:
            print("You are not holding the pistol!")
        elif not self.usable:
            print("The pistol is out of bullets. It is useless now.")
        else:
            if self.ui in ('break window with', 'break the window with', 'shoot window with', 'shoot the window with'):
                self.shoot_gun()
                object_dictionary['w'].engage_window('shoot window with pistol x', object_dictionary)
            elif self.ui in ('break door with', 'break the door with', 'shoot door with', 'shoot the door with'):
                self.shoot_gun()
                object_dictionary['d'].engageDoor('shoot door with pistol x', object_dictionary)
            elif self.ui in ('attack robot with', 'attack the robot with', 'shoot robot with', 'shoot the robot with'):
                self.shoot_gun()
                object_dictionary['r'].engage_robot('attack robot with pistol x', object_dictionary)
            else:
                error()


def error():
    print("*You can't do that*")
    print("type HELP if confused.")
