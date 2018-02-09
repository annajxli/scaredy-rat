# scaredy-rat
ethovision fear conditioning behavior analysis

this is a collection of jupyter notebooks that analyze raw data output from EthoVision.

scaredy-rat: main notebook; finds mean, median, and maximal velocities for timebins across the FC paradigm, generates a plot of velocity over time.

rat-pack: concatenates mean and median outputs from scaredy-rat into a more readable format.

rat-pack-max: concatenates max outputs from scaredy-rat.

----

the timebins are as follows (and modifiable):

pretone (30 s before tone)

tone (during tone, 30s default)

shock (5s after tone)

post-shock (30s after shock time bin)

----

originally created for the Shansky Lab, Northeastern University.
