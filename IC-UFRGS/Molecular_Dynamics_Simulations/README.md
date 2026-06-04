# Molecular_Dynamics_Simulations
 Simulations in C language of Molecular Dynamics based on "Understanding Molecular Simulation From Algorithms to Applications" by Frenkel and Smit.

## MolecularSimulation.c

This is a molecular dynamics simulations based on Lennard-Jones potential. The paramaters for this simulation are number of particles (N), density (rho), initial temperature (t0), time-step (dt), end time (tmax) and equilibrium time (teq). The program use a Verlet Algorithm for the integration. It also computes the radial distribution and mean squared displacement (MSD). The output are 4 files:

 - energias.txt: contains the time (T), potential energy (U), kinetic energy (K) and total energy (E) per particle;
 - g_r.txt: contains the radius of the sphere analysed (r) and the radial distribution (g(r));
 - msd.txt: contains the time (T) and the mean squared displacemente (dr);
 - posi.txt: are a group of files each one containing the position of each particle in i 100 steps in simulation. This files are used in the program Jmol (http://jmol.sourceforge.net/) to visualize the particles evolution;
 
**Verify before running the program that in the same branch you have a folder called "podicoes". In this folder will be saved all the posi.txt files.**


## Graficos.py
This program plots a graph of the energy of the sistem, the MSD and the radial distribution. You will also find a plot of the local density commented at the end. According to Frenkel's book, the energy graph must have the following behaviour: 

- the total energy must remain constant; 
- the kinetic and potential energy may vary initially, but they must oscillate around their equilibrium value near the end;

Any other behaviour means there is an error in the simulation.

## Simulacao.c (this is an old project. Check "MolecularSimulation" for the working one.)
It is a molecular dynamic simulation using Verlet Integration. The parameters - number of particles (N), density (rho), initial temperature (t0), time-step (dt) and end time (tmax) - are declared inside the code, there is no need to use the file "parameters.txt". This program creates a file named "saida.txt" with the potential energy (U), the kinetic energy (K) and total energy (E) computed for each step.
