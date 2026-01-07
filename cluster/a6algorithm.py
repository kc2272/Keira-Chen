"""
Primary algorithm for k-Means clustering

This file contains the Algorithm class for performing k-means clustering. While
it is the last part of the assignment, it is the heart of the clustering
algorithm. You need this class to view the complete visualizer.

Keira Chen (kc2272) and Henry Yoon (hjy22)
November 15, 2024
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6dataset
import a6cluster

# TASK 3: ALGORITHM
# Part A
def valid_seeds(value, size):
    """
    Returns True if value is a valid list of seeds for clustering.

    A list of seeds is a k-element list of integers between 0 and
    size-1. In addition, no seed element can appear twice.

    Parameter value: a value to check
    Precondition: value can be anything

    Paramater size: The database size
    Precondition: size is an int > 0
    """
    assert isinstance(size, int) and size > 0

    if isinstance(value, list):
        for x in value:
            if not isinstance(x, int) or not (0 <= x < size):
                return False

        copy = []
        for i in range(len(value)):
            if value[i] in copy:
                return False
            else:
                copy.append(value[i])

        return True
    return False


class Algorithm(object):
    """
    A class to manage and run the k-means algorithm.

    The method step() performs one step of the calculation. The method run()
    will continue the calculation until it converges (or reaches a maximum
    number of steps).
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization with no DIRECT access)
    # Attribute _dataset: The Dataset for this algorithm
    # Invariant: _dataset is an instance of Dataset
    #
    # Attribute _cluster: The clusters to use at each step
    # Invariant: _cluster is a non-empty list of Cluster instances

    # Part B
    def getClusters(self):
        """
        Returns the list of clusters in this object.

        This method returns the cluster list directly (it does not copy). Any
        changes made to this list will modify the set of clusters.
        """
        return self._cluster


    def __init__(self, dset, k, seeds=None):
        """
        Initializes the algorithm for the dataset ds, using k clusters.

        If the optional argument seeds is supplied, those seeds will be a list
        of indices into the dataset. They specify which points should
        be the initial cluster centroids. Otherwise, the clusters are initialized
        by randomly selecting k different points from the database to be the
        cluster centroids.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter k: the number of clusters
        Precondition: k is an int, 0 < k <= dset.getSize()

        Paramter seeds: the initial cluster indices (OPTIONAL)
        Precondition: seeds is None, or a list of valid seeds.
        """
        assert isinstance(dset, a6dataset.Dataset)
        assert isinstance(k, int) and 0 < k <= dset.getSize()
        assert seeds == None or valid_seeds(seeds, dset.getSize())

        self._dataset = dset
        self._cluster = []
        if seeds != None:
            for i in seeds:
                newCluster = a6cluster.Cluster(dset, dset.getPoint(i))
                self._cluster.append(newCluster)
        else:
            randomSeeds = random.sample(dset.getContents(), k)
            for j in range(len(randomSeeds)):
                newCluster = a6cluster.Cluster(dset, randomSeeds[j])
                self._cluster.append(newCluster)


    # Part C
    def _nearest(self, point):
        """
        Returns the cluster nearest to point

        This method uses the distance method of each Cluster to compute the
        distance between point and the cluster centroid. It returns the Cluster
        that is closest.

        Ties are broken in favor of clusters occurring earlier in the list
        returned by getClusters().

        Parameter point: The point to compare.
        Precondition: point is a list of numbers (int or float). Its length is
        the same as the dataset dimension.
        """
        assert a6dataset.is_point(point)
        assert len(point) == self._dataset.getDimension()

        min = 10000000000000000000000000000000000000

        for x in self._cluster:
            distance = x.distance(point)
            if distance < min:
                min = distance
                nearest = x

        return nearest


    def _partition(self):
        """
        Repartitions the dataset so each point is in exactly one Cluster.
        """
        # First, clear each cluster of its points. Then, for each point in the
        # dataset, find the nearest cluster and add the point to that cluster.

        for cluster in self._cluster:
            cluster.clear()

        for i in range(self._dataset.getSize()):
            point = self._dataset.getPoint(i)
            nearestCluster = self._nearest(point)
            nearestCluster.addIndex(i)


    # Part D
    def _update(self):
        """
        Returns True if all centroids are unchanged after an update; False otherwise.

        This method first updates the centroids of all clusters. When it is done,
        it checks whether any of them have changed. It returns False if just one
        has changed. Otherwise, it returns True.
        """
        updates = []
        for x in self._cluster:
            updates.append(x.update())

        if False in updates:
            return False
        else:
            return True


    def step(self):
        """
        Returns True if the algorithm converges after one step; False otherwise.

        This method performs one cycle of the k-means algorithm. It then checks
        if the algorithm has converged and returns the appropriate result (True
        if converged, false otherwise).
        """
        self._partition()
        return self._update()
        # In a cycle, we partition the points and then update the means.


    def run(self, maxstep):
        """
        Continues clustering until either it converges or performs maxstep steps.

        After the maxstep call to step, if this calculation did not converge,
        this method will stop.

        Parameter maxstep: The maximum number of steps to perform
        Precondition: maxstep is an int >= 0
        """
        assert isinstance(maxstep, int) and maxstep >= 0
        # Call k_means_step repeatedly, up to maxstep times, until the algorithm
        # converges. Stop once you reach maxstep iterations even if the algorithm
        # has not converged.
        # You do not need a while loop for this. Just write a for-loop, and exit
        # the for-loop (with a return) if you finish early.

        for i in range(maxstep):
            if self.step() == True:
                return
