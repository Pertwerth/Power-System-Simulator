### Generates fluctuating power supply pattern ###

import random
import math

'''default_model_variables = {
    'delta_power': 0.01,
    'power_increment': 0.1,
    'power_decrement': 0.1
}'''


class EnergySimulator:
    
    def __init__(self, **kwargs):
        self.model_variables = {}
        input_set = kwargs.keys()
        
        default_model_variables = {
            'delta_power': 0.01,
            'power_increment': 0.1,
            'power_decrement': 0.1,
            'sampling_rate': 60,
            'increment_time_interval': 1,
            'decrement_time_interval': 1
        }
        
        if 'delta_power' in input_set:
            self.model_variables['delta_power']=kwargs['delta_power']
        else:
            self.model_variables['delta_power']=default_model_variables['delta_power']
        if 'power_increment'in input_set:
            self.model_variables['power_increment']=kwargs['power_increment']
        else:
            self.model_variables['power_increment']=default_model_variables['power_increment']
        if 'power_decrement' in input_set:
            self.model_variables['power_decrement']=kwargs['power_decrement']
        else:
            self.model_variables['power_decrement']=default_model_variables['power_decrement']
        if 'sampling_rate' in input_set:
            self.model_variables['sampling_rate']=kwargs['sampling_rate']
        else:
            self.model_variables['sampling_rate']=default_model_variables['sampling_rate']
        if 'increment_time_interval' in input_set:
            self.model_variables['increment_time_interval']=kwargs['increment_time_interval']
        else:
            self.model_variables['increment_time_interval']=default_model_variables['increment_time_interval']
        if 'decrement_time_interval' in input_set:
            self.model_variables['decrement_time_interval']=kwargs['decrement_time_interval']
        else:
            self.model_variables['decrement_time_interval']=default_model_variables['decrement_time_interval']

    '''
    powers is an ordered list of tuples (supply, duration)
    Assumes that all supply powers are integers
    '''         
    
    def data_generation(self):
        samples = []
        i = 0
        try:
            for supply, duration in self.powers:
                total_samples_per_duration = int(duration*self.model_variables['sampling_rate'])
                for j in range(total_samples_per_duration):
                    power = supply+self.fluctuation_noise()
                    samples.append(power)
                samples = self.power_change_model(supply, self.powers[i+1][0], samples)
                i += 1
        except IndexError:
            return samples    

    def power_change_model(self, initial_power: int, new_power: int, sampling_list: list):
        power = initial_power
        while math.floor(power) != new_power:
            if power < new_power:
                power += self.model_variables['power_increment']
                for i in range(int(self.model_variables['increment_time_interval']*self.model_variables['sampling_rate'])):
                    recorded_power = power+self.fluctuation_noise()
                    sampling_list.append(recorded_power)
            elif power > new_power:
                power -= self.model_variables['power_decrement']
                for i in range(int(self.model_variables['decrement_time_interval']*self.model_variables['sampling_rate'])):
                    recorded_power = power+self.fluctuation_noise()
                    sampling_list.append(recorded_power)

        return sampling_list
    
    def get_powers(self, *args):
        self.powers = []
        if len(args) < 2:
            print('invalid input: need at least two arguments')
            return
        elif len(args)%2 != 0:
            print('Set is incomplete, either missing 1 supply power or 1 duration')     
        else:
            for i in range(0,len(args)-1,2):
                self.powers.append((args[i], args[i+1]))
                
    def fluctuation_noise(self):
        return random.uniform(-self.model_variables['delta_power'], self.model_variables['delta_power'])
    
    def execute_simulation(self):
        return self.data_generation()

def full_simulator_test(test_simulator: EnergySimulator):
    return test_simulator.execute_simulation()

def change_power_model_test(test_simulator: EnergySimulator, power0: int, power1: int):
    samples = []
    return test_simulator.power_change_model(power0, power1, samples)

if __name__ == '__main__':
    test_power_set = [1000,120,-800,60,500,120]
    test_model = {
            'delta_power': 10,
            'power_increment': 100,
            'power_decrement': 100,
            'sampling_rate': 0.1,
            'increment_time_interval': 1,
            'decrement_time_interval': 1
        }
    
    test_simulator = EnergySimulator(**test_model)
    
    test_simulator.get_powers(*test_power_set)
    
    test_result = full_simulator_test(test_simulator=test_simulator)
    
#    print(test_result)
    
    print(f'''
          TEST SUMMARY:
                Number of samples: {len(test_result)}
                Final Entry: {test_result[len(test_result)-1]}
          ''')
 