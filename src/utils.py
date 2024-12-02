from .metrics import hpwl_net
from .btree import BTree

class Pin:
  """
  Class Pin that represents the individual terminal
  """

  def __init__(self, name):
    self.type = "PIN"
    self.name = name
    self.x = None
    self.y = None
    self.placed = None

  def __str__(self):
    s = ""
    s += self.type + ": " + self.name + "\n"
    return s


class Pins:
  """
  Class Pins represents the collection of Pins
  """

  def __init__(self, num_pins):
    self.type = "PINS"
    self.num_pins = num_pins
    self.pins = []
    self.pins_dict = {}

  def __len__(self):
    return len(self.pins)

  def __iter__(self):
    return self.pins.__iter__()

  def __getitem__(self, pin_name):
    return self.get_pin(pin_name)

  def get_pin(self, pin_name):
    return self.pins_dict[pin_name]


class Block:
  """
  Represents individual block in the bench
  """

  def __init__(self, name):
    self.type = "BLOCK"
    self.name = name
    self.w = None
    self.h = None
    self.x = None
    self.y = None
    self.rotated = False

  def __str__(self):
    s = ""
    s += self.type + ": " + self.name + "\n"
    return s


class Blocks:
  """
  Class Blocks represents the blocks in the bench
  """

  def __init__(self, num_blocks):
    self.type = "BLOCKS"
    self.num_blocks = num_blocks
    self.blocks = []
    self.blocks_dict = {}

  def __len__(self):
    return len(self.blocks)

  def __getitem__(self, block_name):
    return self.get_block(block_name)

  def __iter__(self):
    return self.blocks.__iter__()

  def get_block(self, block_name):
    return self.blocks_dict[block_name]


class Net:
  """
  Represents individual net in the bench
  """
  def __init__(self, name):
    self.type = "NET"
    self.name = name
    self.comp = []

  def __str__(self):
    s = ""
    s += self.type + ": " + self.name + "\n"
    return s


class Nets:
  """
  Class Nets represents the nets in the bench
  """

  def __init__(self, num_nets):
    self.type = "NETS"
    self.num_nets = num_nets
    self.nets = []
    self.nets_dict = {}


  def __iter__(self):
    return self.nets.__iter__()

  def __len__(self):
    return len(self.nets)

  def __getitem__(self, net_name):
    return self.get_net(net_name)

  def get_net(self, net_name):
    return self.nets_dict[net_name]


class Contour():
  """
  Represents the contour of the btree
  """
  def __init__(self, block, pprev, nnext):
    self.type = "CONTOUR"
    self.data = block
    self.pprev = pprev
    self.nnext = nnext


