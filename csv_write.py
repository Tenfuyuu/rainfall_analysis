import os

def csv_generation(df_analysed, csv_name, title_text):
    output_dir = "output"
    output_file = os.path.join(output_dir, csv_name)

    with open(output_file, "w", encoding="utf-8-sig") as f:
        f.write(title_text)

    df_analysed.to_csv(output_file, mode="a", index=False, encoding="utf-8-sig")
    print("已完成的文件/Generated File：", output_file)