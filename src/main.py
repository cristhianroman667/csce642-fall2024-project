from utils.utils import Design
# from utils.metrics import hpwl

def main():

  des = Design('n10')
  des.parse()
  hpwl = des.get_hpwl()
  print('hpwl', hpwl)

  area = des._curArea
  print('area', area)

  des.pack()
  des.btree
  hpwl = des.get_hpwl()
  print('hpwl2', hpwl)

  area = des._curArea
  print('area2', area)

  # des.btree.build_tree(list(des.blocks.blocks_dict.keys()))
  # des.btree.print_tree(des.btree.root)



if __name__ == "__main__":
    main()