import numpy as np 
import matplotlib.pyplot as plt

outcomes = [-1,1]
game_matrix = np.random.choice(outcomes, size=(1000, 10000))
path = 100 + np.cumsum(game_matrix, axis=0)

zero_mask = path == 0
first_zero = np.full(10000, 1000)
col_with_zero = zero_mask.any(axis=0)
first_zero[col_with_zero] = np.argmax(zero_mask[:, col_with_zero], axis=0)
row = np.arange(1000).reshape(-1, 1)
mask_below_idx = row > first_zero
path[mask_below_idx] = 0

time = np.arange(1001)

extra_row = np.ones((1,10000))*100
new_path = np.vstack((extra_row, path))


fig, axes = plt.subplots(2,1)

for i in range(100):
    axes[0].plot(time, new_path[:, i], alpha=0.4)

mean_path = np.sum(new_path, axis=1) / 10000
axes[0].plot(time, mean_path, color='red', linewidth=3)

sum = np.sum(game_matrix, axis=0)
max = np.argmax(sum)
min = np.argmin(sum)
axes[0].plot(time, new_path[:, max], color='black')
axes[0].plot(time, new_path[:, min], color='blue')

axes[0].set_xlabel("Time")
axes[0].set_ylabel("BankRoll")
axes[0].set_title("random walk")


final_wealth = new_path[-1, :]
axes[1].hist(final_wealth, bins=200)
axes[1].set_xlabel("final_wealth")
axes[1].set_ylabel("number of people")
axes[1].set_title("final wealth hist")

plt.show()