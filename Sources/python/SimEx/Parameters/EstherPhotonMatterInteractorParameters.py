##########################################################################
#                                                                        #
# Copyright (C) 2016, 2017 Richard Briggs, Carsten Fortmann-Grote        #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

import numpy
import os
import sys
import tempfile
import json

from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters


ESTHER_MATERIAL_DICT = { "Aluminium" : {"name" : "Aluminium",
                       "shortname" : "Al#",
                       "sesame" : "Al#_e_ses",
                       "blf" : "Al#_BLF",
                       "mass_density" : 2.7,
                       },
                       "CH" : {"name" : "CH",
                       "shortname" : "CH2",
                       "sesame" : "CH2_e_ses",
                       "mass_density" : 1.044,
                       },
                       "Diamond" : {"name" : "Diamond",
                       "shortname" : "Dia",
                       "sesame" : "Dia_e_ses",
                       "mass_density" : 3.51,
                       },
                       "Kapton" : {"name" : "Kapton",
                       "shortname" : "Kap",
                       "sesame" : "Kap_e_ses",
                       "mass_density" : 1.42,
                       },
                       "Molybdenum" : {"name" : "Mo",
                       "shortname" : "Mo#",
                       "sesame" : "Mo#_e_ses",
                       "blf" : "Mo#_BLF",
                       "mass_density" : 10.2,
                       },
                       "Gold" : {"name" : "Gold",
                       "shortname" : "Au#",
                       "sesame" : "Au#_e_ses",
                       "blf" : "Au#_BLF",
                       "mass_density" : 19.3,
                       },
                       "Iron" : {"name" : "Iron",
                       "shortname" : "Fe#",
                       "sesame" : "Fe#_e_ses",
                       "blf" : "Fe#_BLF",
                       "mass_density" : 7.85,
                       },
                       "Copper" : {"name" : "Copper",
                       "shortname" : "Cu#",
                       "sesame" : "Cu#_e_ses",
                       "blf" : "Cu#_BLF",
                       "mass_density" : 8.93,
                       },
                       "Tin" : {"name" : "Tin",
                       "shortname" : "Sn#",
                       "sesame" : "Sn#_e_ses",
                       "blf" : "Sn#_BLF",
                       "mass_density" : 7.31,
                       },
                       "LiF" : {"name" : "Lithium Fluoride",
                       "shortname" : "LiF",
                       "sesame" : "LiF_e_ses",
                       "mass_density" : 2.64,
                       },
                       "Titanium" : {"name" : "Titanium",
                       "shortname" : "Ti#",
                       "sesame" : "Ti#_e_ses",
                       "blf" : "Ti#_BLF",
                       "mass_density" : 4.43,
                       },
                       "Berylium" : {"name" : "Berylium",
                       "shortname" : "Be#",
                       "sesame" : "Be#_e_ses",
                       "blf" : "Be#_BLF",
                       "mass_density" : 1.85,
                       },
                       "Cobalt" : {"name" : "Cobalt",
                       "shortname" : "Co#",
                       "sesame" : "Co#_e_ses",
                       "blf" : "Co#_BLF",
                       "mass_density" : 8.9,
                       },
                       "Chromium" : {"name" : "Chromium",
                       "shortname" : "Cr#",
                       "sesame" : "Cr#_e_ses",
                       "blf" : "Cr#_BLF",
                       "mass_density" : 7.19,
                       },
                       "Iron2" : {"name" : "Iron2",
                       "shortname" : "Fe2",
                       "sesame" : "Fe2_e_ses",
                       "mass_density" : 7.87,
                       },
                       "Water" : {"name" : "Water",
                       "shortname" : "H2O",
                       "sesame" : "H20_e_ses",
                       "mass_density" : 1.0,
                       },
                       "Magnesium" : {"name" : "Magnesium",
                       "shortname" : "Mg#",
                       "sesame" : "Mg#_e_ses",
                       "blf" : "Mg#_BLF",
                       "mass_density" : 1.74,
                       },
                       "Mylar" : {"name" : "Mylar",
                       "shortname" : "Myl",
                       "sesame" : "Myl_e_ses",
                       "mass_density" : 1.38,
                       },
                       "Nickel" : {"name" : "Nickel",
                       "shortname" : "Ni#",
                       "sesame" : "Ni#_e_ses",
                       "blf" : "Ni#_BLF",
                       "mass_density" : 8.9,
                       },
                       "Lead" : {"name" : "Lead",
                       "shortname" : "Pb#",
                       "sesame" : "Pb#_e_ses",
                       "blf" : "Pb#_BLF",
                       "mass_density" : 11.35,
                       },
                       "Quartz" : {"name" : "Quartz",
                       "shortname" : "Qua",
                       "sesame" : "Qua_e_ses",
                       "mass_density" : 2.65,
                       },
                       "Silicon" : {"name" : "Silicon",
                       "shortname" : "Si#",
                       "sesame" : "Si#_e_ses",
                       "mass_density" : 2.33,
                       },
                       "SiliconOxide" : {"name" : "SiliconOxide",
                       "shortname" : "SiO",
                       "sesame" : "SiO_e_ses",
                       "mass_density" : 2.65,
                       },
                       "Vanadium" : {"name" : "Vanadium",
                       "shortname" : "V##",
                       "sesame" : "V##_e_ses",
                       "blf" : "V##_BLF",
                       "mass_density" : 6.11,
                       },
                       "Tungsten" : {"name" : "Tungsten",
                       "shortname" : "W##",
                       "sesame" : "W##_e_ses",
                       "blf" : "W##_BLF",
                       "mass_density" : 19.35,
                       },
                       "Silver" : {"name" : "Silver",
                       "shortname" : "Ag#",
                       "sesame" : "Ag#_e_ses",
                       "blf" : "Ag#_BLF",
                       "mass_density" : 10.5,
                       },
           }

