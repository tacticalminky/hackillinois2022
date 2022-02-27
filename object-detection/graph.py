import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_json("trash_data.json")
# print(data)

plastics = [0]
for i in data["Plastic"]:
    plastics.append(i + plastics[-1])

papers = [0]
for i in data["Paper"]:
    papers.append(i + papers[-1])

garbages = [0]
for i in data["Garbage"]:
    garbages.append(i + garbages[-1])

plt.plot(plastics, label="Plastic")
plt.plot(papers, label="Paper")
plt.plot(garbages, label="Garbage")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Units thrown")
plt.show()