# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:17:56 2017

@author: bchhmb
"""

import math
import matplotlib.pyplot as plt

class Plate (object):
    
    def __init__ (self, name=' ', wells = 384, filled_wells = 0, maxvolume = 0, volume = 0, status='new', start_time = 0):
        self.name = name
        self.wells = wells
        while filled_wells > wells:
            filled_wells=int(input(str(self.name) + ': You are trying to fill more wells than available. Please input the correct number: '))
        self.filled_wells = filled_wells
        self.maxvolume = maxvolume
        self.volume = volume
        self.TotalVolume = self.volume * filled_wells
        self.status = status
        self.time = start_time

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
        
    def PCR(self, plate, time):
        plate.status = 'PCR done'
        plate.time += time 
        
    def Assembly(self, plate, time):
        plate.status = 'Assembly done'
        plate.time += time 
        


class Liquid_Handler2 (object):

    def __init__(self,channels = 1, well_processing_time=0, plate_change_time=0):
        self.channels = channels
        self.well_processing_time = well_processing_time
        self.plate_change_time = plate_change_time
    
    def fillplate (self, source_plate, destination_plate, destination_wells, volume):
        destination_plate.filled_wells = destination_wells
        source_plate.removevolume(volume*destination_plate.filled_wells)
        source_plate.time = source_plate.filled_wells / self.channels * self.well_processing_time
        source_plate.status = 'liquid transferred'
        destination_plate.addvolume(volume)
        destination_plate.time = source_plate.filled_wells / self.channels * self.well_processing_time
        destination_plate.status = 'filled'

     
    def transfer (self,source_plate,destination_plate,volume):
        while volume + destination_plate.volume>destination_plate.maxvolume or volume > source_plate.volume:
            volume = int(input('Incorrect transfer value. Please input the correct number: '))
        destination_plate.filled_wells = source_plate.filled_wells
        source_plate.removevolume(volume)
        source_plate.time = source_plate.filled_wells / self.channels * self.well_processing_time
        source_plate.status = ''
        destination_plate.addvolume(volume)
        destination_plate.time = source_plate.filled_wells / self.channels * self.well_processing_time
        destination_plate.status = ''
        
    
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
            plate.time = plate.filled_wells / self.channels * self.well_processing_time + self.plate_change_time
            plate.status = 'compressed'
        for i in compressed_plates:
            i.addvolume(volume)
            plate.time = plate.filled_wells / self.channels * self.well_processing_time + self.plate_change_time
            plate.status = 'new'
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
        source_plate.time = source_plate.filled_wells / self.channels * self.well_processing_time + self.plate_change_time
        source_plate.status = 'decompressed'
        for plate in decompressed_plates:
            plate.addvolume(volume)
            plate.time = source_plate.filled_wells / self.channels * self.well_processing_time + self.plate_change_time
            plate.status = 'new'
        return decompressed_plates    
    
    
    def additional():
        pass

def plot (Lists):    

    y_Labels = ['Time[h]']
    Titles = ['Time = f (Number of constructs)']
    
    i=0
    
    for List in Lists:

        fig, ax = plt.subplots()
        ax.plot(PCR_reactions_list,List)
        ax.set(xlabel='Number of constructs [U]', ylabel=y_Labels[i],
               title=Titles[i])
        ax.grid()
        plt.show()
        
        i += 1





PCR_reactions_list = range (10,10010,10)
TotalTimeList = []
for PCR_reactions in PCR_reactions_list:

    PCR_plate_size = 384   
    PCR_plate_number = math.ceil(PCR_reactions/PCR_plate_size)
    Complexity = PCR_reactions / PCR_reactions
    
    Opentron = Liquid_Handler2(8,1,10)
    Echo =  Liquid_Handler2(1,1,10)
    Thermalcycler = Thermal_Cycler()
    TotalTime = 0

    
    for i in range(0,PCR_plate_number):
        PrimerPlate = Plate('PrimerPlate',384,384,50,50)
        MasterMixPlate = Plate('MasterMixPlate',6,1,5000,5000) 
        PCRPlate = Plate('PCRPlate',384,0,50,0,'PCR not done')
    
        UsedPlatesList = []
        
        Opentron.fillplate(MasterMixPlate, PCRPlate, 384 ,10)
        UsedPlatesList.append(MasterMixPlate)
        
        Echo.transfer(PrimerPlate, PCRPlate, 0.5)
        UsedPlatesList.append(PrimerPlate)
        
        Thermalcycler.PCR(PCRPlate,120*60)
        UsedPlatesList.append(PCRPlate)
        
        
        
        for plate in UsedPlatesList:
            TotalTime += plate.time
        
    print('Total running time is ' + str(math.ceil(TotalTime/60)) + " min")
    TotalTimeList.append(TotalTime/60)
    

plot ([TotalTimeList])

#plate splice
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96] 
b = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192]
c = [193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288]
d = [289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313,314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384]

#Dr Foo's Protocols
MasterMixPlate = Plate('MasterMixPlate',6,1,5000,5000)
PCRPlate = Plate('PCRPlate',384,0,50,0)
PrimerPlate1 = Plate('PrimerPlate1',96,96,360,100)
PrimerPlate2 = Plate('PrimerPlate2',96,96,360,100)
PrimerPlate3 = Plate('PrimerPlate3',96,96,360,100)
PrimerPlate4 = Plate('PrimerPlate4',96,96,360,100)
ECHOPlate = Plate('ECHOPlate', 384,0,65,0)
PCRPlate1 = Plate('PCRPlate1',96,0,360,0)
PCRPlate2 = Plate('PCRPlate2',96,0,360,0)
PCRPlate3 = Plate('PCRPlate3',96,0,360,0)
PCRPlate4 = Plate('PCRPlate4',96,0,360,0)
Opentrons = Liquid_Handler2(8)
Echo = Liquid_Handler2(1)
Thermalcycler = Thermal_Cycler()

#Distribution of Master Mix
Opentrons.transfer(MasterMixPlate,PCRPlate,10)

#Transferring Primers to ECHO plate
Opentrons.transfer(PrimerPlate1,ECHOPlate.wells(a),10)
Opentrons.transfer(PrimerPlate2,ECHOPlate.wells(b),10)
Opentrons.transfer(PrimerPlate3,ECHOPlate.wells(c),10)
Opentrons.transfer(PrimerPlate4,ECHOPlate.wells(d),10)

#Transfer of primers from ECHO plate to PCR plate
Echo.transfer(ECHOPlate,PCRPlate,2.5)

#Transfer of PCR mixture to respective plates
Opentrons.transfer(PCRPlate.wells(a),PCRPlate1,10)
Opentrons.transfer(PCRPlate.wells(b),PCRPlate2,10)
Opentrons.transfer(PCRPlate.wells(c),PCRPlate3,10)
Opentrons.transfer(PCRPlate.wells(d),PCRPlate4,10)

#Performing PCR reactions for each plate
Thermalcycler.PCR(PCRPlate1)
Thermalcycler.PCR(PCRPlate2)
Thermalcycler.PCR(PCRPlate3)
Thermalcycler.PCR(PCRPlate4)
