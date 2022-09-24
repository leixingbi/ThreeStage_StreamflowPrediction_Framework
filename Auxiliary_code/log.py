"""
Function:
    To output the execution logs to txt file
"""
import datetime


def log_(status):
    log_file = open(r"Result\\Logs.txt", "a")
    now_time = datetime.datetime.now()
    if status == "begin":
        log_file.write("\n\n----A new round of model execution------\n")
        log_file.write(str(now_time)+"\n")
    elif status == "end":
        log_file.write(str(now_time)+"\n")
        log_file.write("----A new round of model execution------\n")
    else:
        log_file.write("%s\n" % status)
    log_file.close()