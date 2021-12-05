import sys
import math

# Data structure to store x, y and z coordinates of a point
class Point:
    def __init__ (self,x,y,z):
        # A point with x, y and z cordinates as x, y and z
        self.x = x
        self.y = y
        self.z = z
    def __str__ (self):
        # used for printing the points while debugging
        return str(self.x)+" "+str(self.y)+" "+str(self.z)
    def __sub__(self, point):
        # return a point i.e. vector resulting from the differenc of the two vectors
        return Point(self.x-point.x, self.y-point.y, self.z-point.z)
    def __eq__ (self,point):
        # If all the three x, y and z coordinates are equal the the two points are equal
        return (self.x==point.x) and (self.y==point.y) and (self.z==point.z)
    def dotProduct (self,point):
        # return the dot product of the two given points/vectors
        return (self.x * point.x + self.y * point.y + self.z * point.z)
    def dotProduct2D (self,point): # when projected on X-Y plane
        # return the dot product of the two given points/vectors when projected on X-Y plane
        # It ignores the z coordinates
        return (self.x * point.x + self.y * point.y)
    def crossProduct (self,point):
        # return the cross product of the two given points/vectors
        x = (self.y * point.z) - (self.z * point.y)
        y = (self.z * point.x) - (self.x * point.z)
        z = (self.x * point.y) - (self.y * point.x)
        return Point(x, y, z)
    def normalize (self):
        # It normalize the vector/point
        length = self.length()
        self.x = self.x/length
        self.y = self.y/length
        self.z = self.z/length
    def normalize2D (self): # when projected on X-Y plane
        # It normalize the vector/point when projected on X-Y plane
        # It ignores the z coordinate
        length = self.length2D()
        self.x = self.x/length
        self.y = self.y/length
    def length (self):
        # It returns the length of the vector
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def length2D (self): # when projected on X-Y plane
        # It returns the length of the vector when projected on X-Y plane
        # It ignores the z coordinate
        return math.sqrt(self.x**2 + self.y**2)
    def __hash__ (self):
        # return the hash value of the object which is used to compare dictionary keys during a dictionary lookup quickly
        return hash((self.x,self.y,self.z))

# Data structure to store two end points of a edge with direction
class Edge:
    def __init__ (self,point1,point2):
        # This is a edge with two end points as point1 and point2
        # It's direction is from point1 to point2
        self.point1 = point1
        self.point2 = point2
    def __eq__ (self,edge):
        # In my implementation the direction of edge used determine the direction of the normal of the plane formed
        # The plane formed should have all the other remaining points pointing opposite to the direction of its normal
        # A-->B used with point C and B-->A used with point C will create two planes with normals pointing in opposite directions
        # Hence A-->B is distinguished from B-->A. Here edge is represented by two end points and its direction
        if ((self.point1 == edge.point1) and (self.point2 == edge.point2)):
            return True
        return False
    def __str__(self):
        # used for printing the edges while debugging
        return "["+str(self.point1)+";"+str(self.point2)+"]"
    def reverse (self):
        # return an edge with the same end points but with opposite direction
        return Edge(self.point2,self.point1)
    def __hash__(self):
        # return the hash value of the object which is used to compare dictionary keys during a dictionary lookup quickly
        return hash((self.point1,self.point2))

# A function to find the point in the set of input points such that it together with the
# given edge will form a plane with the maximum angle in the direction of the given edge
def findPoint3D(edge1):
    point1 = edge1.point1
    point2 = edge1.point2
    vector1 = point2 - point1
    direction = vector1                            # vector in the direction of the given edge
    direction.normalize()                          # unit vector in the direction of the given edge
    initialized = False
    normal = None
    point3 = None
    cosine_min = None
    special = None
    exist = False
    sum = 0
    for point in points:
        if point != point1 and point != point2:    # ensure point is different from point1 and point2
            vector2 = point - point2
            temp = vector1.crossProduct(vector2)   # vector pointing in the direction of the normal to the plane with given edge and point
            try:
                temp.normalize()                   # implies point, point1 and point2 will form a plane
            except:
                continue                           # implies colinear points
            if not initialized:
                initialized = True                 # marker to indicate the reference for angle measurement has been initialized
                normal = temp                      # this is the reference for angle measurement for planes
                point3 = point                     # initialize point3 with the point for which the plane has 0 angle w.r.t reference
                cosine_min = 1                     # initialize angle with 0 i.e. cosine = 1 as angle grows cosine decrease
            cosine = normal.dotProduct(temp)   # cos(θ) helps determine the magnitute of the angle of plane
            sine = normal.crossProduct(temp)   # A vector with magnitute sin(θ) and pointing in the direction of the angle
            # temp2 is positive when direction of angle is same as that of the direction of the given edge else negetive
            # temp2 is the sign of angle
            temp2 = direction.dotProduct(sine)
            sum += temp2   # stores the sign of angles for all planes
            if cosine < cosine_min and temp2 > 0:
                # temp2 > 0 means the direction of angle is same as that of the direction of the given edge i.e. angle sign is positive
                # lower the cosine value larger is the angle
                point3 = point       # The point found sofar which makes a plane with maximum angle
                # It has positive angle sign or we can say it is in the direction of the given edge
                cosine_min = cosine  # cosine of the maximum angle sofar
            if cosine < 0 and temp2 == 0:
                # temp2 is zero when angle is 0 (minimum) or 180 degrees (maximum) in either along the direction of the given edge or opposite
                # That means angle sign may be positive or negetive
                # Since cosine < 0 implies angle must be 180 degrees (maximum)
                special = point  # This is the special case when angle of plane is maximum but angle sign or direction is unknown
                exist = True     # this marker indicate that there exist a special point
    if sum > 0 and exist == True:
        # if there exist a special point then the sign of the angle for the plane formed by this point is same as the remaining points
        # sum stores the sign of the angles for all planes and add them together
        # All positive will add to positive and all negative will add to negative
        # Hence sum is the sign of the angle for the plane formed by this point
        point3 = special   # since sum > 0 implies angle sign is positive and we know special case has maximum possible angle i.e. 180
    return point3

