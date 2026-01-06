import numpy as np 
import math 
import matplotlib.pyplot as plt
from scipy.stats import norm

class Engine:
    def __init__(self, s_o, mu, sigma, time=1, simulations=50000):
        self.s_o = s_o
        self.mu = mu
        self.sigma = sigma
        self.time = time
        self.total_steps = time*252
        self.simulations = simulations
        self.time_step = 1 / 252
    
    def apple_path(self):
        rng = np.random.default_rng()

        matrix = rng.normal(0, 1, size=(self.simulations, self.total_steps + 1))
        matrix[:, 0] = 0
        delta = self.mu - ( self.sigma**2 / 2 )
        matrix *= self.sigma * np.sqrt(self.time_step)
        matrix += delta * self.time_step
        matrix = np.cumsum(matrix, axis=1)
        matrix = math.e**matrix
        matrix[:, 0] = 1
        matrix *= self.s_o

        return matrix
    
    def S_t(self):
        rng = np.random.default_rng()

        s_t = rng.normal(0, self.time, self.simulations)
        s_t *= self.sigma
        delta = self.mu - ( self.sigma**2 / 2 )
        s_t += delta 
        s_t = math.e**s_t * self.s_o

        return s_t
    
    def black_sholes(self, k, r):
        d1 = (np.log(self.s_o / k) + (r + self.sigma**2 / 2)*self.time) / (self.sigma * np.sqrt(self.time))
        d2 = d1 - self.sigma*np.sqrt(self.time)

        n_d1 = norm.cdf(d1)
        n_d2 = norm.cdf(d2)

        return self.s_o*n_d1 - k*(np.exp(-r*self.time))*n_d2

    def antithetic_s_t(self):
        rng = np.random.default_rng()

        s_t = rng.normal(0, self.time, self.simulations)
        s_t *= self.sigma
        _s_t = -s_t
        delta = self.mu - ( self.sigma**2 / 2 )
        s_t += delta 
        _s_t += delta
        s_t = math.e**s_t * self.s_o
        _s_t = math.e**(_s_t) * self.s_o

        return s_t, _s_t

class Tasks:
    def __init__(self):
        pass

    def task1(self):
        path_simulations = Engine(100, 0.05, 0.20)
        matrix = path_simulations.apple_path()
        time = np.arange(0, 253)

        plt.figure()

        for i in range(100):
            plt.plot(time, matrix[i, :], alpha=0.7)

        mean_path = np.mean(matrix, axis=0)
        plt.plot(time, mean_path, color='orange', linewidth=4)

        exp_path = np.full(253, 0.05)* (1/252)
        exp_path[0] = 0
        exp_path = np.cumsum(exp_path)
        exp_path = math.e**exp_path * 100
        plt.plot(time, exp_path, color='blue', linewidth=4)


        plt.xlabel("Time")
        plt.ylabel("Stock Price")
        plt.title("Apple Stock Path")
        plt.show()

    def task2(self):
        K = 100
        r = 0.05

        error_list = []
        number_of_samples = []
        simulations = 1024

        while simulations < 10e7:
            path_simulations = Engine(100, 0.05, 0.20, 1, simulations)
            payoffs = path_simulations.S_t() - K
            payoffs[payoffs < 0] = 0
            exp_payoff = np.mean(payoffs)
            monte_price = np.exp(-r)*exp_payoff
            b_sholes = path_simulations.black_sholes(K, r)

            error_list.append(monte_price - b_sholes)
            number_of_samples.append(simulations)
            simulations *= 2

        plt.figure()
        plt.plot(number_of_samples, error_list)
        plt.xlabel("Number of Simulations")
        plt.ylabel("Error (monte - sholes)")
        plt.title("B Sholes and Monte Analysis")
        plt.show()

    def task3(self):
        K = 100
        r = 0.05

        discounted_payoff = []
        number_of_samples = []
        simulations = 1024

        while simulations < 10e5:
            path_simulations = Engine(100, 0.05, 0.20, 1, simulations)
            matrix = path_simulations.apple_path()
            matrix = np.mean(matrix, axis=1)
            payoff = np.maximum(matrix - K, 0)
            discount = math.e**(-r) * np.mean(payoff)

            number_of_samples.append(simulations)
            discounted_payoff.append(discount)

            simulations *= 2
        
        plt.figure()
        plt.plot(number_of_samples, discounted_payoff)
        plt.xlabel("Number of Samples")
        plt.ylabel("Discounted Expected Payoff")
        plt.title("Asian Options")
        plt.show()

    def task4(self):
        K = 100
        r = 0.05

        simulations = 1024
        error = []
        num_sim = []

        while simulations < 10e5:
            path_simulations = Engine(100, 0.05, 0.2, 1, simulations)
            matrix = path_simulations.apple_path()
            value_matrix = np.zeros((simulations, 253))
            immediate_cash = np.maximum(K - matrix, 0)
            
            i = 251
            value_matrix[:, -1] += np.maximum(K - matrix[:, -1], 0)
            while i >= 0:
                value_matrix[:, i] = value_matrix[:, i+1] * math.e**(-r/252)

                mask1 = K - matrix[:, i] > 0
                x = matrix[mask1, i]
                y = value_matrix[mask1, i+1] * np.exp(-r/252)

                if np.sum(x)>0:
                    coef = np.polyfit(x, y, 2)

                    z = x**2 * coef[0] + x * coef[1] + coef[2]
                    idx = np.where(mask1)[0]
                    mask2 = immediate_cash[mask1, i] > z
                    idx_change = idx[mask2]
                    value_matrix[idx_change, i] = immediate_cash[idx_change, i]

                i -= 1

            american_ = np.mean(value_matrix[:, 0])
            european_ = np.mean(np.maximum(K - matrix[:, -1], 0) * math.e**(-r))

            error.append(american_ - european_)
            num_sim.append(simulations)
            simulations *= 2

        plt.figure()
        plt.plot(num_sim, error)
        plt.xlabel("Number of Sample")
        plt.ylabel("American - European")
        plt.title("American Put Option Analysis with European")
        plt.show()

    def task5(self):
        K = 100
        r = 0.05

        error_list = []
        number_of_samples = []
        simulations = 512

        while simulations < 10e7:
            path_simulations = Engine(100, 0.05, 0.20, 1, simulations)
            payoff1, payoff2 = path_simulations.antithetic_s_t()
            payoff2 -= K
            payoff1 -= K
            payoff1[payoff1 < 0] = 0
            payoff2[payoff2 < 0] = 0
            exp_payoff = ( np.mean(payoff1) + np.mean(payoff2) ) / 2
            monte_price = np.exp(-r)*exp_payoff
            b_sholes = path_simulations.black_sholes(K, r)

            error_list.append(monte_price - b_sholes)
            number_of_samples.append(simulations)
            simulations *= 2

        plt.figure()
        plt.plot(number_of_samples, error_list)
        plt.xlabel("Number of Simulations")
        plt.ylabel("Error (monte - sholes)")
        plt.title("B Sholes and Monte Analysis")
        plt.show()


try:
    a = int(input("Enter the Task you want to perform (eg. 1,2,..) : "))
    t = Tasks()
    if a == 1:
        t.task1()
    elif a == 2:
        t.task2()
    elif a == 3:
        t.task3()
    elif a == 4:
        t.task4()
    elif a == 5:
        t.task5()
    else:
        print("Chutiye, 5 hi task the")
    
except:
    print("Input Task Number Only")