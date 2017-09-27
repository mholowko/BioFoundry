from bqplot import *
from IPython.display import display
import math


#PCR setup (Master mix)
def PCRsetup (NConst):
    #Program to calculate required PCR components
    #NFrag = input('Put in the number of combinations: ')
    NFrag = math.ceil(NConst/5) #Number of DNA fragments to process, the divisor is proportional to the complexity of the constrtucion
    NPrimer = NFrag * 2
    Vmm = NFrag * 5 #volume of PCR Master Mix in uL
    Compmm = {'buffer': 0.2*Vmm, 'dNTPs' : 0.02*Vmm, 'polymerase' : 0.01*Vmm, 'water' : 0.77*Vmm}
    NRes = math.ceil((Vmm+250)/2800) #number of reservoir wells needed
    #print("Number of fragments to PCR is " + str(NFrag))
    #print("Required volume of Master Mix is " + str(Vmm) + " ul")
    #print("Required volume of polymerase is " + str(round(Compmm['polymerase'],1)) + " ul")
    #print("Required number of wells in reservoir for PCR Master Mix is " + str(NRes))
    return (NFrag,NPrimer,NRes,Vmm)

#Echo
def Echo (sourcewells,reaction):
    #all times in seconds if not defined otherwise
    import math
    if reaction == "PCR": 
        NPlatesF = math.ceil(sourcewells[0]/96)  #Number of plates with PCR mixtures
        NPlatesP = math.ceil(sourcewells[1]/384) #Number of plates with primers
        NPlatesR = math.ceil(sourcewells[2]/6)   #Number of reservoir plates
        NPlates = NPlatesF + NPlatesP + NPlatesR
        Tinitload = 120 #seconds 
        Tprocess = sourcewells[0] * 0.2 #seconds
        Tchange = 45 #seconds
        TTotal = (Tinitload + (Tprocess + Tchange) * NPlates)/60 #minutes
        #print('Number of source plates with plasmids needed is ' + str(NPlates))
        #print('Total time to prepare the plates in Echo for PCR = ' + str(round(TTotal,1)) + " min")
        return (NPlatesF, TTotal)
    elif reaction == "Gibson": #not finished
        NPlatesF = math.ceil(sourcewells[0]/384)
        NPlatesG = math.ceil(sourcewells[1]/384) #number of Gibson plates
        NPlates = NPlatesF + NPlatesG
        Tinitload = 120 #seconds 
        Tprocess = sourcewells[0] * 0.2 #seconds
        Tchange = 45 #seconds
        TTotal = (Tinitload + (Tprocess + Tchange) * NPlates)/60 #minutes
        #print("Required number of plates with Gibson mixes " + str(NPlatesG))
        #print('Total time to prepare the plates in Echo for PCR = ' + str(round(TTotal,1)) + " min")
        return(NPlatesG, TTotal)
    else:
        print("Unknown process")
        return 
    
#Thermal Cycler processes running time
def ThermalCycler (Nplates,reaction):
    if reaction == "PCR":
        Tpcr = 120 * Nplates #minutes
        #print("Time required to run the PCR is " + str(Tpcr) + " min")
        return (Tpcr)
    elif reaction == "Gibson":
        Tgibson = 20 * Nplates #minutes
        #print("Time required to run the PCR is " + str(Tgibson) + " min")
        return (Tgibson)
    else:
        print("Unknown process")
        return 

#Gibson Reaction Setup
def Gibson (NFrag):
    import math
    Vgibson = NFrag * 5 #in uL
    NRes = math.ceil((Vgibson+250)/2800) #numbrer of reservoir wells needed
    #print ("Required volume of Gibson Master Mix is " + str(Vgibson) + " uL.")
    #print("Required number of wells in reservoir for Gibson Master Mix is " + str(NRes))
    return(NRes,Vgibson)

#Transformation
def Transformation (Ntrans):
    #All times in seconds
    import math
    NplateT = math.ceil(Ntrans/96) #Number of plates with transformants
    T_thaw = 300 #Time of thawing the cells
    T_add = 300 #Time for cells distribution/plasmid/recovery media addition
    T_plasmid = 300 #Time for plasmid addition
    T_incubation = 1800 #Incubation time
    T_heatshock = 45 #Heat shock time
    T_recovery = 3600 #Recovery time
    T_Total = (T_thaw + T_add*3 + T_incubation + T_heatshock + T_recovery) * NplateT / 60
    return(T_Total)

#Calculation of costs
def Costs (Vmm,Vgibson,NPlatesF,NPlatesG,NFrag):
    Price={'PCR_MM': 0.01376, 'Gibson_MM': 1.98413, '96_well_plate': 5, '384_well_plate': 5, 'Primers': 10} #in SGD for 1 mL
    Totalcost = Price['PCR_MM']*Vmm + Price['Gibson_MM']*Vgibson + Price['96_well_plate']*(NPlatesF + NPlatesG) + Price['Primers']*2*NFrag
    return (Totalcost)
    
#Creating plots
def Plots (Lists):    

    i=0

    for List in Lists:
        Titles = ['Time = f (Number of constructs)','Number of Gibson plates = f (Number of constructs)','Number of PCR Plates = f (Number of constructs)','Cost = f (Number of constructs)']
        y_Labels = ['Time[h]','Number of Gibson plates','Number of PCR Plates','Cost [SGD]']

        x_data = NConstList
        y_data = List

        x_sc = LinearScale()
        y_sc = LinearScale()
        
        panzoom = PanZoom(scales={'x': [x_sc], 'y': [y_sc]})

        ax_x = Axis(label='Number of constructs', scale=x_sc, tick_format='0.0f')
        ax_y = Axis(label_offset='-50', label=y_Labels[i], scale=y_sc, orientation='vertical', tick_format='0.0f')

        line = Lines(x=x_data,
                     y=y_data,
                     scales={'x': x_sc, 'y': y_sc},
                     colors=['red', 'yellow'])

        fig = Figure(axes=[ax_x, ax_y], marks=[line],title = Titles[i],interaction = panzoom)

        display(fig)

        i += 1


#Controls
def Control(NConst):
    import math
    TTotal = 0
    PCRPar = PCRsetup(NConst)
    NPlatesF,Ttemp = Echo (PCRPar,"PCR")
    TTotal += Ttemp
    TTotal += ThermalCycler(NPlatesF, "PCR")
    GibsonPre = Gibson(PCRPar[0])
    GibsonP = (NPlatesF, NConst, GibsonPre[0],GibsonPre[1])
    NPlatesG, Ttemp = Echo(GibsonP, "Gibson")
    TTotal += Ttemp
    TTotal += ThermalCycler(NPlatesG, "Gibson")
    TTotal += Transformation(NPlatesG)
    Totalcost = Costs(PCRPar[3],GibsonP[3],NPlatesF,NPlatesG,PCRPar[0])
    return (TTotal,NPlatesG,NPlatesF,Totalcost)

N_Const = 10000    # Number of constructs
Control_variables = Control(N_Const)
print(str(round(Control_variables[0]/60,1)) + ' hours are needed to finish the process')

TimeList = []
GibsonPlateList = []
PCRPlateList = []
CostList = []
NConstList = range (10,10010,10)
for N_Const in NConstList:
    Control_variables = Control(N_Const)
    #print(str(round(Control_variables[0]/60,1)) + ' hours are needed to finish the process')
    TimeList.append(Control_variables[0]/60) 
    GibsonPlateList.append(Control_variables[1])
    PCRPlateList.append(Control_variables[2])
    CostList.append(Control_variables[3])

Lists = [TimeList,GibsonPlateList,PCRPlateList,CostList]

Plots(Lists)

