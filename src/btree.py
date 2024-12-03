import random
import copy
import numpy as np


class Node:
  """
  A node in the B*-tree
  """
  def __init__(self, name, parent=None, is_left=None, left=None, right=None, is_leaf=False):
    self.type = "NODE"
    self.name = name
    self.parent = parent # only none if root
    self.left = left
    self.right = right
    self.is_leaf = is_leaf
    self.is_left = is_left

  def __str__(self):
    s = ""
    s += self.type + ": " + self.name + "\n"
    return s


class Nodes:
  """
  Represents the nodes in a B*-tree
  """
  def __init__(self, num_nodes):
    self.num_nodes =num_nodes
    self.nodes = []
    self.nodes_dict = {}

  def __iter__(self):
    return self.nodes.__iter__()

  def __len__(self):
    return len(self.nodes)

  def __getitem__(self, node_name):
    return self.get_node(node_name)

  def get_node(self, node_name):
    if node_name is None:
      return
    return self.nodes_dict[node_name]

  def is_leaf(self, node_name):
    if self.nodes_dict[node_name].left is None and self.nodes_dict[node_name].right is None:
      return True
    else:
      return False


class BTree:
  """
  Represents the B*-tree of a floorplan
  """

  def __init__(self, num_blocks):
    # print("Creating B*-tree")
    self.type = "Btree"
    self.num_nodes = num_blocks
    self.root = None
    self.nodes = Nodes(num_blocks)
    # self.blocks = blocks



  def build_leafs(self, block_list, parent=None, is_left=None):
    # random.shuffle(block_list)

    if not block_list:
      return None

    if len(block_list) > 1:
      new_name = block_list.pop()
      n = int(len(block_list) / 2) + 1

      left_tree = self.build_leafs(block_list[:n], parent=new_name, is_left=True)
      right_tree = self.build_leafs(block_list[n:], parent=new_name, is_left=False)
      return Node(new_name, parent=parent, is_left=is_left, left=left_tree, right=right_tree)

    new_name = block_list.pop()
    return Node(new_name, parent=parent, is_left=is_left, is_leaf=True)


  def build_tree(self, block_list):
    self.root = self.build_leafs(block_list)


  def print_tree(self, node=None, depth=0):
    if node is not None:
      print("  "*depth, node.name)
      self.print_tree(node.left, depth+1)
      self.print_tree(node.right, depth+1)


  def delete_node(self, nn):
    node = self.nodes[nn]
    if self.nodes.is_leaf(nn):
      if nn == self.nodes[node.parent].left.name:
        self.nodes[node.parent].left.name = None
      elif nn == self.nodes[node.parent].right is not None:
        self.nodes[node.parent].right.name = None

      node.name = None

    elif node.left is not None and node.right is None:
      self.nodes[node.left.name].parent = node.parent
      if node.parent is None:
        self.root = self.nodes[node.left.name]
      else:
        if nn == self.nodes[node.parent].left.name:
          self.nodes[node.parent].left.name = node.left.name
        else:
          self.nodes[node.parent].right.name = node.left.name
      node.left.name = node.right.name = node.parent = None

    elif node.left is None and node.right is not None:
      self.nodes[node.right.name].parent = node.parent
      if node.parent is None:
        self.root = self.nodes[node.right.name]
      else:
        if nn == self.nodes[node.parent].left.name:
          self.nodes[node.parent].left.name = node.right.name
        else:
          self.nodes[node.parent].right.name = node.right.name
      node.left.name = node.right.name = node.parent = None

    else:
      picked_left = random.uniform(0, 1)
      if picked_left < 0.5:
        self.swap_nodes(nn, self.nodes[nn.left.name])
      else:
        self.swap_nodes(nn, self.nodes[nn.right.name])
      delete_node(nn)



  def update_store(self, node=None, depth=0):
    if node is not None:
      self.nodes.nodes.append(node)
      self.nodes.nodes_dict[node.name] = node
      self.update_store(node.left, depth+1)
      self.update_store(node.right, depth+1)


  def swap_nodes(self, n1, n2):
    node1 = self.nodes[n1]
    node2 = self.nodes[n2]

    if n1 == n2:
      return

    if node1.parent != n2 and node2.parent != n1: # not connected
      self.__swap_node(n1, n2)
    else:
      val_n1 = True if n1 == node2.parent else False
      if val_n1:
        if node1.left.name == n2:
          node1.left.name = None
          isleft = True
        else:
          node1.right.name = None
          isleft = False

        node2.parent = n2

      else:
        if node2.left.name == n1:
          node2.left.name = None
          isleft = True
        else:
          node2.right.name = None
          isleft = False

        node1.parent = n1

      self.__swap_node_connected(n1, n2)

      if val_n1:
        node1.parent = n2
        if isleft:
          node1.left.name = n1
        else:
          node1.right.name = n1

      else:
        node2.parent = n1
        if isleft:
          node2.left.name = n2
        else:
          node2.right.name = n2


  def __swap_node_connected(self, n1, n2):

    node1 = self.nodes[n1]
    node2 = self.nodes[n2]

    if node1.left is not None:
      self.nodes[node1.left.name].parent = n2
    if node1.right is not None:
      self.nodes[node1.right.name].parent = n2

    if node2.left.name is not None:
      self.nodes[node2.left.name].parent = n1
    if node2.right is not None:
      self.nodes[node2.right.name].parent = n1

    if node1.parent != n1:
      if node1.parent is not None:
        p = self.nodes[node1.parent]
        if p.left.name == n1:
        # if p.left is not None:
          p.left.name = n2
        else:
          p.right.name = n2
      else:
        self.root.name = n2

    if node2.parent != n2:
      if node2.parent is not None:
        p = self.nodes[node2.parent]
        if p.left.name == n2:
        # if p.left is not None:
          p.left.name = n1
        else:
          p.right.name = n1
      else:
        self.root.name = n1

    node1.parent, node2.parent = node2.parent, node1.parent


  def __swap_node(self, n1, n2):
    node1 = self.nodes[n1]
    node2 = self.nodes[n2]

    if node1.left is not None:
      self.nodes[node1.left.name].parent = n2
    if node1.right is not None:
      self.nodes[node1.right.name].parent = n2

    if node2.left is not None:
      self.nodes[node2.left.name].parent = n1
    if node2.right is not None:
      self.nodes[node2.right.name].parent = n1

    if node1.parent != n1:
      if node1.parent is not None:
        p = self.nodes[node1.parent]
        if p.left.name == n1:
        # if p.left is not None:
          p.left.name = n2
        else:
          p.right.name = n2
      else:
        self.root.name = n2


    if node2.parent != n2:
      if node2.parent is not None:
        p = self.nodes[node2.parent]
        if p.left.name == n2:
        # if p.left is not None:
          p.left.name = n1
        else:
          p.right.name = n1
      else:
        self.root.name = n1

    node1.parent, node2.parent = node2.parent, node1.parent


  def extract_features(self):
    return np.arange(20)