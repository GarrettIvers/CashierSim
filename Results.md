# Grocery Store Simulation
**By:**
- Peyton Slater
- Meme Chhay
- Garrett Iverson

**Simulation 001**

**Instructor:** Dr. Doug Williams

**Date:** April 11, 2024


## Description
This simulation models the behavior of a grocery store with both cashier and self-checkout options. The purpose is to analyze customer flow, checkout queue lengths, and wait times under various store configurations and customer behaviors.

## Variables
- `simulation_time`: Duration of the simulation (in minutes)
- `num_cashiers`: Number of cashier checkouts available
- `num_self_checkouts`: Number of self-checkout stations available
- `arrival_rate`: Average number of customers arriving per hour
- `shopping_time_mean`: Mean shopping time for customers (in minutes)
- `shopping_time_std`: Standard deviation of shopping time (in minutes)
- `cashier_service_time_mean`: Mean service time at cashier checkouts (in minutes)
- `cashier_service_time_std`: Standard deviation of service time at cashier checkouts (in minutes)
- `self_checkout_service_time_mean`: Mean service time at self-checkout stations (in minutes)
- `self_checkout_service_time_std`: Standard deviation of service time at self-checkout stations (in minutes)
- `seed`: Random seed for reproducibility

## Distributions
- Customer arrivals follow a Poisson distribution with an average arrival rate of `arrival_rate` customers per hour.
- Shopping times are normally distributed with a mean of `shopping_time_mean` and a standard deviation of `shopping_time_std`.
- Service times at cashier checkouts are normally distributed with a mean of `cashier_service_time_mean` and a standard deviation of `cashier_service_time_std`.
- Service times at self-checkout stations are normally distributed with a mean of `self_checkout_service_time_mean` and a standard deviation of `self_checkout_service_time_std`.

## Simulation Results
![Average Shopping Time and Service Time](average_shopping_service_time.png)
*Figure 1: Average Shopping Time and Service Time*

The graph above shows the average shopping time and service time over the course of the simulation. The rolling mean with a window of 10 is used to smooth out fluctuations and show the overall trend.

![Checkout Queue Length](checkout_queue_length.png)
*Figure 2: Checkout Queue Length*

This graph displays the length of the cashier queue and self-checkout queue at the end of the simulation. It provides insights into which queue experiences more congestion.

![Average Checkout Queue Wait Time](average_checkout_wait_time.png)
*Figure 3: Average Checkout Queue Wait Time*

The graph above shows the average wait time for customers in the cashier queue and self-checkout queue. It helps identify which queue has longer wait times.

## Analysis
Based on the simulation results, we can observe the following:
- The average shopping time remains relatively stable throughout the simulation, while the average service time shows some variability.
- In this particular simulation run, the cashier queue has a longer queue length compared to the self-checkout queue.
- The average wait time is higher for the cashier queue compared to the self-checkout queue.

These insights can help store managers make informed decisions about resource allocation, staffing, and checkout configurations to optimize customer experience and reduce wait times.

## Conclusion
The grocery store simulation provides a valuable tool for understanding customer behavior, queue dynamics, and service performance in a retail setting. By adjusting the simulation parameters, such as the number of cashiers and self-checkout stations, arrival rate, and service time distributions, various scenarios can be explored to identify optimal store configurations and improve overall efficiency.