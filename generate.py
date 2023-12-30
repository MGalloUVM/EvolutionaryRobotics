import pyrosim.pyrosim as pyrosim

# Create our world
def Create_World():
    # Set output file's name
    pyrosim.Start_SDF("world.sdf")
    # Define cube dimensions (L, W, H)
    cube_dim = (1, 1, 1)
    # Define cube positions (X, Y, Z)
    cube_pos = (-5, 5, cube_dim[2]/2)
    # Write to output
    pyrosim.Send_Cube(
        name="Torso",
        pos=[cube_pos[0], cube_pos[1], cube_pos[2]],
        size=[cube_dim[0], cube_dim[1], cube_dim[2]])
    # Close file
    pyrosim.End()


# Create our Robot
def Create_Robot():
    # Define output file for URDF writing
    pyrosim.Start_URDF("body.urdf")

    # Define dimensions (L, W, H)
    torso_dim = (1, 1, 1)
    # Define positions (X, Y, Z) ABSOLUTE
    torso_pos = (0, 0, 0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="Link0",
        pos=[torso_pos[0], torso_pos[1], torso_pos[2]],
        size=[torso_dim[0], torso_dim[1], torso_dim[2]])
    
    # Define dimensions (L, W, H)
    leg_dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    leg_pos = (0, 0, 0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="Link1",
        pos=[leg_pos[0], leg_pos[1], leg_pos[2]],
        size=[leg_dim[0], leg_dim[1], leg_dim[2]])
    
    # Define dimensions (L, W, H)
    leg_dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    leg_pos = (0, 0, 0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="Link2",
        pos=[leg_pos[0], leg_pos[1], leg_pos[2]],
        size=[leg_dim[0], leg_dim[1], leg_dim[2]])
    
    # Define dimensions (L, W, H)
    leg_dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    leg_pos = (0, 0.5, 0)
    # Write to output
    pyrosim.Send_Cube(
        name="Link3",
        pos=[leg_pos[0], leg_pos[1], leg_pos[2]],
        size=[leg_dim[0], leg_dim[1], leg_dim[2]])
    
    # Define dimensions (L, W, H)
    leg_dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    leg_pos = (0, 0.5, 0)
    # Write to output
    pyrosim.Send_Cube(
        name="Link4",
        pos=[leg_pos[0], leg_pos[1], leg_pos[2]],
        size=[leg_dim[0], leg_dim[1], leg_dim[2]])
    
    # Define dimensions (L, W, H)
    leg_dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    leg_pos = (0, 0, -0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="Link5",
        pos=[leg_pos[0], leg_pos[1], leg_pos[2]],
        size=[leg_dim[0], leg_dim[1], leg_dim[2]])
    
    # Define dimensions (L, W, H)
    leg_dim = (1, 1, 1)
    # Define positions (X, Y, Z) RELATIVE
    leg_pos = (0, 0, -0.5)
    # Write to output
    pyrosim.Send_Cube(
        name="Link6",
        pos=[leg_pos[0], leg_pos[1], leg_pos[2]],
        size=[leg_dim[0], leg_dim[1], leg_dim[2]])

    # Define our Torso_Leg joint
    pyrosim.Send_Joint(
        name = "Link0_Link1",
        parent= "Link0", child = "Link1",
        type = "revolute",
        position = [0, 0, 1]) 
    
    pyrosim.Send_Joint(
        name = "Link1_Link2",
        parent= "Link1", child = "Link2",
        type = "revolute",
        position = [0, 0, 1]) 

    pyrosim.Send_Joint(
        name = "Link2_Link3",
        parent= "Link2", child = "Link3",
        type = "revolute",
        position = [0, 0.5, 0.5]) 
    
    pyrosim.Send_Joint(
        name = "Link3_Link4",
        parent= "Link3", child = "Link4",
        type = "revolute",
        position = [0, 1, 0]) 
    
    pyrosim.Send_Joint(
        name = "Link4_Link5",
        parent= "Link4", child = "Link5",
        type = "revolute",
        position = [0, 0.5, -0.5])

    pyrosim.Send_Joint(
        name = "Link5_Link6",
        parent= "Link5", child = "Link6",
        type = "revolute",
        position = [0, 0, -1])
    # Close file
    pyrosim.End()


Create_World()
Create_Robot()