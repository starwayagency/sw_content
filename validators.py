
def validate_phone_number(number):
  if not number.startswith('+'):
    return False 
  if not len(number) == 13:
    return False 
  try:
    int(number[1:])
  except:
    return False 
  return True 

