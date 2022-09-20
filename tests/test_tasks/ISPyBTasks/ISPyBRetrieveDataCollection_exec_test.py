# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "05/09/2019"

import os
import unittest

from edna2.utils import UtilsTest
from edna2.utils import UtilsConfig

from edna2.tasks.ISPyBTasks import ISPyBRetrieveDataCollection


class ISPyBRetrieveDataCollectionExecTest(unittest.TestCase):

    def setUp(self):
        self.dataPath = UtilsTest.prepareTestDataPath(__file__)

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run ispyb test with default config')
    def test_execute_ISPyBRetrieveDataCollection_image(self):
        UtilsConfig.setSite('esrf_ispyb_valid')
        referenceDataPath = self.dataPath / \
            "ISPyBRetrieveDataCollection_image.json"
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        iSPyBRetrieveDataCollection = ISPyBRetrieveDataCollection(inData=inData)
        iSPyBRetrieveDataCollection.execute()
        outData = iSPyBRetrieveDataCollection.outData
        self.assertEqual(outData['imagePrefix'], 'ref-ednatest')

    @unittest.skipIf(UtilsConfig.getSite() == 'Default',
                     'Cannot run ispyb test with default config')
    def test_execute_ISPyBRetrieveDataCollection_dataCollectionId(self):
        UtilsConfig.setSite('esrf_ispyb_valid')
        referenceDataPath = self.dataPath / \
            "ISPyBRetrieveDataCollection_dataCollectionId.json"
        inData = UtilsTest.loadAndSubstitueTestData(referenceDataPath)
        iSPyBRetrieveDataCollection = ISPyBRetrieveDataCollection(inData=inData)
        iSPyBRetrieveDataCollection.execute()
        outData = iSPyBRetrieveDataCollection.outData
        self.assertEqual(outData['imagePrefix'], 'ref-ednatest')

