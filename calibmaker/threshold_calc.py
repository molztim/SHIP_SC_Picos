# Vth = 1.5 * [VBG_ADJ * 0.3V] - 1.64/2 V + [0.00316/2 V * DVTH]

def simplethershold(VBG_ADJ,DVTH):
    Vth = 1.5 * (VBG_ADJ * 0.3) - (1.64/2 - (0.00316 / 2 * DVTH))
    print(f"{Vth} V")

# With 0 it works fine, at 13 its starts to jitter, 76 ist trigger way to fast
simplethershold(2,0)
simplethershold(2,30)
simplethershold(2,50)
    
def findthreshold(target):
    best_guess = [0,0,100]
    for VBG_ADJ in range(8):
        for DVTH in range(2**9):
            Vth = 1.5 * (VBG_ADJ * 0.3) - 1.64/2 + (0.00316 / 2 * DVTH)
            if abs(Vth - target) < abs(best_guess[-1] - target):
                best_guess = [VBG_ADJ,DVTH,Vth]
    print(f"Finished Guessing! VBG_ADJ {best_guess[0]}, DVTH: {best_guess[1]}, Target: {target}/{best_guess[2]} V")

findthreshold(0.)
findthreshold(0.1)
findthreshold(0.2)
findthreshold(0.3)
findthreshold(0.4)
findthreshold(0.5)
