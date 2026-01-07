"""
ORIGINAL
Cluster class for k-Means clustering

This file contains the class cluster, which is the second part of the assignment.
With this class done, the visualization can display the centroid of a single
cluster.

Keira Chen (kc2272) and Henry Yoon (hjy22)
November 15, 2024
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6dataset

# TASK 2: CLUSTER
class Cluster(object):
    """
    A class representing a cluster, a subset of the points in a dataset.

    A cluster is represented as a list of integers that give the indices in the
    dataset of the points contained in the cluster. For instance, a cluster
    consisting of the points with indices 0, 4, and 5 in the dataset's data
    array would be represented by the index list [0,4,5].

    A cluster instance also contains a centroid that is used as part of the
    k-means algorithm. This centroid is list of n numbers, where n is the
    dimension of the dataset. While this looks like a point in the dataset, it
    typically is not actually in the dataset (as it is usually in between the
    data points).
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization with no DIRECT access)
    # Attribute _dataset: The Dataset for this cluster
    # Invariant: _dataset is an instance of Dataset
    #
    # Attribute _centroid: The centroid of this cluster
    # Invariant: _centroid is a point (list of int/float) whose length is equal
    # to the dimension of _dataset.
    #
    # MUTABLE ATTRIBUTES (Can be changed at any time, via addIndex, or clear)
    # Attribute _indices: the indices of this cluster's points in the dataset
    # Invariant: _indices is a list of ints. For each element ind in _indices,
    # 0 <= ind <= _dataset.getSize()

    # Part A
    def getIndices(self):
        """
        Returns the indices of points in this cluster

        This method returns the indices directly (not a copy). Any changes made
        to this list will modify the cluster.
        """
        return self._indices


    def getCentroid(self):
        """
        Returns a COPY centroid of this cluster.

        This getter method is to protect access to the centroid, and prevent
        someone from changing it accidentally. That means this method has to
        copy the centroid before returning it.
        """
        return self._centroid[:]


    def __init__(self, dset, centroid):
        """
        Initializes a new empty cluster whose centroid is a copy the given one

        This method COPIES the centroid. It does not use the original centroid
        passed as an argument.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter centroid: the cluster centroid
        Precondition: centroid is a list of ds.getDimension() numbers
        """
        assert isinstance(dset, a6dataset.Dataset)
        assert isinstance(centroid, list) and len(centroid)==dset.getDimension()

        self._dataset = dset
        self._centroid = centroid[:]
        self._indices = []


    def addIndex(self, index):
        """
        Adds the given dataset index to this cluster.

        If the index is already in this cluster, this method leaves the
        cluster unchanged.

        Precondition: index is a valid index into this cluster's dataset.
        That is, index is an int >= 0, but less than the dataset size.
        """
        assert isinstance(index, int)
        assert 0 <= index < self._dataset.getSize()

        if index not in self._indices:
            self._indices.append(index)


    def clear(self):
        """
        Removes all points from this cluster, but leaves the centroid unchanged.
        """
        self._indices.clear()


    def getContents(self):
        """
        Returns a new list containing copies of the points in this cluster.

        The result is a list of points (lists of int/float). It has to be
        computed from the list of indices.
        """
        newList = []

        for index in self._indices:
            pointCopy = self._dataset.getPoint(index)
            newList.append(pointCopy)

        return newList


    # Part B
    def distance(self, point):
        """
        Returns the euclidean distance from point to this cluster's centroid.

        Parameter point: The point to be measured
        Precondition: point is a list of numbers (int or float), with the same
        dimension as the centroid.
        """
        assert a6dataset.is_point(point)
        assert len(point) == len(self._centroid)

        cent = self.getCentroid()
        sum = 0

        for i in range(len(point)):
            temp = float(cent[i]) - float(point[i])
            temp = pow(temp, 2)
            sum += temp

        return math.sqrt(sum)


    def getRadius(self):
        """
        Returns the maximum distance from any cluster point to the centroid.

        This method loops over the contents of this cluster to find the maximum
        distance from the centroid.
        """
        maxDistance = 0

        for x in self._indices:
            point = self._dataset.getPoint(x)
            distanceToCentroid = self.distance(point)

            if distanceToCentroid > maxDistance:
                maxDistance = distanceToCentroid

        return maxDistance


    def update(self):
        """
        Returns True if the centroid remains unchanged; False otherwise.

        This method recomputes the centroid of this cluster. The new centroid is
        the average of the of the contents (To average a point, average each
        coordinate separately).

        Whether the centroid "remained unchanged" after recomputation is
        determined by numpy.allclose. The return value should be interpreted as
        an indication of whether the starting centroid was a "stable" position
        or not.

        If there are no points in the cluster, the centroid does not change.
        """
        if len(self._indices) == 0:
            return True

        newCentroid = []
        for k in range(len(self._centroid)):
            newCentroid.append(0)

        for x in self._indices:
            point = self._dataset.getPoint(x)
            for i in range(len(point)):
                newCentroid[i] += point[i]

        for i in range(len(newCentroid)):
            newCentroid[i] /= len(self._indices)

        if numpy.allclose(self._centroid, newCentroid):
            return True
        else:
            self._centroid = newCentroid
            return False


    # PROVIDED METHODS: Do not modify!
    def __str__(self):
        """
        Returns a String representation of the centroid of this cluster.
        """
        return str(self._centroid)+':'+str(self._indices)


    def __repr__(self):
        """
        Returns an unambiguous representation of this cluster.
        """
        return str(self.__class__) + str(self)
