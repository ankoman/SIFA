import csv
from fire import Fire
from typing import NamedTuple

class result(NamedTuple):
    n_enc: int
    ave_score_correct: float
    ave_score_wrong_min: float
    ave_n_ineff_ef: float
    ave_rank: float
    attacked: str

def main(alpha_hyp, beta_hyp, ANALYSIS_TYPE = "inef"):

    for alpha_act in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        for beta_act in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:

            filename = f"{ANALYSIS_TYPE}-a_act{alpha_act}-b_act{beta_act}-a_hyp{alpha_hyp}-b_hyp{beta_hyp}.csv"

            attacked_enc = 0
            with open(f'res/inef/{alpha_hyp}_{beta_hyp}/' + filename) as f:
                reader = csv.reader(f)
                next(reader)    ### Header skip
                for row in reader:
                    res = result(*row)
                    if res.attacked == "True":
                        attacked_enc = int(res.n_enc)
                        if float(res.ave_rank) > 30:
                            print('*', end='')
                        print(f'{attacked_enc:06}, ', end='')
                        break
                    elif float(res.ave_rank) == 256.0:
                        attacked_enc = int(res.n_enc)
                        print(f'{-int(res.n_enc):06}, ' , end='')
                        break
            if attacked_enc == 0:
                print(f'{attacked_enc:06}, ', end='')
        print('')

if __name__ == '__main__':
    Fire(main)