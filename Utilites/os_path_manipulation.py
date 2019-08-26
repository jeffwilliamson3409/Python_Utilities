import sys
import os.path as op
#sys.path.insert(0, '/Users/jeffwilliamson1/Desktop/Proj1')


one_up = op.abspath(op.join(__file__, ".."))

print(one_up)

two_up = op.abspath(op.join(__file__, "../.."))

print(two_up)

three_up = op.abspath(op.join(__file__, "../../.."))

print(three_up)

