import math
import json

def loss_cal(x):
    if x == 0:
        return 0
    a = -math.log(x/100) + 0.01
    if (x <= 2):
        return 5/a
    else:
        return 20/a
    
def bw_cal(x):
    return 1/(x + 0.01)

def delay_cal(x):
    return math.e*x/2



def read_info(switches):
    with open ("initial.txt", "r")as f:
        lst = f.read()
    print(lst)
    tmp = json.loads(lst)


    print(tmp)
    for i in tmp.values():
        switches.append(i)



def main(now12 = 0, now13 = 0, now23 = 0):
    switches = []
    #带宽 时延 丢包率   
    read_info(switches)
    smooth_switches = [[0,0,0],[0,0,0],[0,0,0]]
    bw = [0,0,0]
    delay = [0,0,0]
    loss = [0,0,0]

    switches[0][0] = switches[0][0] - now12
    switches[1][0] = switches[1][0] - now13
    switches[2][0] = switches[2][0] - now23



    for i in range (3):
        for j in range(2):
            smooth_switches[i][j] = math.log2(switches[i][j] + 1)

    for i in range(3):
        smooth_switches[i][2] = switches[i][2]

    # print(smooth_switches)

    total_bw = 0
    for i in range (3):
        total_bw += smooth_switches[i][0]**2
    total_bw = math.sqrt(total_bw)
    for i in range (3):
        bw[i] = smooth_switches[i][0]/total_bw

    total_delay = 0
    for i in range (3):
        total_delay += smooth_switches[i][1]**2
    total_delay = math.sqrt(total_delay)
    for i in range (3):
        delay[i] = smooth_switches[i][1]/total_delay

    total_loss = 0
    for i in range (3):
        total_loss += smooth_switches[i][2]**2
        loss[i] = smooth_switches[i][2]


    # print("100: ", loss_cal(100))
    # print("30: ", loss_cal(30))
    # print("0.2: ", loss_cal(0.2))

    for i in range(3):
        loss[i] = loss_cal(loss[i])
    for i in range (3):
        bw[i] = bw_cal(bw[i])
    for i in range (3):
        delay[i] = delay_cal(delay[i])

    print("bw: ", bw)
    print("delay: ", delay)
    print("loss: ",loss)

    weight = [100000, 100000, 100000]
    for i in range (3):
        weight[i] = delay[i] + bw[i]*loss[i] + 0.5
    return(weight)


weight1 = main(0.1, 0.1, 0.1)
print(weight1)

