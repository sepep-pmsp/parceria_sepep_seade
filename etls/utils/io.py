from .path import solve_dir, solve_path

def save_df_as_csv(df, fname, folder, **csv_kwargs):

    fpath = solve_path(fname, parent=folder)
    df.to_csv(fpath, **csv_kwargs)


