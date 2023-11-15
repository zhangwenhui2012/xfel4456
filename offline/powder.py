import argparse

PREFIX      = '/gpfs/exfel/exp/SPB/202302/p004456/'
DATA_PATH   = 'entry_1/instrument_1/detector_1/data'

parser = argparse.ArgumentParser(description='Calculate the sum over events in a run. Requires processed data and vds file.')
parser.add_argument('run', type=int, help='Run number')
parser.add_argument('-a', '--ADU_per_photon',
                    help='ADUs per photon, for proc/ data the adus are in units of keV',
                    type=float)
parser.add_argument('-n', '--max_frames',
                    help='maximum number of frames to sum',
                    type=int)
                    #default='badpixel_mask_r0021.h5')
args = parser.parse_args()

args.vds_file         = PREFIX+'scratch/vds/r%.4d.cxi' %args.run
args.output_file      = PREFIX+'scratch/powder/powder_r%.4d.h5'%args.run


import numpy as np
import h5py
#import extra_data
from tqdm import tqdm
import sys
import time
import os

import multiprocessing as mp

if os.path.exists(args.output_file):
    print('Deleting existing powder file:', args.output_file)
    os.remove(args.output_file)

with h5py.File(args.vds_file) as f:
    cellID    = f['/entry_1/cellId'][:, 0]

Nevents = cellID.shape[0]

if args.max_frames :
    Nevents = args.max_frames

indices = np.arange(Nevents)

size = mp.cpu_count()

# split frames over ranks
events_rank = np.linspace(0, Nevents, size+1).astype(int)

frame_shape = (8,512,1024)

def worker(rank, lock):
    my_indices = indices[events_rank[rank]: events_rank[rank+1]] 
    
    print(f'rank {rank} is processing indices {events_rank[rank]} to {events_rank[rank+1]}')
    sys.stdout.flush()

    if rank == 0 :
        it = tqdm(range(len(my_indices)), desc = f'Processing data from {args.vds_file}')
    else :
        it = range(len(my_indices))

    frame = np.empty(frame_shape, dtype = float)
    
    powder = np.zeros(frame_shape, dtype = float)
    sum_index = 0
    done = False
    with h5py.File(args.vds_file) as g:
        data = g[DATA_PATH]
        
        for i in it:
            index = my_indices[i]
            frame[:] = np.squeeze(data[index]).astype(float)
            
            # photon conversion
            if args.ADU_per_photon :
                frame -= args.ADU_per_photon//2 + 1
                frame /= args.ADU_per_photon
            
            frame[frame<0] = 0
                
            powder += frame
            sum_index += 1
            
    # take turns writing frame_buf to file 
        
    # write to file sequentially
    if rank == 0: 
        print('Writing photons to     ', args.output_file)
        sys.stdout.flush()
    
    if lock.acquire() :
        with h5py.File(args.output_file, 'a') as f:
            if 'data' in f :
                powder += f['data'][()] 
                sum_index += f['Nframes'][()] 
                f['data'][...] = powder
                f['Nframes'][...] = sum_index
            else :
                f['data'] = powder
                f['Nframes'] = sum_index
        
        print(f'rank {rank} done')
        sys.stdout.flush()
        lock.release()


lock = mp.Lock()
jobs = [mp.Process(target=worker, args=(m, lock)) for m in range(size)]
[j.start() for j in jobs]
[j.join() for j in jobs]
print('Done')
sys.stdout.flush()



