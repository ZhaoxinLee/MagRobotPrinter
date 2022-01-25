import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()
kit2 = MotorKit(address=0x61)
kit3 = MotorKit(address=0x62)

class Stepper():
    def __init__(self):
        self.delay = 0.01
        self.direction_11 = stepper.FORWARD
        self.direction_21 = stepper.FORWARD
        self.direction_22 = stepper.FORWARD
        self.direction_31 = stepper.FORWARD
        self.direction_32 = stepper.FORWARD
        self.lastphi = 0
        self.lasttheta = 0
        self.lastalpha = 0
        self.lastbeta = 0
        
        #activate coils to hold the shafts of motors
#         kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
#         kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
#         kit2.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
#         kit2.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
#         kit2.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
#         kit2.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
#         kit3.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
#         kit3.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
#         kit3.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
#         kit3.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        
    def motorgo(self,phi,alpha21,alpha32,beta22,beta31):
        if phi > 0:
            self.direction_11 = stepper.FORWARD
        else:
            self.direction_11 = stepper.BACKWARD
            
        if alpha21 < 0:
            self.direction_21 = stepper.FORWARD
        else:
            self.direction_21 = stepper.BACKWARD
            
        if beta22 < 0:
            self.direction_22 = stepper.FORWARD
        else:
            self.direction_22 = stepper.BACKWARD
            
        if beta31 > 0:
            self.direction_31 = stepper.FORWARD
        else:
            self.direction_31 = stepper.BACKWARD
            
        if alpha32 > 0:
            self.direction_32 = stepper.FORWARD
        else:
            self.direction_32 = stepper.BACKWARD
            
        phi_steps = round(abs(phi*3.6)/0.9)#*3.6 is the gear transmission ratio
        alpha21_steps = round(abs(alpha21)/0.9)
        beta22_steps = round(abs(beta22)/0.9)
        beta31_steps = round(abs(beta31)/0.9)
        alpha32_steps = round(abs(alpha32)/0.9)
        for i in range(phi_steps):
            kit.stepper1.onestep(direction=self.direction_11, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for j in range(alpha21_steps):
            kit2.stepper1.onestep(direction=self.direction_21, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for k in range(alpha32_steps):
            kit3.stepper2.onestep(direction=self.direction_32, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for m in range(beta22_steps):
            kit2.stepper2.onestep(direction=self.direction_22, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for n in range(beta31_steps):
            kit3.stepper1.onestep(direction=self.direction_31, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
#         kit.stepper1.release()


    def fieldgo(self,phi,theta):
        
        if phi-self.lastphi > 0:
            self.direction_11 = stepper.FORWARD
        else:
            self.direction_11 = stepper.BACKWARD
            
        if theta-self.lasttheta > 0:
            self.direction_21 = stepper.FORWARD
            self.direction_32 = stepper.BACKWARD
            self.direction_31 = stepper.FORWARD
            self.direction_22 = stepper.BACKWARD
        else:
            self.direction_21 = stepper.BACKWARD
            self.direction_32 = stepper.FORWARD
            self.direction_31 = stepper.BACKWARD
            self.direction_22 = stepper.FORWARD
        
            
        phi_steps = round(abs((phi-self.lastphi)*3.6)/0.9)#*3.6 is the gear transmission ratio
        
        if theta >= 0 and theta <= 90:
            alpha = 0.0002468*theta**3-0.019*theta**2+0.76977*theta-2.1038
            beta = 0.0000755*theta**3-0.00357*theta**2+0.77157*theta-0.02957
        elif theta > 90:
            alpha = 180-(0.0002468*(180-theta)**3-0.019*(180-theta)**2+0.76977*(180-theta)-2.1038)
            beta = 180-(0.0000755*(180-theta)**3-0.00357*(180-theta)**2+0.77157*(180-theta)-0.02957)
        elif theta < 0 and theta >= -90:
            alpha = -(0.0002468*(-theta)**3-0.019*(-theta)**2+0.76977*(-theta)-2.1038)
            beta = -(0.0000755*(-theta)**3-0.00357*(-theta)**2+0.77157*(-theta)-0.02957)
        elif theta < -90:
            alpha = (0.0002468*(180+theta)**3-0.019*(180+theta)**2+0.76977*(180+theta)-2.1038)-180
            beta = (0.0000755*(180+theta)**3-0.00357*(180+theta)**2+0.77157*(180+theta)-0.02957)-180
            
        alpha21_steps = round(abs(alpha-self.lastalpha)/0.9)
        alpha32_steps = alpha21_steps
        beta22_steps = round(abs(beta-self.lastbeta)/0.9)
        beta31_steps = beta22_steps
        
        for i in range(phi_steps):
            kit.stepper1.onestep(direction=self.direction_11, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for j in range(alpha21_steps):
            kit2.stepper1.onestep(direction=self.direction_21, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for k in range(alpha32_steps):
            kit3.stepper2.onestep(direction=self.direction_32, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for m in range(beta22_steps):
            kit2.stepper2.onestep(direction=self.direction_22, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for n in range(beta31_steps):
            kit3.stepper1.onestep(direction=self.direction_31, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        
        self.storeval(phi,theta,alpha,beta)
        
        #calibrate pointing direction
        if theta == 0 and phi == 0:
            self.resetval()  
            
    def storeval(self,phi,theta,alpha,beta):
        self.lastphi = phi
        self.lasttheta = theta
        self.lastalpha = alpha
        self.lastbeta = beta
        
    def resetval(self):
        self.lastphi = 0
        self.lasttheta = 0
