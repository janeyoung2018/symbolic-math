import argparse
import time

import os
import ray
from ray.exceptions import RayTimeoutError

from backward import generate_bwd


@ray.remote
def ray_generate_bwd(n=1):
    out = generate_bwd(n)
    for res in out:
        append_sample(res)
    return out


def append_sample(sample):
    fldr = './data/dataset'
    path = os.path.join(fldr, '{}.txt'.format(time.time()))
    if os.path.exists(fldr):
        arg = 'a'
    else:
        os.makedirs(fldr, exist_ok=True)
        arg = 'w'

    with open(path, arg) as fi:
        fi.write(sample)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu', default=8, nargs='?')
    parser.add_argument('--num', default=64, nargs='?')
    parser.add_argument('--n', default=1, nargs='?')
    args = parser.parse_args()

    sequences_per_process = int(args.n)
    cpu = int(args.cpu)
    num = int(args.num)
    process_runs = int(num / cpu)

    ray.shutdown()
    ray.init(num_cpus=cpu)
    t0 = time.time()

    print('{} samples {} cpu {} process_runs {} seq per process'.format(num, cpu, process_runs, sequences_per_process))

    fails = 0
    dataset = []
    for _ in range(process_runs*cpu):
        try:
            out = ray_generate_bwd.remote(sequences_per_process)
            out = ray.get(out, timeout=sequences_per_process)
            dataset.extend(out)
        except (TypeError, RayTimeoutError) as e:
            print('fail', e)
            fails += 1

    print(time.time() - t0)
    print(len(dataset))
