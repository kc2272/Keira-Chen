"""
Dataset for k-Means clustering

This file contains the class Dataset, which is the very first part of the
assignment. You cannot do anything in this assignment (except run the unit test)
before this class is finished.

Keira Chen (kc2272) and Henry Yoon (hjy22)
November 15, 2024
"""
import math
import random
import numpy


# TASK 0: HELPERS TO CHECK PRECONDITIONS
def is_point(value):
    """
    Returns True if value is a list that only contains ints or floats

    Parameter value: a value to check
    Precondition: value can be anything
    """
    if not isinstance(value, list):
        return False
    for i in range(len(value)):
        if (not isinstance(value[i], float) and not isinstance(value[i], int)):
            return False
    return True


def is_point_list(value):
    """
    Returns True if value is a list of points (int/float lists)

    This function also checks that all points in value have same dimension.

    Parameter value: a value to check
    Precondition: value can be anything
    """
    if not isinstance(value, list):
        return False
    if is_point(value[0]) == False:
        return False
    dimension = len(value[0])
    for i in range(len(value)):
        if is_point(value[i]) == False or len(value[i]) != dimension:
            return False

    return True


# TASK 1: DATASET
class Dataset(object):
    """
    A class representing a dataset for k-means clustering.

    The data is stored as a list of points (int/float lists). All points have
    the same number elements which is the dimension of the data set.

    None of the attributes should be accessed directly outside of the class
    Dataset (e.g. in the methods of class Cluster or KMeans). Instead, this class
    has getter and setter style methods (with the appropriate preconditions) for
    modifying these values.
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization)
    # Attribute _dimension: The point dimension for this dataset
    # Invariant: _dimension is an int > 0.
    #
    # MUTABLE ATTRIBUTES (Can be changed at any time, via addPoint)
    # Attribute _contents:  The dataset contents
    # Invariant: _contents is a table of numbers (float or int), possibly empty.
    # Each row of _contents is a list of size _dimension

    # Part A
    # Getters for encapsulated attributes
    def getDimension(self):
        """
        Returns the point dimension of this data set
        """
        return self._dimension


    def getSize(self):
        """
        Returns the number of points in this data set.
        """
        return len(self._contents)


    def getContents(self):
        """
        Returns the contents of this data set as a list of points.

        This method returns the contents directly (not a copy). Any changes made
        to this list will modify the data set. If you want to access the data
        set, but want to protect yourself from modifying the data, use getPoint()
        instead.
        """
        return self._contents


    def __init__(self, dim, contents=None):
        """
        Initializes a database for the given point dimension.

        The optional parameter contents is the initial value of the data
        set. When initializing the data set, it creates a COPY of the list
        contents. If contents is None, the data set start off empty. The
        parameter contents is None by default.

        Parameter dim: The dimension of the dataset
        Precondition: dim is an int > 0

        Parameter contents: the dataset contents
        Precondition: contents is either None or it is a table of numbers (int
        or float). If contents is not None, then contents if not empty and the
        number of columns is equal to dim.
        """
        assert isinstance(dim, int) and dim > 0
        assert (contents == None or is_point_list(contents))
        if contents != None:
            assert len(contents[0]) == dim

        self._dimension = dim
        if contents != None:
            self._contents = contents[:]
        else:
            self._contents = []


    def getPoint(self, i):
        """
        Returns a COPY of the point at index i in this data set.

        Often, we want to access a point in the data set, but we want a copy to
        make sure that we do not accidentally modify the data set.  That is the
        purpose of this method.

        If you actually want to modify the data set, use the method getContents().
        That returns the list storing the data set, and any changes to that
        list will alter the data set.


        Parameter i: the index position of the point
        Precondition: i is an int that refers to a valid position in 0..getSize()-1
        """
        assert isinstance(i, int)
        assert i in range(self.getSize())

        contents = self.getContents()
        point = contents[i]
        return point[:]


    def addPoint(self,point):
        """
        Adds a COPY of point at the end of _contents.

        This method does not add the point directly. It adds a copy of the point.

        Parameter point: The point to add to the set
        Precondition: point is a list of int/float. The length of point is equal
        to getDimension().
        """
        assert is_point(point)
        assert len(point) == self.getDimension()

        self._contents.append(point[:])


    # Part B
    def __str__(self):
        """
        Returns a string representation of this dataset.

        The string returned should be formatted with each point on a line (so
        there is a newline between each point), with the index of each point
        at the start of the line. The index and the point are separated by a
        colon and a space. Finally, there should be NO spaces after any of the
        commas in the point (this is not the default)

        In addition, any ints should be cast to a float before conversion
        to a string.

        Example: Suppose the contents of this dataset is

            [[1.0, 2], [3.0, 4.0], [5, 6.0]]

        In that case, this method would produce the string

            '0: [1.0,2.0]\n1: [3.0,4.0]\n2: [5.0,6.0]'

        See the assignment instructions for more details.
        """
        s = ''
        for pointIndex in range(self.getSize()):
            s += str(pointIndex) + ': ['
            for coordinate in range(self._dimension):
                s += str(float(self._contents[pointIndex][coordinate]))
                if coordinate < self._dimension - 1:
                    s += ','
            s += ']'
            if pointIndex < self.getSize() - 1:
                s += '\n'

        return s
