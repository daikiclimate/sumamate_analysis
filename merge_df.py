import pandas as pd
import os
import tqdm

def main(output_dir = "output/"):
    files = os.listdir(output_dir)

    dfs = []
    for i, f in tqdm.tqdm(enumerate(files)):
        _df = pd.read_excel(output_dir + f, index_col = 0)
        dfs.append(_df)
    df = pd.concat(dfs)
    df = df.reset_index().drop(columns = "index")
    df = df.sort_values("room_id")
    df.to_excel("all_sumamate11_log.xlsx")

def merge_tmp():
    df1 = pd.read_excel("all_sumamate11_log.xlsx", index_col = 0)
    df2 = pd.read_excel("sumamate_log.xlsx", index_col = 0)
    df = pd.concat([df1, df2])
    df.to_excel("all_merged_sumamate13_log.xlsx")


if __name__=="__main__":
    # main()
    merge_tmp()
