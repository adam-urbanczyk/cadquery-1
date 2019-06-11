"""
    This module tests cadquery creation and manipulation functions

"""
# system modules
import math,os.path,time,tempfile

# my modules
from cadquery import *
from cadquery import exporters
from tests import BaseTest, writeStringToFile, makeUnitCube, readFileAsString, makeUnitSquareWire, makeCube

# where unit test output will be saved
OUTDIR = tempfile.gettempdir()
SUMMARY_FILE = os.path.join(OUTDIR, "testSummary.html")

SUMMARY_TEMPLATE = """<html>
    <head>
        <style type="text/css">
            .testResult{
                background: #eeeeee;
                margin: 50px;
                border: 1px solid black;
            }
        </style>
    </head>
    <body>
        <!--TEST_CONTENT-->
    </body>
</html>"""

TEST_RESULT_TEMPLATE = """
    <div class="testResult"><h3>%(name)s</h3>
    %(svg)s
    </div>
    <!--TEST_CONTENT-->
"""

# clean up any summary file that is in the output directory.
# i know, this sux, but there is no other way to do this in 2.6, as we cannot do class fixutres till 2.7
writeStringToFile(SUMMARY_TEMPLATE, SUMMARY_FILE)


class TestCadQuery(BaseTest):

    def tearDown(self):
        """
            Update summary with data from this test.
            This is a really hackey way of doing it-- we get a startup event from module load,
            but there is no way in unittest to get a single shutdown event-- except for stuff in 2.7 and above

            So what we do here is to read the existing file, stick in more content, and leave it
        """
        svgFile = os.path.join(OUTDIR, self._testMethodName + ".svg")

        # all tests do not produce output
        if os.path.exists(svgFile):
            existingSummary = readFileAsString(SUMMARY_FILE)
            svgText = readFileAsString(svgFile)
            svgText = svgText.replace(
                '<?xml version="1.0" encoding="UTF-8" standalone="no"?>', "")

            # now write data into the file
            # the content we are replacing it with also includes the marker, so it can be replaced again
            existingSummary = existingSummary.replace("<!--TEST_CONTENT-->", TEST_RESULT_TEMPLATE % (
                dict(svg=svgText, name=self._testMethodName)))

            writeStringToFile(existingSummary, SUMMARY_FILE)

    def saveModel(self, shape):
        """
            shape must be a CQ object
            Save models in SVG and STEP format
        """
        shape.exportSvg(os.path.join(OUTDIR, self._testMethodName + ".svg"))
        shape.val().exportStep(os.path.join(OUTDIR, self._testMethodName + ".step"))

    def testText(self):

        box = Workplane("XY" ).box(4, 4, 0.5)

        obj1 = box.faces('>Z').workplane()\
            .text('CQ 2.0',0.5,-.05,cut=True,halign='left',valign='bottom', font='Sans')

        #combined object should have smaller volume
        self.assertGreater(box.val().Volume(),obj1.val().Volume())

        obj2 = box.faces('>Z').workplane()\
            .text('CQ 2.0',0.5,.05,cut=False,combine=True, font='Sans')

        #combined object should have bigger volume
        self.assertLess(box.val().Volume(),obj2.val().Volume())

        #verify that the number of top faces is correct (NB: this is font specific)
        self.assertEqual(len(obj2.faces('>Z').vals()),5)

        obj3 = box.faces('>Z').workplane()\
            .text('CQ 2.0',0.5,.05,cut=False,combine=False,halign='right',valign='top', font='Sans')

        #verify that the number of solids is correct
        self.assertEqual(len(obj3.solids().vals()),5)
