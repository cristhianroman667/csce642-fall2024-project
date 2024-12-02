from src.utils import Design
# from utils.metrics import hpwl

def main():

  des = Design('n10')
  des.parse()
  print('hpwl', des.get_hpwl())
  print('area', des._curArea)
  print('\n')

  print('swap operation')
  des.swap_blocks('sb7', 'sb0')
  print('hpwl', des.get_hpwl())
  print('area2', des._curArea)



if __name__ == "__main__":
    main()