# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 19:34:53 2019

@author: parju
"""

from Queue import Queue


class Node:
    def __init__(self, label, value, parent):
        self.label = label
        self.value = value
        self.parent = parent
        self.leftChild = None
        self.rightChild = None

    def hasLeftChild(self):
        if(self.leftChild):
            return True
        return False
    
    def getLeftChild(self):
        return self.leftChild
    
    def setLeftChild(self, leftC):
        self.leftChild = leftC
    
    def hasRightChild(self):
        if(self.rightChild):
            return True
        
    def getRightChild(self):
        return self.rightChild
    
    def setRightChild(self, rightC):
        self.rightChild = rightC
    
    def getParent(self):
        return self.parent
    
    def setParent(self, p):
        self.parent = p
    
    def isLeaf(self):
        return (not self.leftChild and not self.rightChild)
    
    def isRightChild(self):
        return (self.getParent().hasRightChild() and self.value == self.parent.rightChild.value)
    
    def isLeftChild(self):
        return (self.getParent().hasLeftChild() and self.value == self.parent.leftChild.value)
    
    def hasGrandPa(self):
        if(self.parent.parent is not None):
            return True
        return False
    
    def getGrandPa(self):
        return self.parent.parent
    
    def isRoot(self):
        return (self.parent is None)


class BST:
    def __init__(self):
        self.root = None
        self.weight = 0
        self.depth = 1
        self.height = 0

    def getNodeLevel(self, node):
        if(node.parent is None):
            return 0

        return 1 + self.getNodeLevel(node.parent)

    def getHeight(self):
        return self.height

    def setHeight(self):
        self.height = self.depth - 1

    def getDepth(self):
        return self.depth

    def setDepth(self):
        nodes = self.preOrd()
        nodesLvl = []

        for node in nodes:
            nodesLvl.append(self.getNodeLevel(node))

        self.depth += max(nodesLvl)

    def getWeight(self):
        return self.weight

    def addNodes(self, list):
        for node in list:
            self.addNode(str(node), node)

        self.setDepth()
        self.setHeight()

    def addNode(self, label, value):
        if(self.root):
            self._addNode(label, value, self.root)
        else:
            self.root = Node(label, value, None)
        self.weight += 1

    def _addNode(self, label, value, parent):
        if(value > parent.value):
            if(parent.rightChild):
                self._addNode(label, value, parent.rightChild)
            else:
                parent.rightChild = Node(label, value, parent)
        elif(value < parent.value):
            if(parent.leftChild):
                self._addNode(label, value, parent.leftChild)
            else:
                parent.leftChild = Node(label, value, parent)
        else:
            print(f"Node {str(value)} already exists!")

    def pathWidth(self, node=None, queue=Queue()):
        if(not node):
            node = self.root
            queue.put(node)

        if(node.hasLeftChild()):
            queue.put(node.leftChild)

        if(node.hasRightChild()):
            queue.put(node.rightChild)

        if(node.hasLeftChild()):
            self.pathWidth(node.leftChild, queue)

        if(node.hasRightChild()):
            self.pathWidth(node.rightChild, queue)
        return queue

    def _pathWidth(self, lvl=0):
        if(lvl > self.getHeight()):
            return []

        unorderedNodeList = self.preOrd()
        orderedList = []

        for node in unorderedNodeList:
            if(self.getNodeLevel(node) == lvl):
                orderedList.append(node)

        return orderedList + self._pathWidth(lvl+1)

    def preOrd(self):
        if(self.root):
            nodeList = []
            nodeList = self._preOrd(self.root, nodeList)

            return nodeList
        else:
            print("Empty Tree")

    def _preOrd(self, node, preList):
        preList.append(node)

        if(node.hasLeftChild()):
            self._preOrd(node.leftChild, preList)

        if(node.hasRightChild()):
            self._preOrd(node.rightChild, preList)

        return preList

    def inOrd(self):
        if(self.root):
            nodeList = []
            nodeList = self._inOrd(self.root, nodeList)

            return nodeList
        else:
            print("Empty Tree")

    def _inOrd(self, node, inList):
        if(node.leftChild):
            self._inOrd(node.leftChild, inList)

        inList.append(node)

        if(node.rightChild):
            self._inOrd(node.rightChild, inList)

        return inList

    def postOrd(self):
        if(self.root):
            nodeList = []
            nodeList = self._postOrd(self.root, nodeList)

            return nodeList
        else:
            print("Empty Tree")

    def _postOrd(self, node, postList):
        if(node.leftChild):
            self._postOrd(node.leftChild, postList)

        if(node.rightChild):
            self._postOrd(node.rightChild, postList)

        postList.append(node)

        return postList

    def externalNodes(self):
        allNodes = self.preOrd()
        currentList = []

        for node in allNodes:
            if(not node.hasLeftChild() and not node.hasRightChild()):
                print(node.value, end=',')
                currentList.append(node)

        return currentList

    def internalNodes(self):
        allNodes = self.preOrd()
        currentList = []

        for node in allNodes:
            if((node.hasLeftChild() or node.hasRightChild()) and node.parent):
                print(node.value, end=',')
                currentList.append(node)

        return currentList

    def operateLevels(self, lvl=0):
        if(lvl > self.getHeight()):
            return None

        nodeList = self.preOrd()
        currentList = []
        result = 0

        for node in nodeList:
            if(self.getNodeLevel(node) == lvl):
                currentList.append(node.value)

        if(lvl % 2 == 0):
            for num in currentList:
                result += num
        else:
            result = 1
            for num in currentList:
                result *= num

        print(result)

        self.operateLevels(lvl+1)

    def searchElement(self, nodeValue):
        nodeList = self.preOrd()
        requestedNode = None

        for node in nodeList:
            if(node.value == nodeValue):
                requestedNode = node
                print(self.getNodeLevel(node))
                return requestedNode

        print("This node doesn't exists.")

    def nodeXtoYcore(self, valueNodeX, valueNodeY):
        x = self.searchElement(valueNodeX)
        y = self.searchElement(valueNodeY)

        nodeList = []
        try:
            nodeList = self._postOrd(x, nodeList)
        except:
            print(f"Node {valueNodeX} doesn't exists!")
            return False

        if(y in nodeList):
            print(f"There is a route between {valueNodeX} and {valueNodeY}.")
        else:
            print(f"No Route between {valueNodeX} and {valueNodeY}")

    # def nodeXtoY(self, nodeX, nodeY):
    #     if(nodeX.hasLeftChild()):
    #         if(nodeX.leftChild == nodeY):
    #             return True
    #         self.nodeXtoY(nodeX.leftChild, nodeY)

    #     if(nodeX.hasRightChild()):
    #         if(nodeX.rightChild == nodeY):
    #             return True
    #         self.nodeXtoY(nodeX.rightChild, nodeY)

    #     return False

#
#listofNodes = [54, 26, 8, 77, 63, 35, 43, 69, 59, 56, 55, 58, 86, 79, 100]
#
#myBST = BST()
#myBST.addNodes(listofNodes)
#
## Remove 8, 77, 86
#
#l = myBST.preOrd()
#
#for node in l:
#    print(node.value, end=', ')

