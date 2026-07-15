import random
import statistics
from functions.comb_manager import CombinationManager
from gamspy_model.meshr_class import ReactiveDistillationModel
import numpy as np

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

counter_list = []
fobj_list = []
for i in range(2):

    Ns  = random.randint(6, 22)
    NFE = random.randint(2, Ns-1)
    NFB = random.randint(NFE, Ns-1)
    NR1 = random.randint(2, Ns-3)
    NR2 = random.randint(NR1+1, Ns-2)
    NR3 = random.randint(NR2+1, Ns-1)
    print(
        'Ns  = {Ns}; ' \
        'NFE = {NFE}; '\
        'NFB = {NFB}; '\
        'NR1 = {NR1}; '\
        'NR2 = {NR2}; '\
        'NR3 = {NR3}; '\
    )

    # # Adding missing values
    # df.loc[len(df)] = [5,1,3,1,0.03486890497071899]
    # df.loc[len(df)+1] = [13,10,12,10,0.03785507026734513]


    # start with the first var combination
    # Ns = 6
    # NFE = 1

    y = [Ns, NFE, NFB, NR1, NR2, NR3]

    meshr.update_config(
        Ns=Ns,
        NFE=NFE,
        NFB=NFB,
        reactive_trays=[NR1,NR2,NR3]
    )
    i = 0 # number of times solver is called
    best  = meshr.solve(solver="CONOPT")['Profit']

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
            [Ns, NFE, NFB, NR1, NR2, NR3] = y_d
            meshr.update_config(
                Ns=Ns,
                NFE=NFE,
                NFB=NFB,
                reactive_trays=[NR1,NR2,NR3]
            )
            Sol = meshr.solve(solver="CONOPT")
            Fobj = Sol['Profit']
            fobj_list.append(Fobj)

        challenger = min(fobj_list)
        challenger_idx =  fobj_list.index(challenger)
        print(challenger,best)
        if challenger < best:
            y_old = y #########
            best = challenger
            y = batch[challenger_idx]
            best_bool = True
            y_best = y

            # line search
            d = [a-b for a,b in zip(y,y_old)]
            line_search = True
            while line_search:
                y_old = y
                y_new = [a+b for a,b in zip(y,d)]
                [Ns, NFE, NFB, NR1, NR2, NR3] = y_new
                meshr.update_config(
                    Ns=Ns,
                    NFE=NFE,
                    NFB=NFB,
                    reactive_trays=[NR1,NR2,NR3]
                )
                Sol = meshr.solve(solver="CONOPT")
                Fobj = Sol['Profit']
                if Fobj < best:
                    best = Fobj
                    y_best = y
                else:
                    line_search = False

            # print(best,y)

    print(y_best,best,i)
    counter_list.append(i)

print(f'Mean = {statistics.mean(counter_list):.2f}')
print(f"STD = {statistics.stdev(counter_list):.2f}")
