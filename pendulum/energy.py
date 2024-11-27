import numpy as np
import scipy.constants as const

from pendulum.solid_bar_pendulum import SolidBarPendulum


class Energy:
    def __init__(self, pendulum: SolidBarPendulum):
        self.pendulum = pendulum
        self.time = pendulum.pivot.t
        self.translation_kinetic_energy = 0.5 * self.pendulum.mass * self.pendulum.center_of_mass.velocity_smooth ** 2
        self.rotation_kinetic_energy = 0.5 * self.pendulum.moment_of_inertia * self.pendulum.angular_velocity ** 2
        self.kinetic_energy = self.translation_kinetic_energy + self.rotation_kinetic_energy
        self.potential_energy = self.pendulum.mass * const.g * self.pendulum.center_of_mass.y_position_smooth
        self.mechanical_energy = self.kinetic_energy + self.potential_energy
        self.work = np.diff(self.kinetic_energy)
        self.total_work = np.nansum(self.work)
        self.non_conservative_forces_work = np.diff(self.mechanical_energy)
        self.total_non_conservative_forces_work = np.nansum(self.non_conservative_forces_work)