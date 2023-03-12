import subprocess
import numpy as np
import shutil
import os
import matplotlib.pyplot as plt

#SETTINGS
TARGETS = ["example_target.py"]

LB = -3
UB = 7
NUM_SAMPLES = 20
ITERATIONS = 5

xs = np.linspace(LB, UB, NUM_SAMPLES)

COMPILE_CMDS = []
RUN_CMD = "python3 example_target.py"

DENOTATION = '$$$'

#END SETTINGS

CWD = os.getcwd()
TEMP_DEST = os.path.join(os.getcwd(), "temp")
if not os.path.isdir(TEMP_DEST):
    os.mkdir(TEMP_DEST)
scores = []
ASPECT_RATIO = 0

plot_xs = []
plot_ys = []

for i in range(ITERATIONS):
    for x in xs:
        for target_name in TARGETS:
            new_content = ""
            with open(target_name, "r") as src_file:
                lines = src_file.readlines()
                for line in lines:
                    index = line.find(DENOTATION)
                    if index != -1:
                        line = line[0:index] + str(x) + line[(line.rfind(DENOTATION) + 3):]
                    new_content += line
            with open(os.path.join(TEMP_DEST, target_name), "w") as dest_file:
                dest_file.write(new_content)
        
        os.chdir(TEMP_DEST)

        for CMD in COMPILE_CMDS:
            subprocess.run(CMD)


        process = subprocess.Popen(RUN_CMD.split(' '),
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
        (out, err) = process.communicate()
        code = process.wait()

        if code != 0:
            print(err)
        else:
            score = float(out.decode("utf-8").strip())
            scores.append(score)
            print(str(x).ljust(25, ' '), score)
        
        os.chdir(CWD)

    best_index = np.argmax(scores)
    best_score = scores[best_index]
    best_x = xs[best_index]
    print("best_score", best_score)
    print("best_x", best_x)

    plot_xs.extend(xs)
    plot_ys.extend(scores)

    xs = np.linspace(xs[best_index - 1 if best_index != 0 else best_index], xs[best_index + 1 if best_index != len(xs) - 1 else best_index], NUM_SAMPLES)
    scores.clear()

plot_xs, plot_ys = zip(*sorted(zip(plot_xs, plot_ys)))

plt.plot(plot_xs, plot_ys)
plt.ylabel("score")
plt.xlabel("x")
plt.plot(best_x, best_score, 'ro')
plt.text(best_x, best_score, "best")
plt.show()

shutil.rmtree(TEMP_DEST)
print("exiting")