class EstherPhotonMatterInteractorParameters(AbstractCalculatorParameters):
    """
    class representing parameters for the Hydrocode Input Calculator
    """
    def __init__(self,
                 number_of_layers=None,
                 ablator=None,
                 ablator_thickness=None,
                 sample=None,
                 sample_thickness=None,
                 layer1=None,
                 layer1_thickness=None,
                 layer2=None,
                 layer2_thickness=None,
                 window=None,
                 window_thickness=None,
                 laser_wavelength=None,
                 laser_pulse=None,
                 laser_pulse_duration=None,
                 laser_intensity=None,
                 run_time=None,
                 delta_time=None,
                 read_from_file=None,
                 without_therm_conduc=None,
                 rad_transfer=None,
                 sample_eos_type=None,
                 number_of_zones=None,
                 feather_zone_width=None,
                 minimum_zone_width=None,
                 ):

        """
        Constructor for the HydroParameters

        :param ablator: The ablating material ( "Al" | "CH" | "Diamond" | "Kapton" | "Mylar" )
        :type ablator: str

        :param ablator_thickness: The ablator thickness (micrometers)
        :type ablator_thickness:

        :param sample: The sample material (from list of materials)
        :type sample: str

        :param sample_thickness: The sample thickness (micrometers)
        :type sample_thickness: float

        :param layer1: The layer1 material (from list of materials)
        :type layer1: str

        :param layer2: The layer2 material (from list of materials)
        :type layer2: str

        :param window: The window material (LiF | SiO2 | Diamond)
        :type window: str

        :param window_thickness: The window thickness, if using window (micrometers)
        :type window_thickness: float

        :param laser_pulse: Pulse type ("flat" | "ramp" | "other")
        :type laser_pulse: str

        :param laser_pulse_duration: Pulse duration of the pump laser (ns)
        :type laser_pulse_duration: float

        :param laser_wavelength: Laser wavelength (nm)
        :type laser_wavelength: float

        :param laser_intensity: Laser intensity (TW/cm2)
        :type laser_intensity: float

        :param run_time: Simulation run time (ns)
        :type run_time: float

        :param delta_time: Time steps resolution (ns)
        :type delta_time: float

        :param force_passage: Expert option to force passage of simulation through minor errors
        :type force_passage: boolean

        :param without_therm_conduc: Expert option to use without thermal conductivity options
        :type without_therm_conduc: boolean

        :param rad_transfer: Expert option to use radiative transfer
        :type rad_transfer: boolean
        
        :param sample_eos_type: Choice of EOS, default = sesame, some elements can use blf.
        :type sample_eos_type: str
        
        :param number_of_zones: Expert options, number of zones for mesh (spatial resolution)
        :type number_of_zones: int
        
        :param feather_zone_width: Width of the feathered zone
        :type feather_zone_width: float
        
        :param minimum_zone_width: Minimum width of feathered zone towards laser
        :type minimum_zone_width: float

        """

        # If parameters already exist, read from parameters file
        if read_from_file is not None:
            print ( "Parameters file is located here: %s" % (read_from_file))
            self._readParametersFromFile(read_from_file)

            # Update parameters from arguments.
            for key,val in {
                    'number_of_layers':number_of_layers,
                    'ablator':ablator,
                    'ablator_thickness':ablator_thickness,
                    'sample':sample,
                    'sample_thickness':sample_thickness,
                    'layer1':layer1,
                    'layer1_thickness':layer1_thickness,
                    'layer2':layer2,
                    'layer2_thickness':layer2_thickness,
                    'window':window,
                    'window_thickness':window_thickness,
                    'laser_wavelength':laser_wavelength,
                    'laser_pulse':laser_pulse,
                    'laser_pulse_duration':laser_pulse_duration,
                    'laser_intensity':laser_intensity,
                    'run_time':run_time,
                    'delta_time':delta_time,
                    'sample_eos_type':sample_eos_type,
                    'without_therm_conduc':without_therm_conduc,
                    'rad_transfer':rad_transfer,
                    'number_of_zones':number_of_zones,
                    'feather_zone_width':feather_zone_width,
                    'minimum_zone_width':minimum_zone_width
                    }.items():
                if val is not None:
                    setattr(self, key, val)
        else:
            # Check and set all parameters
            self.__number_of_layers = checkAndSetNumberOfLayers(number_of_layers)
            self.__ablator = checkAndSetAblator(ablator)
            self.__ablator_thickness = checkAndSetAblatorThickness(ablator_thickness)
            self.__sample = checkAndSetSample(sample)
            self.__sample_thickness = checkAndSetSampleThickness(sample_thickness)
            self.__layer1 = checkAndSetLayer1(layer1)
            self.__layer1_thickness = checkAndSetLayer1Thickness(layer1_thickness)
            self.__layer2 = checkAndSetLayer2(layer2)
            self.__layer2_thickness = checkAndSetLayer2Thickness(layer2_thickness)
            self.__window = checkAndSetWindow(window)
            self.__window_thickness = checkAndSetWindowThickness(window_thickness)
            self.__laser_wavelength = checkAndSetLaserWavelength(laser_wavelength)
            self.__laser_pulse = checkAndSetLaserPulse(laser_pulse)
            self.__laser_pulse_duration = checkAndSetLaserPulseDuration(laser_pulse_duration)
            self.__laser_intensity = checkAndSetLaserIntensity(laser_intensity)
            self.__run_time = checkAndSetRunTime(run_time)
            self.__delta_time = checkAndSetDeltaTime(delta_time)
            self.__sample_eos_type = checkAndSetSampleEosType(sample_eos_type)
            self.without_therm_conduc = without_therm_conduc # NEEDS CHECK AND SET / CONSISTENCY
            self.rad_transfer = rad_transfer # NEEDS CHECK AND SET / CONSISTENCY
            self.__number_of_zones = checkAndSetNumberOfZones(number_of_zones)
            self.__feather_zone_width = checkAndSetFeatherZoneWidth(feather_zone_width)
            self.__minimum_zone_width = checkAndSetMinimumZoneWidth(minimum_zone_width)
        
        # Check possible conflicts of checkAndSet functions
        self.checkConsistency()

        # Define start up options (called Demmarage in esther)
        self._setDemmargeFlags()

        # Expert mode: Setup zone feathering (spatial resolution)
        self._setupFeathering()

        # Set state to not-initialized (e.g. input deck is not written)
        self.__is_initialized = False

    def _readParametersFromFile(self,path):
        # Read from parameters file
        json_path = os.path.join(path, 'parameters.json')
        print ( "Parameters file is: %s" % (json_path))
        with open(json_path, 'r') as j:
            dictionary = json.load(j)
            j.close()

        self.__dict__ = dictionary

    def _setDemmargeFlags(self):
        # Expert users options to include in the start up options
        self.__use_usi = "USI" # Use SI units.
        
        # These two are now in the parameters as without_therm_conduc and rad_transfer...
        self.__use_without_therm_conduc = "SANS_COND_THERMIQUE" # Run without thermal conducivity
        self.__use_radiative_transfer = "TRANSFERT_RADIATIF" # Run with radiative transfer

    def _setupFeathering(self, number_of_zones, feather_zone_width, minimum_zone_width):
        """ Method to fix feathering

        :param number_of_zones: The number of zones in the first ablator section (default 250).
        :type number_of_zones: int

        :param feather_zone_width: Width of feather zone (default 4.0 [microns]).
        :type feather_zone_width: float

        :param minimum_zone_width: Minimal zone width (default 4e-4 [microns]).
        :type minimum_zone_width: float

        """
        # Determine the correct zone feathering for ablator
        n = number_of_zones
        feather_list=numpy.zeros(n+1) # Create list of n zones
        feather_list[0]=1. # First zone is 1
        feather_list[-2]=-feather_zone_width/minimum_zone_width
        feather_list[-1]=-feather_list[-2] - 1.

        # Find roots in polynomial over the feather list
        f = numpy.poly1d(feather_list)
        roots = numpy.roots(f)
        root_found = False

        # Get all purely real roots above 1.
        for i in range(n):
            if roots[i].imag == 0 and roots[i].real > 1.000001: # Why not > 1.? This would exclude 1.0f
                r = round(roots[i].real,4)
                root_found = True

        if root_found == False:
            raise RuntimeError( "No ratio bigger than 1.000001 was found.")

        # Store feather information on object.
        self._feather_zone_width = feather_zone_width
        self._minimum_zone_width = minimum_zone_width
        self._final_feather_zone_width = round(minimum_zone_width*(r**n),4)
        self._non_feather_zone_width = self.ablator_thickness-feather_zone_width
        self._non_feather_zones = int(self._non_feather_zone_width/(minimum_zone_width*(r**n)))


        self._mass_of_zone = self._final_feather_zone_width*ESTHER_MATERIAL_DICT[self.ablator]["mass_density"]
        width_of_sample_zone = self._mass_of_zone/ESTHER_MATERIAL_DICT[self.sample]["mass_density"]
        self.__number_of_sample_zones=int(self.sample_thickness/width_of_sample_zone)

        print ("Final feather zone width: ", self._final_feather_zone_width)
        print ("Mass of zone: ", self._mass_of_zone)
        print ("Number of non-feathered zones: ", self._non_feather_zones)

        if self.layer1 is not None:
            width_of_layer1_zone = self._mass_of_zone/ESTHER_MATERIAL_DICT[self.layer1]["mass_density"]
            self.__number_of_layer1_zones=int(self.layer1_thickness/width_of_layer1_zone)

        if self.layer2 is not None:
            width_of_layer2_zone = self._mass_of_zone/ESTHER_MATERIAL_DICT[self.layer2]["mass_density"]
            self.__number_of_layer2_zones=int(self.layer2_thickness/width_of_layer2_zone)

        if self.window is not None:
            width_of_window_zone = self._mass_of_zone/ESTHER_MATERIAL_DICT[self.window]["mass_density"]
            self.__number_of_window_zones=int(self.window_thickness/width_of_window_zone)

    def _serialize(self, path=None, filename=None):
        """ Write the input deck for the Esther hydrocode. """

        # Make a temporary directory or use existing path and filename
        self._esther_files_path = path
        self._esther_filename = filename
        if path is None:
            self._esther_files_path = tempfile.mkdtemp(prefix='esther_')
        if filename is None:
            self._esther_filename='tmp_input'

        # Write the input file
        input_deck_path = os.path.join( self._esther_files_path, self._esther_filename+'.txt')
        print ("Writing input deck to ", input_deck_path, ".")

        # Write json file of this parameter class instance.
        json_path = os.path.join( self._esther_files_path, 'parameters.json')
        print ("Writing parameters file to ", json_path, ".")
        with open( json_path, 'w') as j:
            json.dump( self.__dict__, j)
            j.close()

        # Write the file.
        with open(input_deck_path, 'w') as input_deck:
            input_deck.write('DEMARRAGE,%s\n' % (self.__use_usi))

            if self.without_therm_conduc is True:
                input_deck.write('%s\n' % (self.__use_without_therm_conduc)) # Use without thermal conductivity option

            if self.rad_transfer is True:
                input_deck.write('%s\n' % (self.__use_radiative_transfer)) # Use without thermal conductivity option

            input_deck.write('\n')
            input_deck.write('MILIEUX_INT_VERS_EXT\n')
            input_deck.write('\n')

            # If using a window, write the window layer here
            if self.window is not None:
                input_deck.write('- %.1f um %s layer\n' % (self.window_thickness, self.window))
                input_deck.write('NOM_MILIEU=%s\n' % (ESTHER_MATERIAL_DICT[self.window]["shortname"]))
                # Window EOS set to default of SESAME; Add window_eos_choice if other eos become available.
                input_deck.write('EQUATION_ETAT=%s\n' % (ESTHER_MATERIAL_DICT[self.window]["sesame"]))
                input_deck.write('EPAISSEUR_VIDE=100e-6\n')
                input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self.window_thickness))
                # Calculate number of zones in window
                input_deck.write('NOMBRE_MAILLES=%d\n' % (self.__number_of_window_zones))
                input_deck.write('MECANIQUE_RAM\n')
                input_deck.write('\n')

            # If using 4 layers (ablator, layer1, sample, layer2) write layer 2
            if self.number_of_layers == 4:
                input_deck.write('- %.1f um %s layer\n' % (self.layer2_thickness, self.layer2))
                input_deck.write('NOM_MILIEU=%s_2\n' % (ESTHER_MATERIAL_DICT[self.layer2]["shortname"]))
                # Layer 2 EOS set to default value of SESAME; Add layer2_eos_type if other EOS choices wanted.
                input_deck.write('EQUATION_ETAT=%s\n' % (ESTHER_MATERIAL_DICT[self.layer2]["sesame"]))
                if self.window is None:
                    input_deck.write('EPAISSEUR_VIDE=100e-6\n')
                input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self.layer2_thickness))
                # Calculate number of zones
                input_deck.write('NOMBRE_MAILLES=%d\n' % (self.__number_of_layer2_zones))
                input_deck.write('MECANIQUE_RAM\n')
                input_deck.write('\n')
            
            # Write sample layer
            input_deck.write('- %.1f um %s layer\n' % (self.sample_thickness, self.sample))
            input_deck.write('NOM_MILIEU=%s_2\n' % (ESTHER_MATERIAL_DICT[self.sample]["shortname"]))
            input_deck.write('EQUATION_ETAT=%s\n' % (ESTHER_MATERIAL_DICT[self.sample][self.sample_eos_type]))
            if self.number_of_layers == 3: # Add empty space if number of layers = 3 (abl, lay1, sample)
                if self.window is None: # But only if there is no window.
                    input_deck.write('EPAISSEUR_VIDE=100e-6\n')
            elif self.number_of_layers == 2: # Add empty space if number of layers = 2 (abl, sample)
                if self.window is None: # But only if there is no window.
                    input_deck.write('EPAISSEUR_VIDE=100e-6\n')
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self.sample_thickness))
            # Calculate number of zones
            input_deck.write('NOMBRE_MAILLES=%d\n' % (self.__number_of_sample_zones))
            input_deck.write('MECANIQUE_RAM\n')
            input_deck.write('\n')

            # If using 3 layers (ablator, layer1, sample) write layer 1
            if self.number_of_layers == 3:
                input_deck.write('- %.1f um %s layer\n' % (self.layer1_thickness, self.layer1))
                input_deck.write('NOM_MILIEU=%s_2\n' % (ESTHER_MATERIAL_DICT[self.layer1]["shortname"]))
                # Layer1 EOS set to default value of SESAME: Add layer1_eos_type if other EOS choices wanted.
                input_deck.write('EQUATION_ETAT=%s\n' % (ESTHER_MATERIAL_DICT[self.layer1]["sesame"]))
                # Calculate number of zones
                input_deck.write('NOMBRE_MAILLES=%d\n' % (self.__number_of_layer1_zones))
                input_deck.write('MECANIQUE_RAM\n')
                input_deck.write('\n')

            # Write ablator layer
            input_deck.write('- %.1f um %s layer\n' % (self.ablator_thickness, self.ablator))
            input_deck.write('NOM_MILIEU=%s_abl1\n' % (ESTHER_MATERIAL_DICT[self.ablator]["shortname"])) # 1st PART OF ABLATOR
            # Ablator EOS default to sesame (not many ablators have blf); Add ablator_eos_type if wanted.
            input_deck.write('EQUATION_ETAT=%s\n' % (ESTHER_MATERIAL_DICT[self.ablator]["sesame"]))
            # if only simulating ablator layer, then must include empty (VIDE) layer
            if self.number_of_layers == 1:
                input_deck.write('EPAISSEUR_VIDE=100e-6\n')
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self._non_feather_zone_width)) # Non-feather thickness
            input_deck.write('NOMBRE_MAILLES=%d\n' % (self._non_feather_zones)) # Number of zones
            input_deck.write('MECANIQUE_RAM\n') # Needs to be an option to use this.
            input_deck.write('\n')

            input_deck.write('NOM_MILIEU=%s_abl2\n' % (ESTHER_MATERIAL_DICT[self.ablator]["shortname"])) # 2nd PART OF ABLATOR
            # Ablator EOS default to sesame (not many ablators have blf); Add ablator_eos_type if wanted.
            input_deck.write('EQUATION_ETAT=%s\n' % (ESTHER_MATERIAL_DICT[self.ablator]["sesame"])) # ABLATOR EOS
            input_deck.write('EPAISSEUR_MILIEU=%.1fe-6\n' % (self._feather_zone_width)) # Feather thickness
            input_deck.write('EPAISSEUR_INTERNE=%.3fe-6\n' % (self._final_feather_zone_width)) # Feather final zone width
            input_deck.write('EPAISSEUR_EXTERNE=4.0e-10\n') #Min zone width
            input_deck.write('MECANIQUE_RAM\n') # Needs to be an option to use this.
            input_deck.write('\n')

            # Adjust refractive index for appropriate ablator
            if self.ablator is "CH":
                input_deck.write('INDICE_REEL_LASER=1.46\n')
            elif self.ablator is "Al":
                input_deck.write('INDICE_REEL_LASER=1.197\n')
            elif self.ablator is "Dia":
                input_deck.write('INDICE_REEL_LASER=2.39\n')
            elif self.ablator is "Myl":
                input_deck.write('INDICE_REEL_LASER=1.65\n')
            elif self.ablator is "Kapton":
                input_deck.write('INDICE_REEL_LASER=1.7\n')
            else:
                # Use generic refractive index for typical ablators
                input_deck.write('INDICE_REEL_LASER=1.6\n')
            input_deck.write('INDICE_IMAG_LASER=1.0\n')
            input_deck.write('\n')

            # Laser parameters
            input_deck.write('DEPOT_ENERGIE,LASER,DEPOT_HELMHOLTZ\n') # Expert mode option
            input_deck.write('LONGUEUR_ONDE_LASER=%.3fe-6\n' % (self.laser_wavelength))
            input_deck.write('DUREE_IMPULSION=%.2fe-9\n' % (self.laser_pulse_duration))
            input_deck.write('INTENSITE_IMPUL_MAX=%.3fe16\n' % (self.laser_intensity))
            if self.laser_pulse is "flat":        
                input_deck.write('TEMPS_IMPUL_TABULE=0.0e-9,INTENSITE_TABULEE=0.0\n') # These need to change for approrpriate laser designs.
                input_deck.write('TEMPS_IMPUL_TABULE=0.2e-9,INTENSITE_TABULEE=1.0\n')
                input_deck.write('TEMPS_IMPUL_TABULE=%.1fe-9,INTENSITE_TABULEE=1.0\n'% (self.laser_pulse_duration-0.2))
                input_deck.write('TEMPS_IMPUL_TABULE=%.1fe-9,INTENSITE_TABULEE=0.0\n' % (self.laser_pulse_duration))
            elif self.laser_pulse is "quasiflat":
                input_deck.write('TEMPS_IMPUL_TABULE=0.0e-9,INTENSITE_TABULEE=0.0\n') # These need to change for approrpriate laser designs.
                input_deck.write('TEMPS_IMPUL_TABULE=0.2e-9,INTENSITE_TABULEE=0.8\n')
                input_deck.write('TEMPS_IMPUL_TABULE=%.1fe-9,INTENSITE_TABULEE=1.0\n'% (self.laser_pulse_duration-0.2))
                input_deck.write('TEMPS_IMPUL_TABULE=%.1fe-9,INTENSITE_TABULEE=0.0\n' % (self.laser_pulse_duration))
            elif self.laser_pulse is "ramp":
                x = numpy.arange(0.,self.laser_pulse_duration+1.0,1)
                y = x**3
                y = y/numpy.amax(y)
                Number_lines = len(x)
                x[Number_lines-1]=self.laser_pulse_duration-0.1 # Set the max intensity at 100 ps before final pulse time
                for i in range(0,Number_lines):
                    input_deck.write('TEMPS_IMPUL_TABULE=%.1fe-9,INTENSITE_TABULEE=%0.3f\n' % (x[i],y[i]))
                input_deck.write('TEMPS_IMPUL_TABULE=%.1fe-9,INTENSITE_TABULEE=0.0\n' % (self.laser_pulse_duration))
            else:
                raise RuntimeError("Laser pulse type has not been chosen")
            input_deck.write('\n')

            # Output parameters
            input_deck.write('SORTIES_GRAPHIQUES\n')
            input_deck.write('DECOUPAGE_TEMPS\n')
            input_deck.write('BORNE_TEMPS=%.2fe-9\n' % (self.run_time))
            input_deck.write('INCREMENT_TEMPS=%.2fe-9\n' % (self.delta_time))
            input_deck.write('\n')

            # End of input file
            input_deck.write('ARRET\n')
            input_deck.write('TEMPS_ARRET=%.2fe-9\n' % (self.run_time))
            input_deck.write('\n')
            input_deck.write('FIN_DES_INSTRUCTIONS')

        # Write the laser input file
        laser_input_deck_path = os.path.join( self._esther_files_path, self._esther_filename+'_intensite_impulsion.txt')
        print ("Writing laser input deck to ", laser_input_deck_path, ".")

        # Write the parameters file (_intensitie_impulsion)
        with open(laser_input_deck_path, 'w') as laser_input_deck:
            if self.laser_pulse == "flat":
                # Write flat top pulse shape to file
                laser_input_deck.write('4\n')
                laser_input_deck.write('temps (s ou u.a.) intensite (W/m2 ou u.a.)\n')
                laser_input_deck.write('0. \t 0\n')
                laser_input_deck.write('0.1e-9\t%.3f\n' % (self.laser_intensity))
                laser_input_deck.write('%.1fe-9\t%.3f\n' % (self.laser_pulse_duration-0.2, self.laser_intensity))
                laser_input_deck.write('%.1fe-9\t0.0\n' % (self.laser_pulse_duration))
                laser_input_deck.write('fin_de_fichier')
            elif self.laser_pulse == "quasiflat":
                laser_input_deck.write('4\n')
                laser_input_deck.write('temps (s ou u.a.) intensite (W/m2 ou u.a.)\n')
                laser_input_deck.write('0. \t 0\n')
                laser_input_deck.write('0.1e-9\t%.3f\n' % (0.8*self.laser_intensity))
                laser_input_deck.write('%.1fe-9\t%.3f\n' % (self.laser_pulse_duration-0.2, self.laser_intensity))
                laser_input_deck.write('%.1fe-9\t0.0\n' % (self.laser_pulse_duration))
                laser_input_deck.write('fin_de_fichier')
            elif self.laser_pulse == "ramp":
                # Write ramp pulse shape to file
                x = numpy.arange(0.,self.laser_pulse_duration+1.0,1)
                y = x**3
                y = y/numpy.amax(y)
                Number_lines = len(x)
                x[Number_lines-1]=self.laser_pulse_duration-0.1 # Set the max intensity at 100 ps before final pulse time
                laser_input_deck.write('%d\n' % (Number_lines+1)) # Number of lines to add in pulse shape
                laser_input_deck.write('temps (s ou u.a.) intensite (W/m2 ou u.a.)\n')
                for i in range(0,Number_lines):
                    laser_input_deck.write('%.2fe-9\t%0.3f\n' % (x[i],y[i]*self.laser_intensity))
                laser_input_deck.write('%.2fe-9\t0.0\n' % (self.laser_pulse_duration))
                laser_input_deck.write('fin_de_fichier')
            else:
                # Use a default Gaussian? or quit?
                # TO DO: GIT ISSUE #96: Expert mode: User defined pulse shape?
                print ("No default laser chosen?")

    @property
    def number_of_layers(self):
           """ Query for the number of layers. """
           return self.__number_of_layers
    @number_of_layers.setter
    def number_of_layers(self, value):
           """ Set the number of layers to the value. """
           self.__number_of_layers = checkAndSetNumberOfLayers(value)

    @property
    def ablator(self):
           """ Query for the ablator type. """
           return self.__ablator
    @ablator.setter
    def ablator(self, value):
           """ Set the ablator to the value. """
           self.__ablator = checkAndSetAblator(value)

    @property
    def ablator_thickness(self):
           """ Query for the ablator thickness. """
           return self.__ablator_thickness
    @ablator_thickness.setter
    def ablator_thickness(self, value):
           """ Set the ablator thickness to the value. """
           self.__ablator_thickness = checkAndSetAblatorThickness(value)

    @property
    def sample(self):
           """ Query for the sample type. """
           return self.__sample
    @sample.setter
    def sample(self, value):
           """ Set the sample type to the value. """
           self.__sample = checkAndSetSample(value)

    @property
    def sample_thickness(self):
           """ Query for the sample thickness type. """
           return self.__sample_thickness
    @sample_thickness.setter
    def sample_thickness(self, value):
           """ Set the sample thickness to the value. """
           self.__sample_thickness = checkAndSetSampleThickness(value)

    @property
    def layer1(self):
           """ Query for the layer1 type. """
           return self.__layer1
    @layer1.setter
    def layer1(self, value):
           """ Set the layer1 type to the value. """
           self.__layer1 = checkAndSetLayer1(value)

    @property
    def layer1_thickness(self):
           """ Query for the layer1 thickness type. """
           return self.__layer1_thickness
    @layer1_thickness.setter
    def layer1_thickness(self, value):
           """ Set the layer1 thickness to the value. """
           self.__layer1_thickness = checkAndSetLayer1Thickness(value)

    @property
    def layer2(self):
           """ Query for the layer2 type. """
           return self.__layer2
    @layer2.setter
    def layer2(self, value):
           """ Set the layer2 type to the value. """
           self.__layer2 = checkAndSetLayer2(value)

    @property
    def layer2_thickness(self):
           """ Query for the layer2 thickness type. """
           return self.__layer2_thickness
    @layer2_thickness.setter
    def layer2_thickness(self, value):
           """ Set the layer2 thickness to the value. """
           self.__layer2_thickness = checkAndSetLayer2Thickness(value)

    @property
    def window(self):
           """ Query for the window type. """
           return self.__window
    @window.setter
    def window(self, value):
           """ Set the window to the value. """
           self.__window = checkAndSetWindow(value)

    @property
    def window_thickness(self):
           """ Query for the window thickness type. """
           return self.__window_thickness
    @window_thickness.setter
    def window_thickness(self, value):
           """ Set the window thickness to the value. """
           self.__window_thickness = checkAndSetWindowThickness(value)

    @property
    def laser_wavelength(self):
           """ Query for the laser wavelength type. """
           return self.__laser_wavelength
    @laser_wavelength.setter
    def laser_wavelength(self, value):
           """ Set the laser wavelength to the value. """
           self.__laser_wavelength = checkAndSetLaserWavelength(value)

    @property
    def laser_pulse(self):
        """Query for laser pulse type"""
        return self.__laser_pulse
    @laser_pulse.setter
    def laser_pulse(self,value):
        """ Set the laser pulse to type value """
        self.__laser_pulse = checkAndSetLaserPulse(value)

    @property
    def laser_pulse_duration(self):
        """ Query for laser pulse duration """
        return self.__laser_pulse_duration
    @laser_pulse_duration.setter
    def laser_pulse_duration(self,value):
        """ Set laser pulse duration """
        self.__laser_pulse_duration = checkAndSetLaserPulseDuration(value)

    @property
    def laser_intensity(self):
        """ Query for laser intensity """
        return self.__laser_intensity
    @laser_intensity.setter
    def laser_intensity(self,value):
        """ Set laser intensity """
        self.__laser_intensity = checkAndSetLaserIntensity(value)

    @property
    def run_time(self):
        """ Query for simulation run time """
        return self.__run_time
    @run_time.setter
    def run_time(self,value):
        """ Set simulation run time """
        self.__run_time = checkAndSetRunTime(value)

    @property
    def delta_time(self):
        """ Query for simulation time resolution (delta t ns) """
        return self.__delta_time
    @delta_time.setter
    def delta_time(self,value):
        """ Set simulation time resolution delta t, ns"""
        self.__delta_time = checkAndSetDeltaTime(value)

    @property
    def sample_eos_type(self):
        """ Query for sample_eos_type (sesame or blf) """
        return self.__sample_eos_type
    @sample_eos_type.setter
    def sample_eos_type(self,value):
        """ Set sample_eos_type"""
        self.__sample_eos_type = checkAndSetSampleEosType(value)
    
    @property
    def number_of_zones(self):
        """ Query for number of zones in mesh """
        return self.__number_of_zones
    @number_of_zones.setter
    def number_of_zones(self,value):
        """ Set number of zones """
        self.__number_of_zones = checkAndSetNumberOfZones(value)
    
    @property
    def feather_zone_width(self):
        """ Query for feather zone width in mesh """
        return self.__feather_zone_width
    @feather_zone_width.setter
    def feather_zone_width(self,value):
        """ Set number of zones """
        self.__feather_zone_width = checkAndSetFeatherZoneWidth(value)
    
    @property
    def minimum_zone_width(self):
        """ Query for minimum zone width """
        return self.__minimum_zone_width
    @minimum_zone_width.setter
    def minimum_zone_width(self,value):
        """ Set minimum zone width """
        self.__minimum_zone_width = checkAndSetMinimumZoneWidth(value)
    
    def _setDefaults(self):
        """ Method to pick sensible defaults for all parameters. """
        pass

    def checkConsistency(self):
        if self.window is not None:
            if self.window_thickness == 0.0:
                raise ValueError( "Window thickness cannot be 0.0")
        
        # If BLF choice, check if the sample actually has a blf eos.
        if self.sample_eos_type is "blf":
            blf_elements = [ "Aluminium", "Gold", "Cobalt", "Copper",
                    "Iron", "Molybdenum", "Nickel", "Lead", "Tin",
                    "Berylium", "Chromium", "Magnesium",
                    "Silver", "Titanium", "Vanadium", "Tungsten" ]
            if self.sample in blf_elements:
                pass
            else:
                raise RuntimeError("Sample does not have blf EOS... set sample_eos_type to None for default eos")

