import subprocess
import numpy as np
import sys
import matplotlib.pyplot as plt

TARGETS = ["target.py"]

LB = 0
UB = 5
H = .1
xs = np.linspace(LB, UB, int((UB - LB) / H) + 1)
print(xs)

COMPILE_CMDS = []
RUN_CMD = "python3 copy_of_target.py"

scores = []

for x in xs:
    for target_name in TARGETS:
        new_content = ""
        with open(target_name, "r") as src_file:
            lines = src_file.readlines()
            for line in lines:
                index = line.find('$$$')
                if index != -1:
                    line = line[0:index] + str(x) + line[(line.rfind('$$$') + 3):]
                new_content += line
        with open("copy_of_" + target_name, "w") as dest_file:
            dest_file.write(new_content)
    
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

best_index = np.argmax(scores)
print("best_score", scores[best_index])
print("best_x", xs[best_index])

plt.plot(xs, scores)
plt.ylabel("score")
plt.xlabel("x")
plt.show()

print("exiting")