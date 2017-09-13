

#modular design to allow other types of preprocessing. 

from declpreproc import * 



def preproc(filename):
  try:
    declpreproc(filename)
  except:
    print("maybe declarations have already been processed")

#test
filename = raw_input("enter filename")
preproc(str(filename))