###########################
# Check and set functions #
###########################

#################################
# Ablator, layers and sample set functions
##################################

def checkAndSetNumberOfLayers(number_of_layers):
    """
    Utility to check if the number of layers is reasonable.

    :param number_of_layers: The number of layers to check
    :return: Checked number of layers
    :raise ValueError: not (1 < number_of_layers <= 4 )

    """
    if number_of_layers is None:
        raise RuntimeError( "Number of layers is not defined.")

    if not isinstance( number_of_layers, int ):
        raise TypeError("The parameter 'number_of_layers' must be an int.")

    if number_of_layers <1 or number_of_layers > 4:
        raise ValueError( "Number of layers must be between 1 and 4 only.")

    return number_of_layers

def checkAndSetAblator(ablator):
    """
    Utility to check if the ablator exists in the EOS database.

    :param ablator: The ablator material to check.
    :return: The ablator choice after being checked.
    :raise ValueError: ablator not in ["CH", "Al", "Diamond", "Mylar", "Kapton"].
    
    If new ablators are added, the refractive index must be updated in the _serialize function
    to account for the new material, otherwise a default value of 1.6 is used.

    """

    if ablator is None:
        raise RuntimeError( "The parameter 'ablator' is not defined.")

    # Check type.
    if not isinstance( ablator, str):
        raise TypeError("The parameters 'ablator' must be a str.")

    ### Could check if isinstance(ablator, str)
    if ablator == 'CH':
        print ( "Setting CH as ablator.")
    elif ablator.lower() in ['al', 'aluminium']:
        print ( "Setting Al as ablator.")
    elif ablator.lower() in ['dia', 'diamond']:
        print ( "Setting diamond as ablator.")
    elif ablator.lower() in ['mylar', 'myl']:
        print ( "Setting mylar as ablator.")
    elif ablator.lower() in ['kap', 'kapton']:
        print ( "Setting Kapton as ablator.")
    else:
        raise ValueError( "Ablator is not valid. Use 'CH', 'Al', 'dia', 'Myl', or 'Kap' as ablator.")

    return ablator

