# -*- coding: utf-8 -*-
import math
import sys
import numpy as np

class residue:

    # A class for residue information

    def __init__(self,
                 name            = "",
                 freq            = 0,
                 res_list        = [],
                 quantity        = 0,
                 av_mean_density = [],
                 atom_stand_dev  = []):
            
        self.name            = name
        self.freq            = freq
        self.res_list        = res_list
        self.quantity        = quantity
        self.av_mean_density = av_mean_density
        self.atom_stand_dev  = atom_stand_dev


class StructurePDB(object):

    # A class for coordinate PDB file atom

    def __init__(self,
                 atomnum            = 0,
                 residuenum         = 0,
                 atomtype           = "",
                 basetype           = "",
                 chaintype          = 'A',
                 X_coord            = 0,
                 Y_coord            = 0,
                 Z_coord            = 0,
                 atomID             = "",
                 numsurroundatoms   = 0,
                 numsurroundprotons = 0,
                 vdw_rad            = 0,
                 atomOrHetatm       = "" ):
            
        self.atomnum            = atomnum
        self.residuenum         = residuenum
        self.atomtype           = atomtype
        self.basetype           = basetype 
        self.chaintype          = chaintype
        self.X_coord            = X_coord
        self.Y_coord            = Y_coord
        self.Z_coord            = Z_coord
        self.atomID             = atomID
        self.numsurroundatoms   = numsurroundatoms
        self.numsurroundprotons = numsurroundprotons
        self.vdw_rad            = vdw_rad
        self.atomOrHetatm       = atomOrHetatm

        self.nucAcidTypes     = ['DA',
                                 'DC',
                                 'DG',
                                 'DT',
                                 'A',
                                 'C',
                                 'G',
                                 'U']

        self.mainchainProtein = ['N',
                                 'CA',
                                 'C',
                                 'O']

        self.mainchainNucAcid = ["P",
                                 "OP1",
                                 "O5'",
                                 "C5'",
                                 "C4'",
                                 "C3'",
                                 "O3'",
                                 "C2'",
                                 "C1'",
                                 "O4'",
                                 "OP2"]
   
    def protein_or_nucleicacid(self):

        # determine whether the current atom is 
        # a constituent of protein or nucleic acid 

        if self.basetype in self.nucAcidTypes:
            component_type = 'nucleic acid'
        else:
            component_type = 'protein'  
        return component_type
        
    def side_or_main(self):

        # determine whether current atom is 
        # part of main or side chain

        if self.basetype in self.nucAcidTypes:
            if self.atomtype not in self.mainchainNucAcid:
                sideormain = 'sidechain'
            else:
                sideormain = 'mainchain'
        else:
            if self.atomtype not in self.mainchainProtein:
                sideormain = 'sidechain'
            else:
                sideormain = 'mainchain'
        return sideormain
            
    def VDW_get(self):

        # determine VDW radius for atom type

        filename = 'VDVradiusfile.txt'
        vdw      = 'notyetdefined'

        try: # only proceed if file actually found
            VDWradfile  = open(str(filename),'r')
        except IOError:
            self.vdw_rad = 'Unable to locate {} file'.format(filename)
            return

        for line in VDWradfile.readlines():
            a = str(line.split()[1]).lower()
            b = str(self.atomID).lower()
            if a == b:
                # convert VDV radius for element into Angstroms as required:
                val = line.split()[5]
                try: 
                    float(val)
                except ValueError:
                    vdw = 'N/A'
                    break
                vdw = float(line.split()[5])*(0.01)
                break
            else:
                pass
        if vdw == 'notyetdefined':
            print 'Error finding vdw radius from reference file'
            print 'Check reference file...'
            print 'Atom identity given by: {} {}'.format(self.atomnum,self.getAtomID())
            sys.exit()
        VDWradfile.close()
        self.vdw_rad = vdw

    def getAtomID(self):

        # get a unique identifier for atom within structure, 
        # not dependent on atom number which may differ 
        # between different datasets of same structure

        ID = '{}-{}-{}-{}'.format(self.chaintype,
                                  self.residuenum,
                                  self.basetype,
                                  self.atomtype)
        return ID

    def getProtonNumber(self,
                        printText = True):

        # hard coded proton numbers for specific atom 
        # types (not all, may need to add to this)

        protonDic = {'H':1,
                     'C':6,
                     'N':7,
                     'O':8,
                     'NA':11,
                     'MG':12,
                     'P':15,
                     'S':16,
                     'CL':17,
                     'K':19,
                     'CA':20,
                     'MN':25,
                     'FE':26,
                     'NI':28,
                     'ZN':30}
        try:
            protonNum = protonDic[self.atomID]
        except KeyError:
            if printText is True:
                str = 'Unable to find proton number for atom {}, '.format(self.atomID)+\
                      'must hard code in classHolder.py to continue'
                print str
            return
        return protonNum
  
