This 3 Body Simulation works by calculating the gravitational forces between all the bodies in the system using Newton's Law of Gravitation, and the initial positions.
These forces are summed for each body and used to update its velocity. The velocities are used to calculate the change in distance, and this can be used to calculate the change in positions.
A PyGame window is used to show the bodies and the coordinate system is changed into PyGame's system (y values increase downwards, etc.)

To get started, first run the simulation with the figure-8 conditions (one of the few known initial conditions which lead to stable orbits). Change the values (position and velocity are in (x, y)) ane experiment with them.
The given time step value 0.005 seconds is perfect because we need small values for accuracy (or the system turns into chaos), but making the values too small will cause performance issues.
G, the gravitational constant is set to 1 for the figure-8 conditions which is useful for simple simulations to understand the behavior of gravity, because otherwise large masses are required to see any effects.
You can add more bodies or remove a body (to have 2), and you can change the scale based on your values. You can set trail=false for each of the bodies if you don't want to see a trail, or if you want a trail, you can also change the length (in number of previous values).

Have fun!
