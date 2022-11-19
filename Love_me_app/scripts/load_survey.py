import csv
from ..import models
import datetime
import os


def load_survey_from(db):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    row_count = 0
    try:
        with open(dir_path + '/survey.csv') as csv_file_first:
            row_count = sum(1 for line in csv_file_first) - 1
    except Exception as e:
        print(e)
    finally:
        with open(dir_path+'/survey.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            db_total = db.query(models.AiTrainer).count()

            print(db_total)
            print(row_count)
            if int(row_count) > int(db_total):
                print("Tknajsn vkas ")
                for row in csv_reader:
                    print("i3t892ruj")
                    if line_count <= db_total:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        new_trainer = models.AiTrainer(
                            ui_name=row[0],
                            ai_word=row[1],
                            date_created=datetime.datetime.now()
                        )
                        db.add(new_trainer)
                        try:
                            db.commit()
                            db.refresh(new_trainer)
                            print("nbjhvg hnkdvj")
                        except Exception as e:
                            print(str(e))
                        line_count += 1