def checkAndSetAblatorThickness(ablator_thickness):
    """
    Utility to check that the ablator thickness is > 5 um and < 100 um
    """

    # Raise if not set.
    if ablator_thickness is None:
        raise RuntimeError( "Ablator thickness not specified.")

    # Check type.
    if not isinstance( ablator_thickness, (int, float)):
        raise TypeError("The parameters 'ablator_thickness' must be of numeric type (int or float).")

    # Check if ablator is between 5 and 100 um
    if ablator_thickness < 5.0 or ablator_thickness > 100.0:
        raise ValueError( "Ablator must be between 5.0 and 100.0 microns")

    # TO DO PLACEHOLDER
    # IF LASER INTENSITY IS TOO HIGH, ABLATOR MUST BE THICK TO ALLOW FOR ENOUGH MATERIAL TO VAPORISE (CH)

    print ( "Ablator thickness is %4.1f " % ablator_thickness)

    return ablator_thickness

def checkAndSetSample(sample):
    """
    Utility to check if the sample is in the list of known EOS materials
    """

    elements = [ "Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
                "Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum",
                "Berylium", "Chromium", "Iron2", "Kapton", "LiF", "Magnesium", "Mylar",
                "Quartz", "SiliconOxide", "Silver", "Titanium", "Vanadium", "Water", "Tungsten" ]

    # Set default
    if sample is None:
        raise RuntimeError( "sample not specified.")

    if not isinstance(sample, str): raise TypeError("The parameter 'sample' must be a str.")

    # Check each element
    if sample in elements:
        pass
    else:
        raise ValueError( "sample is not in list of known EOS materials")

    return sample

