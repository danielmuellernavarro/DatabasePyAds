
def convert_str_array_tc(s, lenghtString, sizeCols, fill=False):
  array_tc = bytes()
  for i, val in enumerate(s):  
    if i + 1 > sizeCols:
      break
    val = val[:lenghtString-1]
    val = bytes(val, 'utf-8')
    val += bytes(b'\x00'*(lenghtString - len(val)))
    array_tc += val
  if fill:
    total_len = lenghtString*sizeCols
    array_tc += bytes(b'\x00'*(total_len - len(array_tc)))
  return array_tc

def convert_str_array2D_tc(s, lenghtString, sizeCols, sizeRows):
  array_tc = bytes()
  for i, val in enumerate(s):  
    if i + 1 > sizeRows:
      break  
    col_tc = convert_str_array_tc(s=val, lenghtString=lenghtString, sizeCols=sizeCols, fill=True)
    len_col_tc = len(col_tc)
    array_tc += col_tc

  return array_tc

def convert_tc_str_array(s, lenght=81):
  for idx, x in enumerate(s):
    try:
      s[idx] = x.decode('utf-8')
    except:
      pass

  new = "" 
  jump_string = False
  for idx, x in enumerate(s):
    byte_idx = idx%lenght
    if x == '\x00':
      jump_string = True
    elif byte_idx == 0:
      jump_string = False
    if jump_string:
      continue
    new += x

  return new

def read_lenght(s, lenght=256, str_offset=0):
  offset = lenght*str_offset
  str_return = ""
  for idx, x in enumerate(s):
    if idx >= offset:
      x_str = x.decode('utf-8')
      if x_str == '\x00':
        break
      try:
        str_return = str_return + x_str
      except:
        pass
      if idx + offset == lenght:
        break

  return str_return

def convert_tc_config_var(s, nr_vars=1, lenght_var=81):
  for i in range(nr_vars):
    database = read_lenght(s, lenght=lenght_var, str_offset=i*2)
    type_database = read_lenght(s, lenght=lenght_var, str_offset=i*2 + 1)
    host = read_lenght(s, lenght=lenght_var, str_offset=i*2 + 2)
    user = read_lenght(s, lenght=lenght_var, str_offset=i*2 + 3)
    password = read_lenght(s, lenght=lenght_var, str_offset=i*2 + 4)
    if password == '':
      break
    return  {
      "database": database,
      "type_database": type_database,
      "host": host,
      "user": user,
      "password": password
      }