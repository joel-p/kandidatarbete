import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

def generate_data(dimensions, pattern_input_amount=0, pattern_input_length=0):
    dataList = []

    for i in range(dimensions):
        baseData = np.random.choice([0, 1], size=dimensions, p=[.5, .5])

        dataList.append(baseData)

    if pattern_input_amount > 0: #Inserts repeated 0/1 to reduce complexity
        binary = 0
        for i in range(pattern_input_amount):
            row = random.randint(0, dimensions - 1)
            col = random.randint(0, dimensions - pattern_input_length)
            binary = 1 if binary == 0 else 1 #Alternate between filling and not filling pixel
            for j in range(pattern_input_length):
                dataList[row][col + j] = binary

    return np.array(dataList)

def get_ag_complexity(data):
    r = robjects.r
    r['source']('2D_optim.R')

    ag_complexity_func = robjects.globalenv['Array_complexity']

    rpy2.robjects.numpy2ri.activate()
    nr,nc = data.shape
    matrix = robjects.r.matrix(data, nrow=nr, ncol=nc)
    robjects.r.assign("Array_complexity", matrix)

    return ag_complexity_func(matrix)[0]

def generate_image(data, target_ag, name):
    file_name = f"AG{str(target_ag)}_{name}"
    file_path = f"_generated/{file_name}.png"
    plt.imsave(file_path, data, cmap='binary')

    img = cv2.imread(file_path)
    res = cv2.resize(img, dsize=(500, 500), interpolation=cv2.INTER_NEAREST)

    plt.imsave(f"_generated/{file_name}.png", res)

def generate_data_from_file(file):
    return np.genfromtxt(file, delimiter=1, dtype=np.int8)



def process_file(file_name):
    data = generate_data_from_file(file_name)

    ag_complexity = get_ag_complexity(data)
    print("AG: " + str(ag_complexity))
    generate_image(data, "test")

def generate(dimensions, target_ag, name, pattern_input_amount=0, pattern_input_length=0):
    ag_complexity = 0
    data = generate_data(dimensions)
    #count = 0

    while (ag_complexity - target_ag + 1) > 1.3 or (ag_complexity - target_ag + 1) < 0.7: #Allowing a margin of 0.3 from target
        data = generate_data(dimensions, pattern_input_amount, pattern_input_length)
        ag_complexity = get_ag_complexity(data)
        print(ag_complexity)
        #count += 1
        #if count == 100:
            #print("Increasing dimension...")
            #dimensions += 1
            #count = 0

    print("AG: " + str(ag_complexity))
    generate_image(data, target_ag, name)

target_ag = 1

while target_ag > 0:
    target_ag = int(input("Target AG (0 to quit): "))
    file_name = str(input("Filename: "))

    #2
    if target_ag == 2:
        generate(6, target_ag, file_name)

    #8
    if target_ag == 4:
        generate(10, target_ag, file_name)

    #8
    if target_ag == 6:
        generate(13, target_ag, file_name)

    #8
    if target_ag == 8:
        generate(16, target_ag, file_name)

    #10
    elif target_ag == 10:
        generate(19, target_ag, file_name)

    #12
    elif target_ag == 12:
        generate(22, target_ag, file_name)

    #14
    elif target_ag == 14:
        generate(26, target_ag, file_name)

    #16
    elif target_ag == 16:
        generate(29, target_ag, file_name)

    #18
    elif target_ag == 18:
        generate(32, target_ag, file_name)

    #20
    elif target_ag == 20:
        generate(35, target_ag, file_name)

    #22
    elif target_ag == 22:
        generate(38, target_ag, file_name)

    #24
    elif target_ag == 24:
        generate(41, target_ag, file_name)

    #26
    elif target_ag == 26:
        generate(44, target_ag, file_name)

    #28
    elif target_ag == 28:
        generate(47, target_ag, file_name)

    #30
    elif target_ag == 30:
        generate(50, target_ag, file_name)

# process_file("8. Disorder/D_10.txt")

