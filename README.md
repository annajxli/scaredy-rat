# scaredy-rat
ethovision fear conditioning behavior analysis

this is a collection of jupyter notebooks that analyze raw data output from EthoVision.

scaredy-rat: main notebook; finds mean, median, and maximal velocities for timebins across the FC paradigm, generates a plot of velocity over time.

rat-pack: concatenates mean and median outputs from s-r into a more readable format.

rat-pack-max: concatenates max outputs from s-r.

----

the timebins are as follows (and modifiable):

pretone (30 s before tone)

tone (during tone, 30s default)

shock (5s after tone)

post-shock (30s after shock time bin)

----

there are a few issues i'm working on, mainly for the purposes of using a different paradigm (e.g. different number of tones, etc). that said, it should be modifiable to most ethovision raw data. i have a few notes for what to change when running on a different dataset, but it likely has gaps. please feel free to reach out - annajxli@gmail.com.

originally created for the Shansky Lab, Northeastern University.
