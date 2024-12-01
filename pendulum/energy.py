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
        self.log_work()

    def log_work(self):
        kinetic_not_nan = [k for k in self.kinetic_energy if not np.isnan(k)]
        t_diff = kinetic_not_nan[-1] - kinetic_not_nan[0]
        print(f"Work: sum(deltaT) ?= Tf - Ti => {self.total_work} ?= {t_diff} => {self.total_work == t_diff}")
        mechanical_not_nan = [m for m in self.mechanical_energy if not np.isnan(m)]
        t_diff_ncf = mechanical_not_nan[-1] - mechanical_not_nan[0]
        print( f"Non-conservative forces work: sum(deltaT) ?= EMf - EMi => {self.total_non_conservative_forces_work} ?= {t_diff_ncf} => {self.total_non_conservative_forces_work == t_diff_ncf}")