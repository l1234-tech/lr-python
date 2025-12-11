import multiprocessing as mp
from integrate_1 import integrate

def worker(f, a_seg, b_seg, n_seg, result_queue, idx):
    result = integrate(f, a_seg, b_seg, n_iter=n_seg)
    result_queue.put((idx, result))

def integrate_processes_mp(f, a, b, *, n_jobs=2, n_iter=1000):
    """Аналог integrate_process с использованием multiprocessing напрямую (мультипроцессинг по своей реализации схож с noGIL,
    поэтому я выбрал егго , так как noGIL установить не получилось. """

    result_queue = mp.Queue()
    processes = []

    step = (b - a) / n_jobs
    seg_iter = n_iter // n_jobs

    for i in range(n_jobs):
        a_seg = a + i * step
        b_seg = a + (i + 1) * step

        p = mp.Process(
            target=worker,
            args=(f, a_seg, b_seg, seg_iter, result_queue, i)
        )
        processes.append(p)
        p.start()

    # Собираем результаты
    results = [0.0] * n_jobs
    for _ in range(n_jobs):
        idx, result = result_queue.get()
        results[idx] = result

    for p in processes:
        p.join()

    return sum(results)