# A function to find the point in the set of input points such that it together with the given point
# will form a line with the maximum angle when projected in X-Y plane such that all other points when
# also projected on X-Y plane fall in either of the two partitions in X-Y plance separated by the line
def findPoint2D(point1): # when projected on X-Y plane
    initialized = False
    vector = None
    point2 = None
    cosine_min = None
    for point in points:
        if point.x != point1.x or point.y != point1.y:    # ensure point and point1 don't have same projection in X-Y plane
            temp = point - point1                         # vector from point1 to point
            temp.normalize2D()         # unit vector in the direction of projection of vector from point1 to point in X-Y plane
            if not initialized:
                initialized = True     # marker to indicate the reference for angle measurement has been initialized
                vector = temp          # this is the reference for angle measurement for lines
                point2 = point         # initialize point2 with the point for which the line has 0 angle w.r.t reference
                cosine_min = 1         # initialize angle with 0 i.e. cosine = 1 as angle grows cosine decrease
            cosine = vector.dotProduct2D(temp)            # helps determine the magnitute of the angle of line
            if cosine < cosine_min:    # lower the cosine value larger is the angle
                point2 = point         # The point found sofar which makes a line with maximum angle
                cosine_min = cosine    # cosine of the maximum angle sofar
    return point2

points = set() # Set of input points
# Open CONVEX.IN and store all the input set of points in the set- "points"
infile = open(sys.argv[1],"r") # Open the input file
n = infile.readline()          # read the first line which is the total number of points in input set
initialized = False
point1 = None                  # This will store the point in the input set of points with minimum x coordinate
for line in infile:            # read line by line from input file
    x,y,z = line.split()       # split the line to get x, y and z coordinates
    point = Point(float(x),float(y),float(z))     # create a point from input line
    points.add(point)                             # add the point in points set
    if not initialized:
        initialized = True
        point1 = point         # initialize the point with the first point in input set
    if point.x < point1.x:     # Finds the point with the smaller x coordinate
        point1 = point         # update the point1 to store the point with minimum x coordinate sofar
infile.close()                 # close the input file

explored = set()                # explored set of edges
point2 = findPoint2D(point1)    # the point in the set of input points such that it together with the point1
# will form a line with the maximum angle when projected in X-Y plane such that all other points when
# also projected on X-Y plane fall in either of the two partitions in X-Y plance separated by the line
edge = Edge(point1,point2)      # A edge in the convex-hull
edges = {edge}                  # pending set of edges
while len(edges)>0:
    edge1 = edges.pop()                            # take an edge from pending set
    point = findPoint3D(edge1)                     # the point in the set of input points such that
    # it together with the edge1 will form a plane with the maximum angle in the direction of the edge1
    edge2 = Edge(edge1.point2,point)               # A edge in the convex-hull
    edge3 = Edge(point,edge1.point1)               # A edge in the convex-hull
    explored.update({edge1,edge2,edge3})           # edge1, edge2, edge3 are explored because we found the plane by these edges in convex-hull
    edges.difference_update({edge1,edge2,edge3})   # once explored they need to be removed from pending set
    edge1 = edge1.reverse()                        # edge1 with opposite direction
    edge2 = edge2.reverse()                        # edge2 with opposite direction
    edge3 = edge3.reverse()                        # edge3 with opposite direction
    # every edge is present in two triangular faces (planes) in convex-hull with two different directions
    # Since edge1 is explored a triangular face with one edge same as edge1 is found
    # to find another triangular face with edge1 we need to explore edge1 in opposite direction
    edges.update({edge1,edge2,edge3} - explored)   # add edge1, edge2, edge3 with opposite direction in pending set if not already explored

chull = set()                                      # set of all those points that are present in convex-hull
for edge in explored:                              # explored set contain all those edges that are present in convex-hull
    chull.update({edge.point1,edge.point2})        # add endpoints of all the edges that are present in convex-hull
# Open CONVEX.OUT and write all the points in the file that are present in the covex-hull i.e. chull
outfile = open(sys.argv[2],"w")                    # Open the output file
outfile.write(str(len(chull)))                     # first line is the size of chull
for point in chull:
    outfile.write("\n"+str(point.x)+" "+str(point.y)+" "+str(point.z))    # write every points in chull in separate line
outfile.close()                                    # close the output file
