# Ananysis code for p004456

Experiment directory:
```
/gpfs/exfel/exp/SPB/202302/p004456
```

Put personal analysis code in usr/Shared, e.g. for user "amorgan"
```
/gpfs/exfel/exp/SPB/202302/p004456/usr/Shared/amorgan
```

Put any analysis files (bigger than a few megabytes) in /scratch:
```
/gpfs/exfel/exp/SPB/202302/p004456/scratch
```


## analysis goals:
- [x] VDS: virtual h5 files that put all processed module data into a single cxi file.
    - ```offline/slurm/vds_array.sh``` (tested on run 5)
- [ ] Generate powder pattern
- [ ] Calculate number, location and intensity of streaks
- [ ] Generate streakogram from above
- [ ] Write cxi file from scan runs, for the purpose of speckle-tracking

