import subprocess


def extract_aux_result():
    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'xinit'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()
    out, err = proc2.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if str(err) == "":
        return str(out).split("\n")
    else:
        raise Exception("Got stderr=%s" % str(err))


def find_xinit_process(found_procs):
    for proc in found_procs:
        if "/home/gramar/.xinitrc" in proc:
            return proc

    raise Exception("Could not find xinit process")


def find_xinit_pid(xinit_proc_str):
    segmented = xinit_proc_str.split(" ")
    for segment in segmented:
        try:
            pid = int(segment)
            subprocess.call(["kill", str(pid)])
        except ValueError:
            pass


if __name__ == "__main__":
    aux = extract_aux_result()
    correct_proc = find_xinit_process(aux)
    find_xinit_pid(correct_proc)