def checkAndSetSampleThickness(sample_thickness):
    """
    Utility to check that the sample thickness is in permitted range set by Esther.
    """

    # Raise if not set.
    if sample_thickness is None:
        raise RuntimeError( "Sample thickness not specified.")

    # Check type.
    if not isinstance( sample_thickness, (int, float)):
        raise TypeError("The parameters 'sample_thickness' must be of numeric type (int or float).")

    # Check if sample is between 1 and 200 um
    if sample_thickness < 1.0 or sample_thickness > 200.0:
        raise ValueError( "Ablator must be between 1.0 and 200.0 microns")

    return sample_thickness

def checkAndSetLayer1(layer1):
    """
    Utility to check if the layer1 is in the list of known EOS materials
    """

    elements = [ "Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
                "Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum",
                "Berylium", "Chromium", "Iron2", "Kapton", "LiF", "Magnesium", "Mylar",
                "Quartz", "SiliconOxide", "Silver", "Titanium", "Vanadium", "Water", "Tungsten" ]

    # Set default
    if layer1 is None:
        print ( "Running simulation without layer1 material")
        return None

    if not isinstance(layer1, str): raise TypeError("The parameter 'layer1' must be a str.")

    # Check each element
    if layer1 in elements:
        pass
    else:
        raise ValueError( "layer1 is not in list of known EOS materials")

    return layer1

