import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper


kit = MotorKit(address=0x61)

class Stepper():
    def __init__(self):
        self.delay = 0.01
        self.direction_11 = stepper.FORWARD
        self.direction_12 = stepper.FORWARD

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
        
    def motorgo(self,phi,theta):
        if phi > 0:
            self.direction_11 = stepper.FORWARD
        else:
            self.direction_11 = stepper.BACKWARD
            
        if theta < 0:
            self.direction_12 = stepper.FORWARD
        else:
            self.direction_12 = stepper.BACKWARD
            
        phi_steps = round(abs(phi*2.7)/0.9)#*2.7 is the gear transmission ratio
        theta_steps = round(abs(theta)/0.9)
        
        for i in range(phi_steps):
            kit.stepper1.onestep(direction=self.direction_11, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for j in range(theta_steps):
            kit.stepper2.onestep(direction=self.direction_12, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
#         kit.stepper1.release()


    def fieldgo(self,phi,theta):
        
        if phi-self.lastphi > 0:
            self.direction_11 = stepper.FORWARD
        else:
            self.direction_11 = stepper.BACKWARD
            
        if theta-self.lasttheta > 0:
            self.direction_12 = stepper.FORWARD
        else:
            self.direction_12 = stepper.BACKWARD
        
        beta = phi   
        beta_steps = round(abs((phi-self.lastphi)*2.7)/0.9)#*2.7 is the gear transmission ratio
        
        if theta >= 0 and theta <= 90:
            alpha = 0.0001379*theta**3-0.0258*theta**2+2.206*theta-0.174
        elif theta > 90:
            alpha = 180-(0.0001379*(180-theta)**3-0.0258*(180-theta)**2+2.206*(180-theta)-0.174)
        elif theta < 0 and theta >= -90:
            alpha = -(0.0001379*(-theta)**3-0.0258*(-theta)**2+2.206*(-theta)-0.174)
        elif theta < -90:
            alpha = (0.0001379*(180+theta)**3-0.0258*(180+theta)**2+2.206*(180+theta)-0.174)-180

            
        alpha_steps = round(abs(alpha-self.lastalpha)/0.9)

        
        for i in range(beta_steps):
            kit.stepper1.onestep(direction=self.direction_11, style=stepper.INTERLEAVE)
            time.sleep(self.delay)
        for j in range(alpha_steps):
            kit.stepper2.onestep(direction=self.direction_12, style=stepper.INTERLEAVE)
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
