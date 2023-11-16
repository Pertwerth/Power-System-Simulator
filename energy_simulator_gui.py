import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from energy_simulator import EnergySimulator


class EnergySimulatorGui:
    
    def __init__(self):
        self.window = tk.Tk(screenName= 'Energy Simulator GUI')
        self.make_layout()
    
    def set_up_simulator(self):
        model_params = {}
        model_params['delta_power'] = float(self.delta_power_input.get())
        model_params['power_increment'] = float(self.power_increment_input.get())
        model_params['power_decrement'] = float(self.power_decrement_input.get())
        model_params['sampling_rate'] = float(self.sampling_rate_input.get())
        model_params['increment_time_interval'] = float(self.increment_time_interval_input.get())
        model_params['decrement_time_interval'] = float(self.decrement_time_interval_input.get())
        self.simulator = EnergySimulator(**model_params)
        print(f'current params: {self.simulator.model_variables}')
        
    def start_simulation(self):
        powers = [int(i) for i in self.power_input_space.get(1.0, 'end-1c').split(', ')]
        self.simulator.get_powers(*powers)
        data = self.simulator.execute_simulation()
        print(f'''
              SIMULATION SUMMARY:
                    Sample size: {len(data)}
                    Final Entry: {data[len(data)-1]}
              ''')
        self.make_graph(data)
        return data
    
    def make_graph(self, data: list):
        t = [i for i in range(0,len(data))]
        y = data
        
        fig = Figure(figsize= (10, 5), dpi= 100)
        plot = fig.add_subplot(111)
        plot.step(t, y)
        self.output_graph= FigureCanvasTkAgg(figure= fig, master= self.window)
        self.output_graph.draw()
        
        self.output_graph.get_tk_widget().grid(row=8, column=0, columnspan=3, sticky='nsew')
        
        
        

    def make_layout(self):
        self.window.columnconfigure(index= 0, weight = 2)
        self.window.columnconfigure(index= (1,2), weight= 1)
        self.window.rowconfigure(index= (0,1,2,3,4,5,6,7), weight= 1)
        self.window.rowconfigure(index= 8, weight= 7)
        self.power_input_space= tk.Text(master= self.window)
        self.delta_power_label = tk.Label(self.window, text='power fluctuation range')
        self.power_increment_label = tk.Label(self.window, text='power increment')
        self.power_decrement_label = tk.Label(self.window, text='power decrement')
        self.sampling_rate_label = tk.Label(self.window, text='samples per second')
        self.increment_time_interval_label = tk.Label(self.window, text='power increment time interval')
        self.decrement_time_interval_label = tk.Label(self.window, text='power decrement time interval')
        self.delta_power_input = tk.Entry(self.window)
        self.power_increment_input = tk.Entry(self.window)
        self.power_decrement_input = tk.Entry(self.window)
        self.sampling_rate_input = tk.Entry(self.window)
        self.increment_time_interval_input = tk.Entry(self.window)
        self.decrement_time_interval_input = tk.Entry(self.window)
        self.set_model_parameters_button = tk.Button(self.window, text='set model parameters', command=self.set_up_simulator, bg= '#f0f0f0')
        self.set_power_button = tk.Button(self.window, text='start simulation', command= self.start_simulation)
        self.power_input_space.grid(row= 0, rowspan=6, column = 0, sticky='nsew')
        self.delta_power_label.grid(row=0, rowspan=1, column=1, sticky='e')
        self.delta_power_input.grid(row=0, column=2)
        self.power_increment_label.grid(row=1, column=1, sticky='e')
        self.power_increment_input.grid(row=1, column=2)
        self.power_decrement_label.grid(row=2, column=1, sticky='e')
        self.power_decrement_input.grid(row=2, column=2)
        self.sampling_rate_label.grid(row=3, column=1, sticky='e')
        self.sampling_rate_input.grid(row=3, column=2)
        self.increment_time_interval_label.grid(row=4, column=1, sticky='e')
        self.increment_time_interval_input.grid(row=4, column=2)
        self.decrement_time_interval_label.grid(row=5, column=1, stick='e')
        self.decrement_time_interval_input.grid(row=5, column=2)
        self.set_model_parameters_button.grid(row=6, column=1, columnspan=2)
        self.set_power_button.grid(row=6, column=0)
        
    def start_app(self):
        self.window.mainloop()
        
if __name__ == '__main__':
    test_gui = EnergySimulatorGui()
    test_gui.start_app()
        