import numpy as np
import matplotlib.pyplot as plt
import math

class MonteCarlo_PI:
    def __init__(self, n):
        # print("Input the number sample points you want : ")
        self.n = n

    def pi(self):
        x = np.random.rand(self.n, 1)*2 - 1
        y = np.random.rand(self.n, 1)*2 - 1
        x = x*x
        y = y*y
        count = np.sum(x + y < 1)
        return 4 * count / self.n     

class MonteCarlo_e:
    def __init__(self, n):
        self.n = n
        self.inf = 10
    
    # def __init__(self):
    #     self.n = input(int("Input the number sample points you want : "))
    #     self.inf = 1000
    
    def e(self):
        sample_i = np.random.default_rng().uniform(0, 1, size=(self.inf, self.n))
        matrix = sample_i[:-1, :]
        new_row = np.ones((1, self.n))
        matrix = np.vstack((new_row, matrix))
        subtract = matrix - sample_i
        subtract= np.where(subtract < 0, 1, 0)
        args = np.argmax(subtract, axis=0)
        
        return np.mean(args) + 1


a = 2
b = 2
xvalues = []
value_of_pi = []
error = []
while a < 10e7:
    find_pi = MonteCarlo_PI(a)
    t_pi = find_pi.pi()
    value_of_pi.append(t_pi)
    xvalues.append(a)
    error.append(abs(math.pi - t_pi) / math.pi * 100)
    a *= 2

fig, axes = plt.subplots(2,1)

axes[0].plot(xvalues, value_of_pi, color='red')
axes[0].set_xlabel("Number of Samples")
axes[0].set_ylabel("Value of Pi")
axes[0].set_title("Pi determination")

axes[1].plot(xvalues, error, color='red')
axes[1].set_xlabel("Number of Samples")
axes[1].set_ylabel("Relative error")
axes[1].set_title("Relative error analysis")

plt.show()

e = MonteCarlo_e(1000000)
print(e.e())

# subtract = np.array([[2, 4, -1], 
#                      [3, -1, -1], 
#                      [-1, -1, -1],
#                      [4, 5, 6]])
# subtract = np.where(subtract < 0, 1, 0)
# args = np.argmax(subtract, axis=0)
# print(args)