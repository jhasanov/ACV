from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
import csv
import numpy as np


datasize=1750

def getdelta_e_cie2000(l1,a1,b1,l2,a2,b2):
    # Reference color.
    color1 = LabColor(lab_l=l1, lab_a=a1, lab_b=b1)
    # Color to be compared to the reference.
    color2 = LabColor(lab_l=l2, lab_a=a2, lab_b=b2)
    # This is your delta E value as a float.
    delta_e = np.round(delta_e_cie2000(color1, color2,Kl=1, Kc=1, Kh=1),5)
    
    return delta_e

def generate_6_values():
    input=list()
    for _ in range(0,6):
        a=np.random.random(1)[0]
        input.append(a)
    rounded=np.round(input,5)
    return rounded

def generate_inputs_csv(num):
    inputs=list()
    for _ in range(0,num):
        input=generate_6_values()
        inputs.append(input)
    with open("cielab2000_sample_input-{}.csv".format(num), "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(inputs)
    return inputs
    
def generate_outputs_csv(inputs, normalized=True):
    outputs=list()
    for i in inputs:
        l1,a1,b1,l2,a2,b2=i
        output=getdelta_e_cie2000(l1,a1,b1,l2,a2,b2)
        outputs.append(output)
    rounded_outputs=np.round(outputs,5)
    #normalizing against the max
    if normalized:
        norm=[float(k)/max(rounded_outputs) for k in rounded_outputs]
        outfile = open("cielab2000_sample_output-{}-normalized.csv".format(datasize), "w+", newline="")
        out = csv.writer(outfile)
        out.writerows(map(lambda x: [x], norm))
        outfile.close()
    outfile = open("cielab2000_sample_output-{}.csv".format(datasize), "w+", newline="")
    out = csv.writer(outfile)
    out.writerows(map(lambda x: [x], rounded_outputs))
    outfile.close()


generate_outputs_csv(generate_inputs_csv(datasize))










