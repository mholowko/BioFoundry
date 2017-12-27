# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:17:56 2017

@author: mholowko & yvonnefoo
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
        
    def PCR():
        pass
        
    def Assembly():
        pass
        


class Liquid_Handler2 (object):

    def __init__(self,channels = 1):
        self.channels = channels   
         
    def transfer (self,source_plate,destination_plate,volume):
        while volume + destination_plate.volume>destination_plate.maxvolume or volume > source_plate.volume:
            volume = int(input('Incorrect transfer value. Please input the correct number: '))
        destination_plate.filled_wells = source_plate.filled_wells
        source_plate.removevolume(volume)
        destination_plate.addvolume(volume)
    
    def compress(self, source_plates, new_plate_wells, volume):
        import math
        if source_plates[0].wells >= new_plate_wells:
            new_plate_wells = int(input('The new plates format is smaller or the same as original plate. Please provide valid format: '))
        totalwells = 0
        for plate in source_plates:
            totalwells += plate.filled_wells        
        Nnew_plates = math.ceil(totalwells/new_plate_wells)
        tofill = []
        while totalwells > 0:
            if totalwells > new_plate_wells:
                tofill.append(new_plate_wells)
                totalwells -= new_plate_wells
            else:
                tofill.append(totalwells)
                totalwells -= totalwells
        compressed_plates = []
        for i in range(0,Nnew_plates):
            CompressedPlate = Plate ('CompressedPlate ' + str(i), new_plate_wells, tofill[i]  ,50,0)
            compressed_plates.append(CompressedPlate)
        for plate in source_plates:
            plate.removevolume(volume)
        for i in compressed_plates:
            i.addvolume(volume)
        return compressed_plates 
    
    def decompress(self, source_plate, new_plate_wells, volume):
        import math
        if source_plate.wells <= new_plate_wells:
            new_plate_wells = int(input('The new plates format is larger or the same as original plate. Please provide valid format: '))
        Nnew_plates = math.ceil(source_plate.filled_wells/new_plate_wells)
        filling = source_plate.filled_wells
        tofill = []
        while filling > 0:
            if filling > new_plate_wells:
                tofill.append(new_plate_wells)
                filling -= new_plate_wells
            else:
                tofill.append(filling)
                filling -= filling
        decompressed_plates = []
        for i in range(0,Nnew_plates):
            DecompessedPlate = Plate ('DecompressedPlate ' + str(i), new_plate_wells, tofill[i]  ,50,0)
            decompressed_plates.append(DecompessedPlate)
        source_plate.removevolume(volume)
        for i in decompressed_plates:
            i.addvolume(volume)
        return decompressed_plates    
    
    
    def additional():
        pass



PrimerPlate = Plate('PrimerPlate',384,384,50,50)
TemplatePlate = Plate('TemplatePlate',384,126,50,20)
MasterMixPlate = Plate('MasterMixPlate',6,1,2800,1800) 
PCRPlate = Plate('PCRPlate',384,0,50,0)
Opentron = Liquid_Handler2(8)
Echo =  Liquid_Handler2(1)
Thermalcycler = Thermal_Cycler()

print(PrimerPlate.TotalVolume)


print('PCRPlate before Echo ' + str(PCRPlate.filled_wells) + ' ' + str(PCRPlate.volume))
print('PrimerPlate before Echo ' + str(PrimerPlate.filled_wells) + ' ' + str(PrimerPlate.volume))

Echo.transfer(PrimerPlate,PCRPlate,40)

print('PCRPlate after Echo ' + str(PCRPlate.filled_wells) + ' ' + str(PCRPlate.volume))
print('PrimerPlate after Echo ' + str(PrimerPlate.filled_wells) + ' ' + str(PrimerPlate.volume))


NewPlate = Plate('NewPlate',384,200,50,50)

Decompressedplates = Opentron.decompress(NewPlate, 96, 20)


print('NewPlate after Decompression ' + str(NewPlate.filled_wells) + ' ' + str(NewPlate.volume))
for i in Decompressedplates:
    print(str(i.name) + ' after Decompression ' + str(i.filled_wells) + ' ' + str(i.volume))
    

Compressedplates = Opentron.compress(Decompressedplates, 184, 10)

for i in Decompressedplates:
    print(str(i.name) + ' after Compression ' + str(i.filled_wells) + ' ' + str(i.volume))

for i in Compressedplates:
    print(str(i.name) + ' after Compression ' + str(i.filled_wells) + ' ' + str(i.volume))
