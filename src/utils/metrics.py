def hpwl_net(net, blocks, pins):
  """
  Computes the hpwl of a net
  """
  comps = net.comp
  xs = []
  ys = []
  for comp_name in comps:
    if 'sb' in comp_name:
      comp = blocks[comp_name]
    elif 'p' in comp_name:
      comp = pins[comp_name]
    else:
      raise ValueError(f"The component {comp_name} is unknown")

    xs.append(comp.x)
    ys.append(comp.y)

  w = max(xs) - min(xs)
  h = max(ys) - min(ys)
  return w + h