class Design:
  """
  Design reads the parsed files and store information
  """

  def __init__(self, bench_name):
    self.bench_name = bench_name
    self.blocks_path = self.bench_name + "_block.csv"
    self.nets_path = self.bench_name + "_nets.csv"
    self.terminals_path = self.bench_name + "_terminal.csv"

    self.pins = None
    self.nets = None
    self.blocks = None
    self.block_list = None
    self.btree =  None

    # btree variables
    self._conRoot = None
    self._yContour = {}
    self._curWidth = None
    self._curHeight = None
    self._curArea = None


  def parse(self):
    print("Start parsing " + self.bench_name + "...")
    self.blocks = Blocks(int(self.bench_name[1:]))
    self.parse_blocks(self.blocks_path)
    self.block_list = list(self.blocks.blocks_dict.keys())

    self.pins = Pins(0)
    self.parse_pins(self.terminals_path)

    self.nets = Nets(0)
    self.parse_nets(self.nets_path)

    self.btree = BTree(self.blocks.num_blocks)
    self.btree.build_tree(self.block_list)
    self.btree.update_store(self.btree.root) # this two go together
    self.pack()  # this two go together


  def swap_blocks(self, n1, n2):
    self.btree.swap_nodes(n1, n2)
    self.btree.update_store(self.btree.root)
    self.pack()


  def unpack(self):
    self._conRoot = None
    self._yContour = {}
    for block in self.blocks:
      self._yContour[block.name] = Contour(None, None, None)


  def pack(self):
    self.unpack()
    self.DFSPack(self.btree.root)
    self.updateFP()


  def updateFP(self):
    width = 0
    height = 0
    for key, value in self._yContour.items():
      block = self.blocks[key]
      x = block.w if not block.rotated else block.h
      y = block.h if not block.rotated else block.w

      width = max(width, block.x + x)
      height = max(height, block.y + y)
    
    self._curWidth = width
    self._curHeight = height
    self._curArea = height * width


  def place_block(self, node):
    block = self.blocks[node.name]

    if node.parent is None:
      block.x = 0
      block.y = 0
      self._conRoot = node.name
      self._yContour[node.name] = Contour(block, None, None)

    elif node.parent is not None and node.is_left:
      pb = self.blocks[node.parent]
      w = pb.w if not pb.rotated else pb.h
      block.x = self.blocks[node.parent].x + w
      block.y = self.update_contour(node, node.parent, True)

    elif node.parent is not None and not node.is_left:
      pb = self.blocks[node.parent]
      block.x = pb.x
      block.y = self.update_contour(node, node.parent, False)


  def update_contour(self, node, parent, is_left):
    block = self.blocks[node.name]
    maxh = 0
    lpos = 0
    rpos = 0
    lx = block.x
    nx = block.w if not block.rotated else block.h
    rx = lx + nx

    attach = None
    start = self._yContour[parent].nnext if is_left else parent
    c = start
    while c is not None:
      b = self._yContour[c].data
      w = b.w if not b.rotated else b.h
      h = b.h if not b.rotated else b.w

      lpos = b.x
      rpos = lpos + w
      
      if lpos < rx and rpos <= rx:
          maxh = max(maxh, b.y + h)
      elif lpos < rx and rpos > rx:
          maxh = max(maxh, b.y + h)
          attach = c
          break
      else:
          attach = c
          break
      
      c = self._yContour[c].nnext

    if start is None:
      self._yContour[parent].nnext = node.name
      self._yContour[node.name].pprev = parent
      self._yContour[node.name].nnext = None
      self._yContour[node.name].data = block
    else:
      con = parent if is_left else self._yContour[parent].pprev
      if con is None:
        self._conRoot = node.name
      else:
        self._yContour[con].nnext = node.name

      self._yContour[node.name].pprev = con
      self._yContour[node.name].nnext = attach
      self._yContour[node.name].data = block

    return maxh




  def DFSPack(self, node):
    self.place_block(node)
    if node.left is not None:
      self.DFSPack(node.left)

    if node.right is not None:
      self.DFSPack(node.right)


  def parse_nets(self, path):
    print("Parsing net file")
    f = open(path, "r+")
    f.readline()
    tmp = ""
    for line in f:
      info = line.split("\n")
      info = info[0].split(",")

      if tmp != info[0]:
        tmp = info[0]
        new_net = Net(info[0])

        new_net.comp.append(info[1])

        self.nets.nets.append(new_net)
        self.nets.nets_dict[info[0]] = new_net

      else:
        new_net.comp.append(info[1])

    self.nets.num_nets = len(self.nets)
    f.close()


  def parse_pins(self, path):
    print("Parsing terminal file")
    f = open(path, "r+")
    f.readline()
    for line in f:
      info = line.split("\n")
      info = info[0].split(",")
      new_pin = Pin(info[0])

      new_pin.x = int(info[1])
      new_pin.y = int(info[2])
      new_pin.placed = True

      self.pins.pins.append(new_pin)
      self.pins.pins_dict[info[0]] = new_pin

    self.pins.num_pins = len(self.pins) 
    f.close()



  def parse_blocks(self, path):
    print("Parsing block file")
    f = open(path, "r+")
    f.readline()
    for line in f:
      info = line.split("\n")
      info = info[0].split(",")
      new_block = Block(info[0])

      new_block.w = int(info[1])
      new_block.h = int(info[2])
      new_block.x = int(info[3])
      new_block.y = int(info[4])

      self.blocks.blocks.append(new_block)
      self.blocks.blocks_dict[info[0]] = new_block

    f.close()



  def get_hpwl(self):
    total_hpwl = 0
    for net in self.nets:
      total_hpwl += hpwl_net(net, self.blocks, self.pins)

    return total_hpwl


