import subprocess
import os
import signal
import time


def extract_aux_result():
    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'xmobar'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()
    out, err = proc2.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    print(out)
    if str(err) == "":
        return str(out).split("\n")
    else:
        raise Exception("Got stderr=%s" % str(err))


def find_xmobar_process(found_procs):
    for proc in found_procs:
        if "xmobar" in proc and "grep" not in proc and "restart" not in proc:
            return proc

    return None


def kill_xmonad(xinit_proc_str):
    segmented = xinit_proc_str.split(" ")
    for segment in segmented:
        try:
            pid = int(segment)
            res = subprocess.call(["kill", str(pid)])
            print("Killed %s with result %s" % (segment, res))
            break
        except ValueError:
            pass


def start_xmonad():
    pid = subprocess.Popen(['xmobar'], stdout=subprocess.PIPE).pid
    print("Restarted xmobar, new pid=%s" % pid)


def wait_for_new_xmonad():
    procs = extract_aux_result()
    it = 0
    proc = find_xmobar_process(procs)
    while proc is None and it < 10:
        time.sleep(0.1)
        it += 1
        proc = find_xmobar_process(extract_aux_result())
    return proc


def kill_term():
    os.kill(os.getppid(), signal.SIGHUP)


if __name__ == "__main__":
    aux = extract_aux_result()
    correct_proc = find_xmobar_process(aux)
    kill_xmonad(correct_proc)
    start_xmonad()
    time.sleep(5)
    wait_for_new_xmonad()
    # kill_term()
