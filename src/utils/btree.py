import random


class Node:
  """
  A node in the B*-tree
  """
  def __init__(self, name, parent=None, is_left=None, left=None, right=None):
    self.name = name
    self.parent = parent # only none if root
    self.left = left
    self.right = right
    self.is_leaf = None
    self.is_left = is_left


class BTree:
  """
  Represents the B*-tree of a floorplan
  """

  def __init__(self, num_blocks):
    print("Creating B*-tree")
    self.type = "Btree"
    self.num_nodes = num_blocks
    self.root = None
    # self.blocks = blocks


  def build_leafs(self, block_list, parent=None, is_left=None):
    random.shuffle(block_list)

    if not block_list:
      return None

    if len(block_list) > 1:
      new_name = block_list.pop()
      n = int(len(block_list) / 2)

      left_tree = self.build_leafs(block_list[:n], parent=new_name, is_left=True)
      right_tree = self.build_leafs(block_list[n:], parent=new_name, is_left=False)
      return Node(new_name, parent=parent, is_left=is_left, left=left_tree, right=right_tree)

    new_name = block_list.pop()
    return Node(new_name, parent=parent, is_left=is_left)


  def build_tree(self, block_list):
    self.root = self.build_leafs(block_list)


  def print_tree(self, node=None, depth=0):
    if node is not None:
      print("  "*depth, node.name)
      self.print_tree(node.left, depth+1)
      self.print_tree(node.right, depth+1)


  