def checkAndSetLayer1Thickness(layer1_thickness):
    """
    Utility to check that the layer1 thickness is in permitted range set by Esther.
    """

    # Set default
    if layer1_thickness is None:
        return 0.0

    # Check if number.
    if not isinstance( layer1_thickness, (float, int)):
        raise TypeError( "The parameter 'layer1_thickness' must be a numerical type (float or int.)")

    # Check if layer1 is between 1 and 100 um
    if layer1_thickness < 1.0 or layer1_thickness > 200.0:
        raise ValueError( "layer1 must be between 1.0 and 200.0 microns")

    return layer1_thickness

def checkAndSetLayer2(layer2):
    """
    Utility to check if the layer2 is in the list of known EOS materials
    """

    elements = [ "Aluminium", "Gold", "Carbon", "CH", "Cobalt", "Copper", "Diamond",
                "Iron", "Molybdenum", "Nickel", "Lead", "Silicon", "Tin", "Tantalum",
                "Berylium", "Chromium", "Iron2", "Kapton", "LiF", "Magnesium", "Mylar",
                "Quartz", "SiliconOxide", "Silver", "Titanium", "Vanadium", "Water" ]

    # Set default
    if layer2 is None:
        print ( "Running simulation without layer2 material")
        return None

    if not isinstance(layer2, str): raise TypeError("The parameter 'layer2' must be a str.")

    # Check each element
    if layer2 in elements:
        pass
    else:
        raise ValueError( "layer2 is not in list of known EOS materials")

    return layer2

