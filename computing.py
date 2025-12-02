#1)To zrobic kod dla x procesow z ustawiona stala iteracja i porownac ich czas
#2)zrobic kod bez iteracji - pp jak szybko to obliczy


from mpi4py import MPI
import random
import math
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def count_points_in_circle(num_points: int, seed: int | None = None) -> int:
    if seed is not None:
        random.seed(seed)
    inside = 0
    for _ in range(num_points):
        x = random.random() - 0.5
        y = random.random() - 0.5
        if x * x + y * y <= 0.25:
            inside += 1
    return inside

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        N_total = int(sys.argv[1])
    else:
        N_total = 50_000_000  
    base = N_total // size
    remainder = N_total % size
    local_N = base + (1 if rank < remainder else 0)
    comm.Barrier()
    if rank == 0:
        t0 = MPI.Wtime()

    local_inside = count_points_in_circle(local_N, seed=rank + 12345)
    total_inside = comm.reduce(local_inside, op=MPI.SUM, root=0)
    total_points = comm.reduce(local_N, op=MPI.SUM, root=0)

    if rank == 0:
        t1 = MPI.Wtime()
        pi_est = 4.0 * total_inside / total_points
        err = pi_est - math.pi
        print(f"Procesy:       {size}")
        print(f"Liczba punktów {total_points}")
        print(f"pi (estymata): {pi_est}")
        print(f"błąd:          {err}")
        print(f"czas [s]:      {t1 - t0:.6f}")


'''
from mpi4py import MPI
import random
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def count_points_in_circle(num_points: int) -> int:
    inside = 0
    for _ in range(num_points):
        x = random.random() - 0.5
        y = random.random() - 0.5
        if x * x + y * y <= 0.25:
            inside += 1
    return inside


if __name__ == "__main__":
    batch_per_rank = 100_000

    global_inside = 0
    global_points = 0

    comm.Barrier()
    if rank == 0:
        t0 = MPI.Wtime()

    while True:
        local_inside = count_points_in_circle(batch_per_rank)
        local_points = batch_per_rank

        batch_inside = comm.reduce(local_inside, op=MPI.SUM, root=0)
        batch_points = comm.reduce(local_points, op=MPI.SUM, root=0)

        if rank == 0:
            global_inside += batch_inside
            global_points += batch_points

            pi_est = 4.0 * global_inside / global_points
            err = abs(pi_est - math.pi)

            converged = (err < 0.00005)
            print(f"N = {global_points:>10d}, pi = {pi_est:.8f}, err = {err:.8e}, "f"converged = {converged}")
        else:
            converged = None

        converged = comm.bcast(converged, root=0)

        if converged:
            break

    comm.Barrier()
    if rank == 0:
        t1 = MPI.Wtime()
        pi_est = 4.0 * global_inside / global_points
        print("\nFINAL")
        print(f"Procesy:        {size}")
        print(f"Liczba punktów: {global_points}")
        print(f"pi (estymata):  {pi_est}")
        print(f"pi (dokładne):  {math.pi}")
        print(f"błąd:           {pi_est - math.pi}")
        print(f"czas [s]:       {t1 - t0:.6f}")


#2 400 000

'''


