import simpy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

class GroceryStore:
    def __init__(self, env, num_cashiers, num_self_checkouts, arrival_rate, shopping_time_mean, shopping_time_std, cashier_service_time_mean, cashier_service_time_std, self_checkout_service_time_mean, self_checkout_service_time_std, seed):
        self.env = env
        self.cashier_queue = simpy.Resource(env, num_cashiers)
        self.self_checkout_queue = simpy.Resource(env, num_self_checkouts)
        self.arrival_rate = arrival_rate
        self.shopping_time_mean = shopping_time_mean
        self.shopping_time_std = shopping_time_std
        self.cashier_service_time_mean = cashier_service_time_mean
        self.cashier_service_time_std = cashier_service_time_std
        self.self_checkout_service_time_mean = self_checkout_service_time_mean
        self.self_checkout_service_time_std = self_checkout_service_time_std
        self.seed = seed
        self.data = []

        # Set the seed for reproducibility
        random.seed(self.seed)
        np.random.seed(self.seed)

    def customer_arrival(self):
        while True:
            # Generate customer arrivals using a Poisson distribution
            interarrival_time = random.expovariate(self.arrival_rate)
            yield self.env.timeout(interarrival_time)
            self.env.process(self.customer_flow())

    def customer_flow(self):
        # Simulate shopping time using a normal distribution
        shopping_time = random.normalvariate(self.shopping_time_mean, self.shopping_time_std)
        yield self.env.timeout(max(0, shopping_time))

        # Decide whether the customer chooses cashier or self-checkout
        if random.random() < 0.6:  # 60% of customers choose cashier queue
            checkout_start = self.env.now
            with self.cashier_queue.request() as request:
                yield request
                checkout_queue_time = self.env.now - checkout_start
                service_time = random.normalvariate(self.cashier_service_time_mean, self.cashier_service_time_std)
                service_time = max(0, service_time)  # Ensure service time is non-negative
                yield self.env.timeout(service_time)
                self.data.append([self.env.now, shopping_time, checkout_queue_time, service_time, 'Cashier'])
        else:
            checkout_start = self.env.now
            with self.self_checkout_queue.request() as request:
                yield request
                checkout_queue_time = self.env.now - checkout_start
                service_time = random.normalvariate(self.self_checkout_service_time_mean, self.self_checkout_service_time_std)
                service_time = max(0, service_time)  # Ensure service time is non-negative
                yield self.env.timeout(service_time)
                self.data.append([self.env.now, shopping_time, checkout_queue_time, service_time, 'Self-Checkout'])

def run_simulation(simulation_time, num_cashiers, num_self_checkouts, arrival_rate, shopping_time_mean, shopping_time_std, cashier_service_time_mean, cashier_service_time_std, self_checkout_service_time_mean, self_checkout_service_time_std, seed):
    env = simpy.Environment()
    grocery_store = GroceryStore(env, num_cashiers, num_self_checkouts, arrival_rate, shopping_time_mean, shopping_time_std, cashier_service_time_mean, cashier_service_time_std, self_checkout_service_time_mean, self_checkout_service_time_std, seed)
    env.process(grocery_store.customer_arrival())
    env.run(until=simulation_time)

    # Convert collected data to a DataFrame
    df = pd.DataFrame(grocery_store.data, columns=['Timestamp', 'ShoppingTime', 'CheckoutQueueTime', 'ServiceTime', 'CheckoutType'])
    return df

# Example usage
simulation_time = 8 * 60  # Simulate 8 hours (in minutes)
num_cashiers = 1
num_self_checkouts = 2
arrival_rate = 1/5  # Average 5 customers per hour
shopping_time_mean = 20
shopping_time_std = 5
cashier_service_time_mean = 5
cashier_service_time_std = 2
self_checkout_service_time_mean = 8
self_checkout_service_time_std = 3
seed = 42  # Set a seed value for reproducibility

simulation_data = run_simulation(simulation_time, num_cashiers, num_self_checkouts, arrival_rate, shopping_time_mean, shopping_time_std, cashier_service_time_mean, cashier_service_time_std, self_checkout_service_time_mean, self_checkout_service_time_std, seed)

# Round the simulation data to 2 decimal places
simulation_data = simulation_data.round(2)