def checkAndSetLayer2Thickness(layer2_thickness):
    """
    Utility to check that the layer2 thickness is in permitted range set by Esther.
    """

    # Set default
    if layer2_thickness is None:
        return 0.0

    # Check if number.
    if not isinstance( layer2_thickness, (float, int)):
        raise TypeError( "The parameter 'layer2_thickness' must be a numerical type (float or int.)")

    # Check if layer2 is between 1 and 100 um
    if layer2_thickness < 1.0 or layer2_thickness > 200.0:
        raise ValueError( "layer2 must be between 1.0 and 200.0 microns")

    return layer2_thickness

def checkAndSetWindow(window):
    """
    Utility to check that the window exists in the EOS database.
    """

    elements = ["LiF", "SiO2", "Diamond", "Quartz" ]

    if window is None:
        print ( "Running simulation without window material")
        return None

    if not isinstance( window, str):
        raise TypeError("The parameter 'window' must be a str.")

    # Check each element
    if window not in elements:
        raise ValueError( "window is not in list of known EOS materials")

    return window

def checkAndSetWindowThickness(window_thickness):
    """
    Utility to check that the window thickness is > 1 um and < 500 um
    """

    # Set default
    if window_thickness is None:
        return 0.0

    # Check if number.
    if not isinstance( window_thickness, (float, int)):
        raise TypeError( "The parameter 'window_thickness' must be a numerical type (float or int.)")

    # Check if ablator is between 1 and 100 um
    if window_thickness == 0.0:
        pass
    elif window_thickness < 1.0 or window_thickness > 500.0:
        raise ValueError( "Window must be between 1.0 and 500.0 microns")

    return window_thickness