class singlePDB(StructurePDB):

    # StructurePDB subclass for a single pdb file structure

    def __init__(self,
                 atomnum            = 0,
                 residuenum         = 0,
                 atomtype           = "",
                 basetype           = "",
                 chaintype          = "",
                 X_coord            = 0,
                 Y_coord            = 0,
                 Z_coord            = 0,
                 Bfactor            = 0,
                 Occupancy          = 0,
                 meandensity        = 0,
                 maxdensity         = 0,
                 mindensity         = 0,
                 mediandensity      = 0,
                 atomID             = "",
                 numsurroundatoms   = 0,
                 numsurroundprotons = 0,
                 vdw_rad            = 0,
                 atomOrHetatm       = "",
                 bdam               = 0,
                 bdamchange         = 0,
                 Bfactorchange      = 0,
                 numvoxels          = 0,
                 stddensity         = 0,
                 min90tile          = 0,
                 max90tile          = 0,
                 min95tile          = 0,
                 max95tile          = 0):
                    
        super(singlePDB, self).__init__(atomnum, 
                                        residuenum, 
                                        atomtype,
                                        basetype, 
                                        chaintype, 
                                        X_coord,
                                        Y_coord, 
                                        Z_coord, 
                                        atomID,
                                        numsurroundatoms,
                                        numsurroundprotons,
                                        vdw_rad, 
                                        atomOrHetatm)
            
        self.Bfactor        = Bfactor 
        self.Occupancy      = Occupancy
        self.meandensity    = meandensity
        self.maxdensity     = maxdensity
        self.mindensity     = mindensity
        self.mediandensity  = mediandensity
        self.bdam           = bdam
        self.bdamchange     = bdamchange
        self.Bfactorchange  = Bfactorchange        
        self.numvoxels      = numvoxels
        self.stddensity     = stddensity  
        self.min90tile      = min90tile
        self.max90tile      = max90tile
        self.min95tile      = min95tile
        self.max95tile      = max95tile
    
    def vdw_bfac(self):

        # determine a B-factor weighted VDW radius around atom

        return 4*(math.sqrt(float(self.Bfactor) + 25))/(2 * math.pi)

    def getAdditionalMetrics(self):

        # calculate some additional per atom density metrics 

        self.rsddensity     = float(self.stddensity)/self.meandensity
        self.rangedensity   = np.linalg.norm(self.maxdensity - self.mindensity)
      
  
class multiPDB(StructurePDB):
    
    # A subclass for a collection of multiple 
    # different dose pdb file structures

    def __init__(self,
                 atomnum            = 0,
                 residuenum         = 0,
                 atomtype           = "",
                 basetype           = "",
                 chaintype          = "",
                 X_coord            = 0,
                 Y_coord            = 0,
                 Z_coord            = 0,
                 Bfactor            = [],
                 Occupancy          = [],
                 meandensity        = [],
                 maxdensity         = [],
                 mindensity         = [],
                 mediandensity      = [],
                 atomID             = "",
                 numsurroundatoms   = 0,
                 numsurroundprotons = 0,
                 bdam               = [],
                 bdamchange         = [],
                 Bfactorchange      = [],
                 meandensity_norm   = [],
                 maxdensity_norm    = [],
                 mindensity_norm    = [],
                 mediandensity_norm = [],
                 numvoxels          = [],
                 stddensity         = [],
                 min90tile          = [],
                 max90tile          = [],
                 min95tile          = [],
                 max95tile          = [],
                 rsddensity         = [],
                 rangedensity       = []):
            
        super(multiPDB, self).__init__(atomnum,
                                       residuenum,
                                       atomtype,
                                       basetype,
                                       chaintype, 
                                       X_coord,
                                       Y_coord, 
                                       Z_coord, 
                                       atomID,
                                       numsurroundatoms,
                                       numsurroundprotons)   
            
        self.Bfactor            = Bfactor 
        self.Occupancy          = Occupancy
        self.meandensity        = meandensity
        self.maxdensity         = maxdensity
        self.mindensity         = mindensity
        self.mediandensity      = mediandensity
        self.bdam               = bdam
        self.bdamchange         = bdamchange
        self.Bfactorchange      = Bfactorchange
        self.meandensity_norm   = meandensity_norm
        self.maxdensity_norm    = maxdensity_norm
        self.mindensity_norm    = mindensity_norm
        self.mediandensity_norm = mediandensity_norm
        self.numvoxels          = numvoxels
        self.stddensity         = stddensity
        self.min90tile          = min90tile
        self.max90tile          = max90tile
        self.min95tile          = min95tile
        self.max95tile          = max95tile
        self.rsddensity         = rsddensity
        self.rangedensity       = rangedensity


