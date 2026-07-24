import random
import statistics
from functions.comb_manager import CombinationManager
from gamspy_model.meshr_class_without_cat_res import ReactiveDistillationModel
import numpy as np
import time
from datetime import datetime



try:
    del manager
except:
    a=1

meshr = ReactiveDistillationModel(max_stages=22)

# loading the dataframe for simulation
# gdx_file = "data/full_exhaustive_3R_split_1.gdx"
# gdx = gamspy.Container(gdx_file)
# df = process_gdx_data(gdx)
# df = data.drop('NFE',axis=1).rename(columns={'NFB':'NFE','NR1':'NFB','NR2':'NR'})
# df.drop(columns = ['NFB','NR'], inplace=True)
# Generating integer values (20)

counter_list        = []
fobj_list           = []
time_list           = []
y_global_list       = []
fobj_global_list    = []
initial_y_list      = []
line_search_list    = []

for i in range(2):
    # count time
    start_time = time.perf_counter()

    Ns  = random.randint(6, 22)
    NFE = random.randint(2, Ns-1)
    NFB = random.randint(NFE, Ns-1)
    NR1 = random.randint(2, Ns-1)
    # NR2 = random.randint(NR1+1, Ns-1)
    # NR3 = random.randint(NR2+1, Ns-1)
    
    print(
        'Ns  = {Ns}; ' \
        'NFE = {NFE}; '\
        'NFB = {NFB}; '\
        'NR1 = {NR1}; '\
        # 'NR2 = {NR2}; '\
    )

    # # Adding missing values
    # df.loc[len(df)] = [5,1,3,1,0.03486890497071899]
    # df.loc[len(df)+1] = [13,10,12,10,0.03785507026734513]


    # start with the first var combination
    # Ns = 6
    # NFE = 1

    y = [Ns, NFE, NFB, NR1]
    initial_y_list.append(y)

    meshr.update_config(
        Ns=Ns,
        NFE=NFE,
        NFB=NFB,
        reactive_trays=[NR1]
    )
    i = 0 # number of times solver is called
    fobj_best  = meshr.solve(solver="BARON")['Profit']

    # Initialize the combination manager 
    manager = CombinationManager()
    manager.history_set.update([tuple(y)])

    # batch = manager.generate_new_batch(y)

    best_bool = True
    y_best = y
    while best_bool:
        best_bool = False
        # Generate list of combinatory
        batch = manager.generate_new_batch(y)

        fobj_list = []
        for y_d in batch:
            [Ns, NFE, NFB, NR1] = y_d
            meshr.update_config(
                Ns=Ns,
                NFE=NFE,
                NFB=NFB,
                reactive_trays=[NR1]
            )
            Sol = meshr.solve(solver="BARON")
            Fobj = Sol['Profit']
            fobj_list.append(Fobj)
            i+=1 #counting solver calls

        fobj_challenger = min(fobj_list)
        challenger_idx =  fobj_list.index(fobj_challenger)
        print(fobj_challenger,fobj_best)
        if fobj_challenger < fobj_best:
            y_old = y #########
            fobj_best = fobj_challenger
            y = batch[challenger_idx]
            best_bool = True
            y_best = y

            # line search
            d = [b-a for a,b in zip(y_old,y)]
            line_search = True
            line_search_list.append(f"first point line search: {y}")
            while line_search:
                y_old = y
                y_new = [a+b for a,b in zip(y,d)]
                line_search_list.append('linesearch start')
                line_search_list.append(f"y = {y_new}; ")
                line_search_list.append(f"d = {d};")
                [Ns, NFE, NFB, NR1] = y_new
                meshr.update_config(
                    Ns=Ns,
                    NFE=NFE,
                    NFB=NFB,
                    reactive_trays=[NR1]
                )
                Sol = meshr.solve(solver="BARON")
                fobj = Sol['Profit']
                print('line_search\n')
                print(y_best,fobj_best,i)
                i+=1 #counting solver calls
                if fobj < fobj_best:
                    fobj_best = fobj
                    y_best = y_new
                    y = y_new
                else:
                    line_search = False

            # print(best,y)
    print(y_best,fobj_best,i)
    y_global_list.append(y_best)
    fobj_global_list.append(fobj_best)
    counter_list.append(i)
    end_time = time.perf_counter()
    time_list.append(end_time - start_time)

fobj_calls_mean = statistics.mean(counter_list)
fobj_calls_std = statistics.stdev(counter_list)
time_mean = statistics.mean(time_list)
time_std = statistics.stdev(time_list)

print("\n--- Final Results ---")
end_time = time.perf_counter()


print(f"Mean Execution time: {time_mean:.6f} seconds\n")
print(f"Mean of objective functions calls: {fobj_calls_mean}\n")
print(f"STD of objective functions calls: {fobj_calls_std}\n")
print(f"Best Discrete X found: {y_best}")
print(f"Minimum Objective Value: {fobj_best:.4e}")
print(f"Objective function evaluations: {fobj_calls_mean}")

with open("result/D-SDA_4D_optimization_results.txt", "a") as f:
    f.write(f"\n{'='*50}\n")
    f.write(f"Run date: {datetime.now()}\n")
    f.write(f"Mean Execution time: {time_mean:.6f} seconds\n")
    # f.write(f"Status: {status}\n")
    f.write(f"Mean of objective functions calls: {fobj_calls_mean}\n")
    f.write(f"STD of objective functions calls: {fobj_calls_std}\n")
    f.write(f"Best Discrete X found: {y_best}\n")
    f.write(f"Minimum Objective Value: {fobj_best}\n")
    f.write(f"All values: \n")
    for i, (f_val, g_val, h_val, j_val) in enumerate(zip(fobj_global_list, y_global_list, counter_list, initial_y_list), start=1):
        f.write(f"fobj_{i} = {f_val:.4e}; ")
        f.write(f"y_{i} = {g_val}; ")
        f.write(f"fobj_eval_{i} = {h_val}; ")
        f.write(f"initial_y_{i} = {j_val} \n")

with open("result/all_resultsD-SDA_4D_optimization_results.txt", "a") as file:
    for txt in line_search_list:
        file.write(f"{txt}\n")