#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the 'Software'), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ['O. Svensson']
__license__ = 'MIT'
__date__ = '21/04/2019'

# Corresponding EDNA code:
# https://github.com/olofsvensson/edna-mx
# mxPluginExec/plugins/EDPluginH5ToCBF-v1.1/plugins/EDPluginH5ToCBFv1_1.py

import pathlib
import logging

from tasks.AbstractTask import AbstractTask

from utils import UtilsImage
from utils import UtilsConfig

logger = logging.getLogger('edna2')


class H5ToCBFTask(AbstractTask):

    def run(self, inData):
        outData = {}
        hdf5File = pathlib.Path(inData['hdf5File'])
        directory = hdf5File.parent
        prefix = UtilsImage.getPrefix(hdf5File)
        if 'imageNumber'in inData:
            commandLine, cbfFile = self.generateCommandsWithImageNumber(
                inData, directory, prefix, hdf5File)
            outData['outputCBFFile'] = str(cbfFile)
        elif 'startImageNumber' in inData and 'endImageNumber' in inData:
            commandLine, template = self.generateCommandsWithImageRange(
                inData, directory, prefix, hdf5File)
            outData['outputCBFFileTemplate'] = template
        self.setLogFileName('h5ToCBF.log')
        self.runCommandLine('eiger2cbf ' + commandLine)
        return outData

    def generateCommandsWithImageNumber(self, inData, directory, prefix,
                                        hdf5File):
        """
        This method creates a list of commands for the converter
        """
        imageNumber = inData['imageNumber']
        if 'hdf5ImageNumber' in inData:
            hdf5ImageNumber = inData['hdf5ImageNumber']
        else:
            hdf5ImageNumber = imageNumber
        if 'master' in str(hdf5File):
            masterFile = hdf5File
        else:
            if UtilsConfig.isEMBL():
                fileName = '{0}_master.h5'.format(prefix)
            else:
                fileName = '{0}_{1}_master.h5'.format(prefix, hdf5ImageNumber)
            masterFile = directory / fileName
        if 'forcedOutputImageNumber' in inData:
            cbfFileName = prefix + \
                "_%04d" % inData['forcedOutputImageNumber'] + ".cbf"
            imageNumberInHdf5File = imageNumber
        else:
            cbfFileName = prefix + "_%04d" % imageNumber + ".cbf"
            imageNumberInHdf5File = imageNumber - hdf5ImageNumber + 1
        if not 'forcedOutputDirectory' in inData:
            cbfFile = directory / cbfFileName
        else:
            forcedOutputDirectory = \
                pathlib.Path(inData['forcedOutputDirectory'])
            if not forcedOutputDirectory.exists():
                forcedOutputDirectory.mkdir(parents=True, mode=0o755)
            cbfFile = forcedOutputDirectory / cbfFileName
        commandLine = "{0} {1} {2}".format(
            masterFile, imageNumberInHdf5File, cbfFile
        )
        return commandLine, cbfFile

    def generateCommandsWithImageRange(self, inData, directory, prefix, hdf5File):
        startImageNumber = inData['startImageNumber']
        endImageNumber = inData['endImageNumber']
        if 'hdf5ImageNumber' in inData:
            hdf5ImageNumber = inData['hdf5ImageNumber']
        else:
            hdf5ImageNumber = startImageNumber
        if 'master' in str(hdf5File):
            masterFile = hdf5File
        else:
            fileName = prefix + "_{0}_master.h5".format(hdf5ImageNumber)
            masterFile = directory / fileName
        cbfFileNamePrefix = prefix + '_'
        if 'forcedOutputDirectory' in inData:
            forcedOutputDirectory = \
                pathlib.Path(inData['forcedOutputDirectory'])
            if not forcedOutputDirectory.exists():
                forcedOutputDirectory.mkdir(mode=0o755, parents=True)
            cbfFilePath = forcedOutputDirectory / cbfFileNamePrefix
        else:
            cbfFilePath = directory / cbfFileNamePrefix
        commandLine = "{0} {1}:{2} {3}".format(
            masterFile, startImageNumber, endImageNumber, cbfFilePath)
        cbfFileTemplate = str(cbfFilePath) + "######.cbf"
        return commandLine, cbfFileTemplate