#################################
# LASER CHECK AND SET FUNCTIONS #
#################################

def checkAndSetLaserWavelength(laser_wavelength):
    """
    Utility to check that the laser wavelength is correct.
    """

    if laser_wavelength is None:
        raise RuntimeError( "Laser wavelength is not defined")

    # Check if number.
    if not isinstance( laser_wavelength, (float, int)):
        raise TypeError( "The parameter 'laser_wavelength' must be a numerical type (float or int.)")

    if laser_wavelength <= 300 or laser_wavelength > 1200:
        raise ValueError( "laser wavelength must be between 300 and 1200 nm")

 # Convert to microns.
    laser_wavelength = laser_wavelength*1e-3
    print ("Laser wavelength = %.3fe-6" % (laser_wavelength))

    return laser_wavelength

def checkAndSetLaserPulse(laser_pulse):
    """
    Utility to check that the laser pulse type is correct.
    """

    if laser_pulse is None:
        raise RuntimeError( "Laser pulse type has not been chosen")

    pulse_shapes = ["flat","quasiflat","ramp"]

    # Check if str.
    if not isinstance(laser_pulse, str):
        raise TypeError("The parameter 'laser_pulse' must be a str.")

    # Check if pulseshape exists
    if laser_pulse in pulse_shapes:
        pass
    else:
        raise ValueError( "Laser pulse shape is not in specified list.")

    return laser_pulse

def checkAndSetLaserPulseDuration(laser_pulse_duration):
    """
    Utility to check that the laser pulse duration is valid.
    """

    if laser_pulse_duration is None:
        raise RuntimeError( "Laser pulse duration has not been set")

    # Check if number.
    if not isinstance( laser_pulse_duration, (float, int)):
        raise TypeError( "The parameter 'laser_pulse_duration' must be a numerical type (float or int.)")

    if laser_pulse_duration < 1.0 or laser_pulse_duration > 50.0:
        raise ValueError( "Laser pulse must be between 1.0 and 50.0 ns")

    return laser_pulse_duration

def checkAndSetLaserIntensity(laser_intensity):
    """
    Utility to check that the laser intensity is valid.
    """

    if laser_intensity is None:
        raise RuntimeError( "Laser intensity has not been set")

    # Check if number.
    if not isinstance( laser_intensity, (float, int)):
        raise TypeError( "The parameter 'laser_intensity' must be a numerical type (float or int.)")

    # TODO: Check these for more realistic limits of TW/cm**2
    if laser_intensity < 0.001 or laser_intensity > 100.0:
        raise ValueError( "Laser pulse must be between 1.0 and 50.0 ns")

    return laser_intensity

def checkAndSetRunTime(run_time):
    """
    Utility for checking the simulation run time is valid
    """

    if run_time is None:
        raise RuntimeError( "Simulation run time is not set")

    # TODO: Check run times
    if run_time < 1.0 or run_time > 50.0:
        raise ValueError( "Simulation run time should be > 5.0 ns and < 50.0 ns")

    return run_time

def checkAndSetDeltaTime(delta_time):
    """
    Utility for checking the simulation delta time (resolution) is valid
    """

    if delta_time is None:
        raise RuntimeError( "Simulation delta time (time resolution) is not set")

    if delta_time < 0.001 or delta_time > 0.5:
        raise ValueError( "Simulation delta time should be > 10 ps and < 500 ps")

    return delta_time

def checkAndSetSampleEosType(sample_eos_type):
    """
    Utility for choosing the EOS to use for simulation
    """
    
    if sample_eos_type is None: # Set to default EOS (sesame)
        print "EOS type not defined, using default eos (sesame)"
        sample_eos_type = "sesame"
        return sample_eos_type
    
    eos_choices = ["sesame", "blf"]
    
    # Check if str.
    if not isinstance(sample_eos_type, str):
        raise TypeError("The parameter 'sample_eos_type' must be a str (sesame or blf)")

    # Check if EOS type is allowed
    if sample_eos_type in eos_choices:
        pass
    else:
        raise ValueError( "EOS must be either sesame or blf only")
    
    return sample_eos_type

##################################################################
# Setup feathering checkAndSet options (Expert mode)
##################################################################

def checkAndSetNumberOfZones(number_of_zones):
    """
    Utility for checking the number of zones is valid
    """
    
    # Set default value to 250
    if number_of_zones is None:
        number_of_zones = 250
    
    # Make sure  number of zones > 200 and < 1000
    if number_of_zones < 150 or number_of_zones > 1000:
        raise ValueError( "Number of zones should be > 150 and < 1000")

    return number_of_zones

def checkAndSetFeatherZoneWidth(feather_zone_width):
    """
    Utility for checking the feather zone width is valid
    """
    
    # Set default value to 4.0
    if feather_zone_width is None:
        feather_zone_width = 4.0
    
    if feather_zone_width < 2.0 or feather_zone_width > 10.0:
        raise ValueError( "Feather zone width should not be < 2.0 micron or > 10.0 micron")

    return feather_zone_width

def checkAndSetMinimumZoneWidth(minimum_zone_width):
    """
    Utility for checking the feather zone width is valid
    """
    
    # Set default value to 4e-4
    if minimum_zone_width is None:
        minimum_zone_width = 4e-4
    
    if minimum_zone_width < 0.0001 or minimum_zone_width > 0.001:
        raise ValueError( "Minimum zone width should not be < 1 Angstrom or > 10 Angstrom")

    return minimum_zone_width