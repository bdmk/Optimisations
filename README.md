# Optimisations

Project will contain methods for selecting optimal parameter sets for functions with min/max goal.

## Particle Swarm Optimisation
Method uses particles (agents) to search through parameter space and by interactions decide on the best position.
See wikipedia: https://en.wikipedia.org/wiki/Particle_swarm_optimization.

One can set initial position for each particle. Those without specified location will use Halton sequence to generate pseudo-random position.
Implemented perturbation system forces particles to search around any local minimum.