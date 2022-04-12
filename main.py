import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
import numpy as np
import matplotlib.pyplot as plt
import cv2

def generate_data(dimensions, chunk_size):
    dataList = []

    calculated_size = int(dimensions/chunk_size)

    for i in range(calculated_size):
        baseData = np.random.choice([0, 1], size=calculated_size, p=[.5, .5])

        dataList.append(baseData)

    binaryData = np.kron(np.array(dataList), np.ones((chunk_size,chunk_size), dtype=np.array(dataList).dtype))
    return binaryData

def get_ag_complexity(data):
    r = robjects.r
    r['source']('2D_optim.R')

    # Loading the function we have defined in R.
    ag_complexity_func = robjects.globalenv['Array_complexity']

    rpy2.robjects.numpy2ri.activate()
    nr,nc = data.shape
    matrix = robjects.r.matrix(data, nrow=nr, ncol=nc)
    robjects.r.assign("Array_complexity", matrix)

    return ag_complexity_func(matrix)[0]

def generate_image(data, target_ag):
    file_path = '_generated/' + str(target_ag) + '.bmp'
    plt.imsave(file_path, data, cmap='binary')

    img = cv2.imread(file_path)
    res = cv2.resize(img, dsize=(500, 500), interpolation=cv2.INTER_NEAREST)

    plt.imsave('_generated/' + str(target_ag) + '_highres.bmp', res)

def generate_data_from_file(file):
    return np.genfromtxt(file, delimiter=1, dtype=np.int8)




def process_file(file_name):
    data = generate_data_from_file(file_name)

    ag_complexity = get_ag_complexity(data)
    print("AG: " + str(ag_complexity))
    generate_image(data, "test")

def generate(dimensions, chunk_size, target_ag):
    ag_complexity = 0
    data = generate_data(dimensions, chunk_size)
    count = 0

    while (ag_complexity - target_ag + 1) > 1.1 or (ag_complexity - target_ag + 1) < 0.9: #Allowing a margin of 0.1 from target
        data = generate_data(dimensions, chunk_size)
        ag_complexity = get_ag_complexity(data)
        print(ag_complexity)
        count += 1
        if count == 100:
            print("Increasing dimension...")
            dimensions += 1
            count = 0

    print("AG: " + str(ag_complexity))
    generate_image(data, target_ag)


target_ag = 1

while target_ag > 0:
    target_ag = int(input("Target AG (0 to quit): "))

    if target_ag == 2:
        generate(9, 4, target_ag)
    elif target_ag == 4:
        generate(12, 4, target_ag)
    elif target_ag == 6:
        generate(16, 4, target_ag)
    elif target_ag == 8:
        generate(20, 4, target_ag)
    elif target_ag == 10:
        generate(24, 4, target_ag)
    elif target_ag == 15:
        generate(32, 4, target_ag)
    elif target_ag == 20:
        generate(42, 4, target_ag)
    elif target_ag == 31:
        generate(56, 4, target_ag)
    elif target_ag == 60:
        generate(100, 4, target_ag)


process_file("8. Disorder/D_10.txt")