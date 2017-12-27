# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:17:56 2017

@author: bchhmb
"""

class Plate (object):
    
    
    def __init__ (self, name=' ', wells = 384, filled_wells = 0, maxvolume = 0, volume = 0):
        self.name = name
        self.wells = wells
        while filled_wells > wells:
            filled_wells=int(input(str(self.name) + ': You are trying to fill more wells than available. Please input the correct number: '))
        self.filled_wells = filled_wells
        self.maxvolume = maxvolume
        self.volume = volume
        self.TotalVolume = self.volume * filled_wells

    def addvolume(self,volume):
        while volume + self.volume>self.maxvolume:
            volume = int(input(str(self.name) + ': You are trying to add more volume than maximum available. Please input the correct number: '))
        self.volume += volume
        
    def removevolume(self,volume):
        while volume > self.volume:
            volume = int(input(str(self.name) + ': You are trying to remove more volume than available. Please input the correct number: '))
        self.volume -= volume 
        

class Thermal_Cycler(object):
    
    def __init__(self, plate_size = 96, number_of_plates = 1):
        self.plate_size = plate_size
        self.number_of_plates = number_of_plates

class Liquid_Handler2 (object):

    def __init__(self,channels = 1):
        self.channels = channels   
         
    def transfer (self,source_plate,destination_plate,volume):
        while volume + destination_plate.volume>destination_plate.maxvolume or volume > source_plate.volume:
            volume = int(input('Incorrect transfer value. Please input the correct number: '))
        destination_plate.filled_wells = source_plate.filled_wells
        source_plate.removevolume(volume)
        destination_plate.addvolume(volume)
       
    def fill_wells (self, plate, filled_wells, volume):
        if volume > plate.maxvolume:
            volume = int(input('Incorrect volume value. Please input the correct value: '))
        plate.filled_wells = filled_wells
        plate.volume = volume
    
    def distribute(self, plate, filled_wells, volume):
        if volume > plate.maxvolume:
            volume = int(input('Incorrect volume value. Please input the correct value: '))
        plate.filled_wells = filled_wells
        plate.volume = volume
    
    def compress(self, source_plate, destination_plate, volume):
        if source_plate.wells < destination_plate.wells:
            print('Please check the plates again')
            source_plate = int(input('Source Plate: '))
            destination_plate = int(input('Destination Plate: '))
        source_plate.removevolume(volume)
        destination_plate.addvolume(volume)
    
    def decompress(self, source_plate, destination_plate, volume):
        if source_plate.wells > destination_plate.wells:
            print('Please check the plates again')
            source_plate = int(input('Source Plate: '))
            destination_plate = int(input('Destination Plate: '))
        source_plate.removevolume(volume)
        destination_plate.addvolume(volume)
    
    def additional():
        pass





PrimerPlate = Plate(384,384,50)
TemplatePlate = Plate(384,186,20)
MasterMixPlate = Plate(6,1,1800) 
PCRPlate = Plate(384,0,0)
Opentron = Liquid_Handler2(8)
Echo =  Liquid_Handler2(1)


print('PCRPlate before Echo ' + str(PCRPlate.filled_wells) + ' ' + str(PCRPlate.volume))
print('PrimerPlate before Echo ' + str(PrimerPlate.filled_wells) + ' ' + str(PrimerPlate.volume))

Echo.transfer(PrimerPlate,PCRPlate,60)

print('PCRPlate after Echo ' + str(PCRPlate.filled_wells) + ' ' + str(PCRPlate.volume))
print('PrimerPlate after Echo ' + str(PrimerPlate.filled_wells) + ' ' + str(PrimerPlate.volume))
