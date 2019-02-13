'''

'''
import math
import ctypes
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..RCMath.Algebra import angle_between, normalize, rotation_matrix

import time

class Simulator(QObject):

    ''' ---------------------- Private local class ---------------------- '''

    class Cars_props():
        def __init__(self):
            self.current_segment       = 0
            self.local_scalar_position = 0.0
            self.scalar_velocity       = 0.0
            self.basis                 = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
            self.rot_basis             = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
            self.position_vector       = np.array([0.0, 0.0, 0.0])
            self.arrived_end           = False

    ''' ---------------------- Public ---------------------- '''

    ## initialization
    def __init__(self, constructor, cars, **kwargs):
        super(Simulator, self).__init__()

        # Updating data
        self._contructor_obj = constructor
        self._cars_manager   = cars

        ''' --------- Public --------- '''
        self.simulating = False

        """ --------- Simulator Properties --------- """
        self._cars_prop = []
        self._cars_obj  = []
        self._segments  = []

        self._fp = False


    def start(self):
        # It is simulating
        self.simulating = True

        # Set up cars and segments
        self._segments  = self._contructor_obj.get_rails()
        self._cars_obj  = self._cars_manager.get_cars()
        self._cars_prop = []
        n = len(self._cars_obj)
        for i in range(0, n):
            self._cars_prop.append(self.Cars_props())

        # Calculate positions
        for i in range(0, n):
            self.scalar_to_vector_position((n-1-i), 0.6 + 1.3*i)
            self.transform((n-1-i))
            self._cars_obj[i].should_be_rendered = not self._fp

        self._start_time = time.time()


    def stop(self):
        # It is not simulating
        self.simulating = False
        for i in range(0, len(self._cars_prop)):
            self._cars_obj[i].should_be_rendered = False
        # Free arrays
        self._segments  = []
        self._cars_obj  = []
        for i in range(0, len(self._cars_prop)):
            self._cars_prop[i] = None
        self._cars_prop = []


    def step(self):
        now = time.time()
        dt = now - self._start_time
        self._start_time = now

        for i in range(0, len(self._cars_obj)):
            self.calculate_local_step(i, dt)
        self.average_step(dt)
        for i in range(0, len(self._cars_obj)):
            self.transform(i)

    def update_fp(self, fp):
        self._fp = fp
        for i in range(0, len(self._cars_prop)):
            self._cars_obj[i].should_be_rendered = not fp


    ''' ---------------------- Private ---------------------- '''

    def scalar_to_vector_position(self, i, scalar_position):
        # Presets
        car = self._cars_prop[i]
        seg_id = car.current_segment
        n = len(self._segments)

        # Calculate in what segment the car is and where in the 3D space
        local_scalar_pos = car.local_scalar_position + scalar_position
        is_in_rail = self._segments[seg_id].position_in_rail(local_scalar_pos)
        offset = 0.0
        # Before segment
        while(isinstance(is_in_rail, int) and is_in_rail == -2):
            seg_id -= 1
            seg_id = seg_id%n
            offset = self._segments[seg_id]._length
            local_scalar_pos += offset
            is_in_rail = self._segments[seg_id].position_in_rail(local_scalar_pos)
        # After segment
        while(isinstance(is_in_rail, int) and is_in_rail == -1):
            offset = self._segments[seg_id]._length
            seg_id += 1
            seg_id = seg_id%n
            local_scalar_pos -= offset
            is_in_rail = self._segments[seg_id].position_in_rail(local_scalar_pos)

        # Update car properties
        car.current_segment  = seg_id
        car.local_scalar_position = local_scalar_pos
        car.position_vector  = is_in_rail
        car.basis            = self._segments[seg_id].get_basis_in(local_scalar_pos)
        car.rot_basis        = self._segments[seg_id].get_rot_basis_in(local_scalar_pos)


    def transform(self, i):
        # Presets
        car_prop = self._cars_prop[i]
        car_obj  = self._cars_obj[i]
        transform = QMatrix4x4()

        # Position
        pos = car_prop.position_vector
        transform.translate(float(pos[0]), float(pos[1]), float(pos[2]))

        # Rotation (local)
        for i in range(0, 3):
            for j in range(0, 3):
                transform[i, j] = car_prop.rot_basis[i, j]

        # Assign the transformation to the car
        car_obj._transform = transform


    def calculate_local_step(self, i, dt):
        # Presets
        car      = self._cars_prop[i]
        seg      = self._segments[car.current_segment]

        # Aceleration calculation
        aceleration = self.aceleration_calculation(seg, car)

        # Scalar velocity calculation
        aceleration = aceleration
        car.scalar_velocity += aceleration * dt


    def aceleration_calculation(self, seg, car):
        # Presets
        car_vel  = car.scalar_velocity
        car_pos  = car.local_scalar_position
        seg_tg   = seg.tangent(car_pos)
        seg_type = seg._type

        min_vel = 3.0
        max_vel = 3.0


        aceleration = 0.0

        # Platform
        if(seg_type == 0):
            if(car_vel < max_vel):
                aceleration = 5.0

        # Normal
        elif(seg_type == 1):
            g = np.array([0.0, -1.0, 0.0])
            aceleration = np.dot(g, seg_tg)*9.8 - car_vel*0.1

        # Lever
        elif(seg_type == 2):
            if(car_vel < max_vel):
                aceleration = 5.0
            else:
                g = np.array([0.0, -1.0, 0.0])
                aceleration = np.dot(g, seg_tg)*9.8 - car_vel*0.1

        # Brakes
        elif(seg_type == 3):
            if(car_vel > min_vel):
                aceleration = -5.0
            else:
                g = np.array([0.0, -1.0, 0.0])
                aceleration = np.dot(g, seg_tg)*9.8 - car_vel*0.1

        # Final
        elif(seg_type == 4):
            car.arrived_end = True
            if(car_vel > 0.01):
                aceleration = -20.0
            else:
                aceleration = 0.0

        return(aceleration)


    def average_step(self, dt):
        n = len(self._cars_prop)
        arrived_end = False
        # Calculate the average velocity
        average_vel = 0.0
        for i in range(0, n):
            average_vel += self._cars_prop[i].scalar_velocity
            if(self._cars_prop[i].arrived_end):
                arrived_end = True
        average_vel /= float(n)

        if(average_vel < 0.0 and arrived_end):
            average_vel = 0.0

        # Move the car (not transform)
        for i in range(0, n):
            self._cars_prop[i].scalar_velocity = average_vel
            self.scalar_to_vector_position(i, average_vel * dt)


    def update_camera(self, camera, trackball):
        car = self._cars_prop[0]
        pos = QVector3D(car.position_vector[0], car.position_vector[1], car.position_vector[2])
        up  = QVector3D(car.basis[1][0], car.basis[1][1], car.basis[1][2])*0.35

        rot = QQuaternion()
        m4 = self._cars_obj[0]._transform
        m4.rotate(-90.0,0.0,1.0,0.0)
        m3 = QMatrix3x3()
        for i in range(3):
            for j in range(3):
                m3[i, j] = m4[j, i]
        rot = QQuaternion.fromRotationMatrix(m3)

        camera.setPosition(pos + up)
        trackball._rotation = rot
        camera.setRotation(QVector3D(0.0, math.pi, 0.0))
