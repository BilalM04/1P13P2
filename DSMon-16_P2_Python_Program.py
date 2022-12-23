ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

import random

containers_remaining = [1, 2, 3, 4, 5, 6] #list to keep track of containers remaining
containers_moved = [] #list to keep track of containers that have already been moved

def main():
    while not(terminate_program()):
        if (potentiometer.right() == 0.5 and potentiometer.left() == 0.5):
            run_program = True #program runs if both potentiometers are set to 50%
        else:
            run_program = False 

        if (run_program):
            container_id = containers_remaining[int(random.random() * len(containers_remaining))] #gets random container id from containers_remaining list
            arm.spawn_cage(container_id) #spawns cage
            time.sleep(2)
            pick_up_container(container_id) #calls function to pickup container
            #calls rotate_base() function and changes parameter based on container id
            if (container_id == 1 or container_id == 4):
                rotate_base('red')
            elif (container_id == 2 or container_id == 5):
                rotate_base('green')
            elif (container_id == 3 or container_id == 6):
                rotate_base('blue')
            drop_off_container(container_id) #call function to drop off the container
            containers_remaining.remove(container_id) #removes the container id from the containers_remaining list
            containers_moved.append(container_id) #adds container id to the containers_moved list
            run_program = False
            print("set left and right potentiometers to 50%") #instructions for user so the next container can spawn and be moved

    print("task completed.") #prints prompt when all containers have been dropped off
    

def pick_up_container(container_id):
    print('picking up cage...') #prints status to console
    arm.move_arm(0.425, 0.025, -0.212) #moves arm to pickup location
    time.sleep(2)
    if container_id > 3:
        arm.control_gripper(25) #close the gripper slightly if container is large
    else:
        arm.control_gripper(34) #close the gripper more if container is small
    time.sleep(2)
    arm.move_arm(0.406, 0.0, 0.483) #move arm back to home position
    

def rotate_base(colour):
    print("rotate right potentiometer")
    arm_deg = 0
    
    while not(arm.check_autoclave(colour)):
        if (potentiometer.right() < 0.5):
            rotation = (0.5 - potentiometer.right()) * 350 - arm_deg #determines the amount of rotation based on potentiometer and arm's current position
            arm.rotate_base(rotation)#rotates QArm base counter clockwise
            if (rotation != 0):
                arm_deg += rotation #keeps track of QArm's base rotation
        elif (potentiometer.right() > 0.5):
            rotation = (potentiometer.right() - 0.5) * -350 - arm_deg #determines the amount of rotation based on potentiometer and arm's current position
            arm.rotate_base(rotation) #rotates QArm base clockwise
            if (rotation != 0):
                arm_deg += rotation #keeps track of QArm's base rotation
                
               
def drop_off_container(container_id):
    if (container_id < 4):
        print("set left potentiometer to between 50% and 100%") #instructions for small container
    else:
        print("set left potentiometer to 100%") #instructuions for large container

    while True:
        if (potentiometer.left() > 0.5 and potentiometer.left() < 1.0 and container_id < 4):
            print("dropping off cage...")

            #determines drop off location by scanning the colour of the autoclave
            if arm.check_autoclave('red'):
                arm.move_arm(0, 0.610, 0.275) #moves arm above red container
            elif arm.check_autoclave('blue'):
                arm.move_arm(0, -0.610, 0.275) #moves arm above blue container
            elif arm.check_autoclave('green'):
                arm.move_arm(-0.645, 0.245, 0.275) #moves arm above green container

            time.sleep(2)
            arm.control_gripper(-34) #arm drops container on top of box
            time.sleep(2)
            print("returning home...")
            arm.home() #arm returns home
            break
            
        elif (potentiometer.left() == 1.0 and container_id > 3):
            arm.activate_autoclaves() 
            print("dropping off cage...")

            #determines drop off location by scanning the colour of the autoclave
            if arm.check_autoclave('red'):
                arm.open_autoclave('red') #opens red drawer
                time.sleep(2)
                arm.move_arm(0, 0.400, 0.250) #moves arm above red drawer
                time.sleep(2)
                arm.control_gripper(-25) #arm drops container
                time.sleep(2)
                arm.open_autoclave('red', False) #closes red drawer
                
            elif arm.check_autoclave('blue'):
                arm.open_autoclave('blue') #opens blue drawer
                time.sleep(2)
                arm.move_arm(0, -0.400, 0.250) #moves arm above blue drawer
                time.sleep(2)
                arm.control_gripper(-25) #arm drops container
                time.sleep(2)
                arm.open_autoclave('blue', False) #closes blue drawer
                
            elif arm.check_autoclave('green'):
                arm.open_autoclave('green') #opens green drawer
                time.sleep(2)
                arm.move_arm(-0.390, 0.185, 0.250) #moves arm above green drawer
                time.sleep(2)
                arm.control_gripper(-25) #arm drops container
                time.sleep(2)
                arm.open_autoclave('green', False) #closes green drawer

            arm.deactivate_autoclaves()
            time.sleep(2)
            print("returning home...")
            arm.home() #arm returns to home position
            break

def terminate_program():
    return (len(containers_moved) == 6) #if all containers have been moved (list size is 6), then program can terminate

main()

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

