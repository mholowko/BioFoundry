# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:17:56 2017

@author: bchhmb
"""

class Plate (object):
    
    
    def __init__ (self, wells = 384, filled_wells=0, volume = 0):
        self.wells = wells
        self.filled_wells = filled_wells
        self.volume = volume

    def fill_wells(self, filled_wells, volume):
        self.filled_wells = filled_wells
        self.volume = volume
        

class Thermal_Cycler(object):
    
    def __init__(self, plate_size = 96, number_of_plates = 1):
        self.plate_size = plate_size
        self.number_of_plates = number_of_plates

class Liquid_Handler2 (object):

    def __init__(self,channels = 1):
        self.channels = channels   
        
        
    def transfer (self,source_plate,destination_plate,volume):
        while volume > source_plate.volume:
            volume = int(input('What are you doing? Change the volume: '))
        
        
        
        
        destination_plate.filled_wells = source_plate.filled_wells
        destination_plate.volume = volume
        source_plate.volume -= volume
        
    def fill_wells (plate, filled_wells, volume):
        plate.filled_wells = filled_wells
        plate.volume = volume
    
    def distribute():
        pass
    
    def compress():
        pass
    
    def decompress():
        pass
    
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






