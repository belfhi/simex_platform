##########################################################################
#                                                                        #
# Copyright (C) 2015-2017 Carsten Fortmann-Grote                         #
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

""" Module that holds the EstherPhotonMatterInteractor class.

    @author : CFG
    @institution : XFEL
    @creation 20170222

"""

class EstherPhotonMatterInteractor(AbstractPhotonDiffractor):
    """
    Class interfacing the Esther Radiation-Hydrodynamics simulation backengine.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        :param parameters: Parameters for the EstherPhotonMatterInteractor.
        :type parameters: EstherPhotonMatterInteractorParameters

        :param input_path: Path to the input data for this calculator.
        :type input_path: str

        :param output_path: Path to write output data generated by this calculator to.
        :type output_path: str

        """

        # Check parameters.
        parameters = checkAndSetParameters( parameters )

        # Init base class.
        super( EstherPhotonMatterInteractor, self).__init__(parameters, input_path, output_path)

        # Set state to not-initialized (e.g. input deck is not written).
        self.__is_initialized = False

    def expectedData(self):
        """ Query for the data expected by the Diffractor. """
        return None
    #return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Diffractor. """
        return None

    def backengine(self):
        """ This method drives the backengine xrts."""
        ### TODO, system call to esther code.
        pass
        # Serialize the parameters (generate the input deck).
        self.parameters._serialize()

    @property
    def data(self):
        """ Query for the field data. """
        return self.__run_data

    def _readH5(self):
        """
        Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
         ### TODO

    def saveH5(self):
        """
        Method to save the data to a file.
        """
        ### TODO
        pass

if __name__ == "__main__":
    # Launch interactive terminal Q&A session here.


    # Setup parameters instance.
    esther_parameters = EstherPhotonMatterInteractorParameters(...)

    # Setup calculator.
    esther_calculator = EstherPhotonMatterInteractor(parameters=esther_parameters, input_path=xxx, output_path=...)

    # Run.
    esther_calculator.backengine()