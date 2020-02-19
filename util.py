class Order(Enum):
    descending = 0
    ascending = 1

def sortList(list, element, order):
    output = list.copy()
    if(order == Order.ascending):
        for i in range(0, len(output)):
            for j in range(0, len(output)):
                if output[i][element] < output[j][element]:
                    temp = output[i]
                    output[i] = output[j]
                    output[j] = temp
    elif(order == Order.descending):
        for i in range(0, len(output)):
            for j in range(0, len(output)):
                if output[i][element] > output[j][element]:
                    temp = output[i]
                    output[i] = output[j]
                    output[j] = temp   
    return output