# Save simulation results as a table PNG
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')
table = ax.table(cellText=simulation_data.values, colLabels=simulation_data.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)
plt.tight_layout()
plt.savefig('simulation_results_table.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Graph 1: Average Wait Time
fig1, ax1 = plt.subplots(figsize=(10, 6))
cashier_wait_time = simulation_data[simulation_data['CheckoutType'] == 'Cashier']['CheckoutQueueTime'].mean()
self_checkout_wait_time = simulation_data[simulation_data['CheckoutType'] == 'Self-Checkout']['CheckoutQueueTime'].mean()
ax1.bar(['Cashier', 'Self-Checkout'], [cashier_wait_time, self_checkout_wait_time])
ax1.set_xlabel('Checkout Type')
ax1.set_ylabel('Average Wait Time (minutes)')
ax1.set_title('Average Wait Time by Checkout Type')
plt.tight_layout()
plt.savefig('average_wait_time_comparison.png', dpi=300)
plt.close(fig1)

# Graph 2: Queue Length
fig2, ax2 = plt.subplots(figsize=(10, 6))
cashier_queue_length = simulation_data[simulation_data['CheckoutType'] == 'Cashier'].shape[0]
self_checkout_queue_length = simulation_data[simulation_data['CheckoutType'] == 'Self-Checkout'].shape[0]
ax2.plot(simulation_data['Timestamp'], simulation_data['CheckoutType'].map({'Cashier': 1, 'Self-Checkout': 0}).cumsum(), label='Queue Length')
ax2.set_xlabel('Simulation Time (minutes)')
ax2.set_ylabel('Queue Length')
ax2.set_title('Queue Length Over Time')
ax2.legend()
plt.tight_layout()
plt.savefig('queue_length_over_time.png', dpi=300)
plt.close(fig2)

# Graph 3: Checkout Efficiency
fig3, ax3 = plt.subplots(figsize=(10, 6))
cashier_efficiency = cashier_queue_length / (simulation_time / 60)
self_checkout_efficiency = self_checkout_queue_length / (simulation_time / 60)
ax3.bar(['Cashier', 'Self-Checkout'], [cashier_efficiency, self_checkout_efficiency])
ax3.set_xlabel('Checkout Type')
ax3.set_ylabel('Customers Processed per Hour')
ax3.set_title('Checkout Efficiency')
plt.tight_layout()
plt.savefig('checkout_efficiency.png', dpi=300)
plt.close(fig3)

# Graph 4: Customer Experience
fig4, ax4 = plt.subplots(figsize=(8, 6))
checkout_preference = simulation_data['CheckoutType'].value_counts(normalize=True)
ax4.pie(checkout_preference, labels=checkout_preference.index, autopct='%1.1f%%')
ax4.set_title('Customer Checkout Preference')
plt.tight_layout()
plt.savefig('customer_checkout_preference.png', dpi=300)
plt.close(fig4)

# Graph 5: Resource Utilization
fig5, ax5 = plt.subplots(figsize=(10, 6))
cashier_utilization = simulation_data[simulation_data['CheckoutType'] == 'Cashier']['ServiceTime'].sum() / (num_cashiers * simulation_time)
self_checkout_utilization = simulation_data[simulation_data['CheckoutType'] == 'Self-Checkout']['ServiceTime'].sum() / (num_self_checkouts * simulation_time)
ax5.bar(['Cashier', 'Self-Checkout'], [cashier_utilization, self_checkout_utilization])
ax5.set_xlabel('Checkout Type')
ax5.set_ylabel('Utilization')
ax5.set_title('Resource Utilization')
plt.tight_layout()
plt.savefig('resource_utilization.png', dpi=300)
plt.close(fig5)

# Graph 6: Sensitivity Analysis
fig6, ax6 = plt.subplots(figsize=(10, 6))
arrival_rates = [1/10, 1/8, 1/6, 1/4]
avg_wait_times = []
for rate in arrival_rates:
    simulation_data_sensitivity = run_simulation(simulation_time, num_cashiers, num_self_checkouts, rate, shopping_time_mean, shopping_time_std, cashier_service_time_mean, cashier_service_time_std, self_checkout_service_time_mean, self_checkout_service_time_std, seed)
    avg_wait_time = simulation_data_sensitivity['CheckoutQueueTime'].mean()
    avg_wait_times.append(avg_wait_time)
ax6.plot(arrival_rates, avg_wait_times, marker='o')
ax6.set_xlabel('Customer Arrival Rate (customers per minute)')
ax6.set_ylabel('Average Wait Time (minutes)')
ax6.set_title('Sensitivity Analysis - Arrival Rate vs. Wait Time')
plt.tight_layout()
plt.savefig('sensitivity_analysis.png', dpi=300)
plt.close(fig6)