from src.utils import Design

def main():

  des = Design('n10')
  des.parse()
  print('\thpwl', des.get_hpwl())
  print('\tarea', des._curArea)
  des.btree.print_tree(des.btree.root)


  print('swap operation', 'sb9', 'sb6')
  des.swap_blocks('sb9', 'sb6')
  print('\thpwl', des.get_hpwl())
  print('\tarea', des._curArea)

  print('rotation operation', 'sb9')
  des.rotate_block('sb9')
  print('\thpwl', des.get_hpwl())
  print('\tarea', des._curArea)

if __name__ == "__main__":
    main()