class MapInfo:

    # A class for .map file header info
    
    def __init__(self, 
                 nx            = 0, 
                 ny            = 0, 
                 nz            = 0, 
                 mapType       = 0, 
                 start1        = 0, 
                 start2        = 0, 
                 start3        = 0,
                 gridsamp1     = 0, 
                 gridsamp2     = 0, 
                 gridsamp3     = 0, 
                 celldim_a     = 0, 
                 celldim_b     = 0,
                 celldim_c     = 0, 
                 celldim_alpha = 0, 
                 celldim_beta  = 0, 
                 celldim_gamma = 0,
                 fast_axis     = 0, 
                 med_axis      = 0, 
                 slow_axis     = 0, 
                 mindensity    = 0, 
                 maxdensity    = 0,
                 meandensity   = 0,
                 vxls_val      = []):
            
        self.type       = mapType
        self.nxyz       = {'nx' : nx,
                           'ny' : ny,
                           'nz' : nz}
        self.start      = {'1' : start1,
                           '2' : start2,
                           '3' : start3}
        self.gridsamp   = {'1' : gridsamp1,
                           '2' : gridsamp2,
                           '3' : gridsamp3}
        self.celldims   = {'a' : celldim_a,
                           'b' : celldim_b,
                           'c' : celldim_c,
                          'alpha' : celldim_alpha,
                          'beta'  : celldim_beta,
                          'gamma' : celldim_gamma}
        self.axis       = {'fast' : fast_axis,
                           'med'  : med_axis,
                           'slow' : slow_axis}
        self.density    = {'min'  : mindensity,
                           'max'  : maxdensity,
                           'mean' : meandensity}
        self.vxls_val   = vxls_val

    def getnxyzString(self):

        # get string of num columns, rows and sections 

        return self.getParamString(title   = 'Num. Col, Row, Sec',
                                   keys    = ['nx','ny','nz'],
                                   mapAttr = self.nxyz)

    def getStartString(self):
       
        # get string of grid sampling start positions

        return self.getParamString(title   = 'Start positions',
                                   keys    = ['1','2','3'],
                                   mapAttr = self.start)

    def getGridsampString(self):

        # get string of grid sampling dimensions 

        return self.getParamString(title   = 'Grid sampling',
                                   keys    = ['1','2','3'],
                                   mapAttr = self.gridsamp)

    def getCelldimsString(self,
                          tab = False):

        # get string of unit cell dimensions 

        if tab is True:
            n = 1
        else:
            n = 0

        title = 'Cell dimensions'
        s = self.getParamString(title   = title,
                                keys    = ['a','b','c'],
                                mapAttr = self.celldims)
        s += '\n'+'\t'*n+self.getParamString(title   = ' '*len(title),
                                      keys    = ['alpha','beta','gamma'],
                                      mapAttr = self.celldims)
        return s

    def getAxisString(self):

        # get string of grid sampling fast, medium and slow directions

        return self.getParamString(title   = 'Fast,med,slow axes',
                                   keys    = ['fast','med','slow'],
                                   mapAttr = self.axis)

    def getDensityString(self):

        # get string of max, mean and min density values in a map
        # as reported within the map header

        return self.getParamString(title   = 'Values (min, max, mean)',
                                   keys    = ['min','max','mean'],
                                   mapAttr = self.density)

    def getParamString(self,
                       title   = '',
                       keys    = [],
                       mapAttr = ''):

        # formate the density header information into
        # a nice output format to print to command line

        s = title +(40-len(title))*'.'
        for val in keys:
            if isinstance(mapAttr[val],int):
                s += str(mapAttr[val])+' '
            else:
                s += str(round(mapAttr[val],3))+' '
        return s

    def getHeaderInfo(self,
                      tab = False):

        # create a string containing map header information

        if tab is False:
            n = 0
        else:
            n = 1
        s =  '\t'*n+self.getnxyzString() +'\n'+\
             '\t'*n+self.getStartString() +'\n'+\
             '\t'*n+self.getGridsampString() +'\n'+\
             '\t'*n+self.getCelldimsString(tab = True) +'\n'+\
             '\t'*n+self.getAxisString() +'\n'+\
             '\t'*n+self.getDensityString()
        return s



