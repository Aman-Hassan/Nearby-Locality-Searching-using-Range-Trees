#---PointDatabase---#
#References have been taken from various Univeristy websites and Computational Geometry book

class PointDatabase:
    class Node:
        def __init__(self,val,lc = None,rc = None,assoctree = None):
            self.v = val
            self.lc = lc
            self.rc = rc
            self.assoctree = assoctree
    
    
    def __init__(self,pointlist):
        if pointlist == []:
            self.root = None
        else:
            Lx,Ly = self.Sorter(pointlist,0), self.Sorter(pointlist,1)
            # print(Lx,Ly)
            l = len(Lx)
            self.L = []
            self.root = self.CreateTree(Lx,Ly,(float('inf'),float('inf')))

        # self.in_order_2d_print(self.root)
        
    #-----Helper functions for creating __init__ method-----#
    def in_order_print(self,root):
        if root.lc:
            self.in_order_print(root.lc)
        print(root.v, end=" ")
        if root.rc:
            self.in_order_print(root.rc)
    
    def in_order_2d_print(self,root):
        if root.lc:
            self.in_order_2d_print(root.lc)
        print()
        if root.assoctree:
            print(root.v,end=": ")
            self.in_order_print(root.assoctree)
        else:
            self.in_order_print(root)
        print()
        if root.rc:
            self.in_order_2d_print(root.rc)

    def Sorter(self,L,index): #Helper function to sort - uses inbuilt sort function of lists
        if index == 0:
            L1 = sorted(L)
            return(L1)
        else:
            for i in range(len(L)):
                element = (L[i][1],L[i][0])
                L[i] = tuple(element)
            L2 = sorted(L)
            for i in range(len(L)):
                element = (L2[i][1],L2[i][0])
                L2[i] = tuple(element)
            return(L2)
        
    
    def AssociatedTree(self,L): #Helper function to create Associated trees recursively
        ly = len(L)
        ymedian = L[(ly-1)//2]
        if ly == 1:
            lc = None
            rc = None
        else:
            if ((ly-1)//2) == 0:
                lc = None
            else:
                lc = self.AssociatedTree(L[:(ly-1)//2])
            rc = self.AssociatedTree(L[(ly-1)//2 + 1:])
        return(self.Node(ymedian,lc,rc,None))
        
    
    def CreateTree(self,L1,L2,old_median): #Helper function to create Tree sorted in x with associated trees sorted in y at each node
        lx = len(L1)
        # print(L1,L2,old_median,"\n")
        # print(L1,lx,(lx-1)//2)
        xmedian = L1[((lx-1)//2)]
        # print(xmedian)
        L3 = []

        #Creation of Associated Tree: 
        if xmedian[0] < old_median[0]:
            for i in L2:                          
                if i[0] < old_median[0]:
                    L3.append(i)
        else:
            for i in L2:
                if i[0] > old_median[0]:
                    L3.append(i)
        y_pointer = self.AssociatedTree(L3)
        
        #Assigning node values
        if lx == 1:
            lc = None
            rc = None
        else:
            if ((lx-1)//2) == 0:
                lc = None
            else:
                lc = self.CreateTree(L1[:((lx-1)//2)],L3,xmedian)
            rc = self.CreateTree(L1[((lx-1)//2) + 1:],L3,xmedian)
        return(self.Node(xmedian,lc,rc,y_pointer))

    #-----End of Helper functions for __init__ method-----#


   
    def searchNearby(self,q,d):
        if self.SearchRangeTree2d(q[0]-d,q[0]+d,q[1]-d,q[1]+d,2) is None:
            return []
        return(self.SearchRangeTree2d(q[0]-d,q[0]+d,q[1]-d,q[1]+d,2))
     
    #-----Helper functions for SearchNearby function-----#
    def getv1(self,node):
        return node.v

    def getv2(self,node,check):
        if check:
            v = node.v[0]
        else:
            v = node.v[1]
        return v

    def SplitNode2(self,root, p_min, p_max,check):
        splitnode = root
        while splitnode != None:
            node = self.getv2(splitnode,check)
            if p_max < node:
                splitnode = splitnode.lc
            elif p_min > node:
                splitnode = splitnode.rc
            elif p_min <= node <= p_max:
                break
        return splitnode

    def SplitNode1(self,root, p_min, p_max):
        splitnode = root
        while splitnode != None:
            node = self.getv1(splitnode)
            if p_max < node:
                splitnode = splitnode.lc
            elif p_min > node:
                splitnode = splitnode.rc
            elif p_min <= node <= p_max:
                break
        return splitnode

    def SearchRangeTree1d(self,tree, p1, p2, dim, check=True):

        nodes = []
        # find the node which the least common ancestor in the tree for given range
        if dim == 1:
            splitnode = self.SplitNode1(tree, p1, p2)
        else:
            splitnode = self.SplitNode2(tree, p1, p2, check)
        if splitnode == None:
            return nodes
        if dim == 1:
            x = self.getv1(splitnode)
        else:
            x = self.getv2(splitnode,check)
        
        # Check if the node is a valid node in range
        if (x >= p1 and x <= p2):
            nodes.append(splitnode.v)
        # search for nodes in lc subtree
        for i in self.SearchRangeTree1d(splitnode.lc, p1, p2, dim, check):
            nodes.append(i)
        # search for nodes in right subtree
        for i in self.SearchRangeTree1d(splitnode.rc, p1, p2, dim, check):
            nodes.append(i)
        return nodes

    def SearchRangeTree2d(self, x1, x2, y1, y2, dim):
        results = []
        # find the node which the least common ancestor in the tree for given range
        splitnode = self.SplitNode2(self.root, x1, x2,True)
        if (splitnode == None):
            return results
        x = splitnode.v[0]
        y = splitnode.v[1]
        if (x >= x1 and x <= x2 and y >= y1 and y <= y2):
            results.append(splitnode.v)
            # Traverse the nodes in left child of split node
        vl = splitnode.lc
        while (vl != None):
            # Check if the node is a valid node in range
            x = vl.v[0]
            y = vl.v[1]
            if (x >= x1 and x <= x2 and y >= y1 and y <= y2):
                results.append(vl.v)

            # Search the associated ytree at the left child of current node in xtree
            if (x1 <= vl.v[0]):
                if vl.rc != None:
                    for i in self.SearchRangeTree1d(vl.rc.assoctree, y1, y2, dim, False):
                        results.append(i)
                vl = vl.lc
            else:
                vl = vl.rc

        # Traverse the nodes in left child of split node
        vr = splitnode.rc
        while (vr != None):
            # Check if the node is a valid node in range
            x = vr.v[0]
            y = vr.v[1]
            if (x >= x1 and x <= x2 and y >= y1 and y <= y2):
                results.append(vr.v)
            # Search the associated ytree at the left child of current node in xtree
            if (x2 >= vr.v[0]):
                if vr.lc != None:
                    for i in self.SearchRangeTree1d(vr.lc.assoctree, y1, y2, dim, False):
                        results.append(i)
                vr = vr.rc
            else:
                vr = vr.lc

        return results

    
    #-----end of Helper Functions for searchNearby-----#

pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])
pointDbObject.searchNearby((5,5), 1)
# # []
pointDbObject.searchNearby((4,8), 2)
# # [(3,7), (4,9)]
pointDbObject.searchNearby((10,2), 1.5)
# # [(9,2)]

