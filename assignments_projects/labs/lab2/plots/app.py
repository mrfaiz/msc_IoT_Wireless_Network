import re
import numpy as npy
import matplotlib.pyplot as plot


class DataReader:
    def __init__(self, file_name, sample_size,number_of_nodes):
        self.file_name = file_name
        self.sample_size = sample_size
        self.reliability = npy.empty(self.sample_size)
        self.latency = npy.empty(self.sample_size)
        self.number_of_node = number_of_nodes
        self.tempList = [""]
        self.read_file()

    def read_file(self):
        f = open(self.file_name, "r")
        for x in f:
            temp = x.strip()
            if len(temp) > 5:
                self.tempList.append(temp)

    def populate_data(self):
        tempTimeArray = npy.empty(self.sample_size + 1)
        start_index = 1
        for s in self.tempList:
            # print(s)
            if "bCast#" in s:
                # 31001	ID:5	bCast#: 1
                res = re.match(r"(\d+)	ID:(\d+)	bCast#: (\d+)", s)
                if res:
                    tempTime = int(res.group(1))
                    self.reliability[int(res.group(3)) - start_index] = 0
                    self.latency[int(res.group(3)) - start_index] = tempTime
                    tempTimeArray[int(res.group(3)) - start_index] = tempTime
            else:
                # 121001	ID:5	bCast#: 4
                m = re.match(r"(\d+)	ID:(\d+)	(\d+),(\d+)", s)
                if m:
                    # m = re.match(r"(\d+)	ID:(\d+)", s)
                    time = int(m.group(1))
                    self.reliability[int(m.group(3)) - start_index] = self.reliability[int(m.group(3)) - start_index] + 1
                    if time > self.latency[int(m.group(3)) - start_index]:
                        self.latency[int(m.group(3)) - start_index] = time
        for i in range(0, 100):
            self.latency[i] = self.latency[i] - tempTimeArray[i]

    def get_latency_data(self):
        return self.latency

    def get_reliability_data(self):
        for v in range(0,100):
            self.reliability[v] = (self.reliability[v]*100)/self.number_of_node

        return self.reliability


#
# f = open("data_25_nodes.txt", "r")
# tempArray = [""]
# for x in f:
#     temp = x.strip()
#     if len(temp) > 5:
#         tempArray.append(temp)
#
# reliability = npy.empty(101)
# latency = npy.empty(101)
# reliability[0] = 0.0
# latency[0] = 0.0
# packets = npy.arange(0, 101, 1)
# packets[0] = 0.0
# tempTimeArray = npy.empty(101)
#
# for s in tempArray:
#     # print(s)
#     if "bCast#" in s:
#         # 31001	ID:5	bCast#: 1
#         res = re.match(r"(\d+)	ID:(\d+)	bCast#: (\d+)", s)
#         if res:
#             tempTime = int(res.group(1))
#             reliability[int(res.group(3))] = 0
#             latency[int(res.group(3))] = tempTime
#             tempTimeArray[int(res.group(3))] = tempTime
#     else:
#         # 121001	ID:5	bCast#: 4
#         m = re.match(r"(\d+)	ID:(\d+)	(\d+),(\d+)", s)
#         if m:
#             # m = re.match(r"(\d+)	ID:(\d+)", s)
#             time = int(m.group(1))
#             reliability[int(m.group(3))] = reliability[int(m.group(3))] + 1
#             if time > latency[int(m.group(3))]:
#                 latency[int(m.group(3))] = time
#
# for i in range(1, 101):
#     latency[i] = latency[i] - tempTimeArray[i]
#
# for t in reliability:
#     print(t)

number_of_packets = 100
packets_array = npy.arange(0, number_of_packets, 1)
# packets_array[0] = 0
# obj9 = DataReader("data_9_nodes.txt", number_of_packets, 8)
# obj9.populate_data()
# latency_array9 = obj9.get_latency_data()
# reliability_array9 = obj9.get_reliability_data()
#
# obj25 = DataReader("data_25_nodes.txt", number_of_packets, 24)
# obj25.populate_data()
# latency_array25 = obj25.get_latency_data()
# reliability_array25 = obj25.get_reliability_data()
#
# obj49 = DataReader("data_49_nodes.txt", number_of_packets, 48)
# obj49.populate_data()
# latency_array49 = obj49.get_latency_data()
# reliability_array49 = obj49.get_reliability_data()

pdf, plotter = plot.subplots()

# plotter.set_xlabel("Number of Packets")
# plotter.set_ylabel("Latency(ms)")
# plotter.plot(packets_array, latency_array9, label='9 nodes')
# plotter.plot(packets_array, latency_array25, label='25 nodes')
# plotter.plot(packets_array, latency_array49, label='49 nodes')
# plotter.legend()
# pdf.savefig("latency.pdf")


# plotter.set_xlabel("Number of Packets")
# plotter.set_ylabel("Reliability(%)")
# plotter.plot(packets_array, reliability_array9, label='9 nodes')
# plotter.plot(packets_array, reliability_array25, label='25 nodes')
# plotter.plot(packets_array, reliability_array49, label='49 nodes')
# plotter.legend()
# pdf.savefig("reliability.png")

# plotter.set_xlabel("Number of Packets")
# plotter.set_ylabel("Latency(ms)")
# plotter.plot(packets_array, latency_array9, label='9 nodes ')
# plotter.plot(packets_array, latency_array25, label='25 nodes')
# plotter.legend()
# pdf.savefig("latency.pdf")

obj25 = DataReader("data_25_nodes.txt", number_of_packets, 24)
obj25.populate_data()
latency_array25 = obj25.get_latency_data()
# reliability_array25 = obj25.get_reliability_data()

obj25_2 = DataReader("data_25_nodes_1.txt", number_of_packets, 24)
obj25_2.populate_data()
latency_array25_2 = obj25_2.get_latency_data()

plotter.set_xlabel("Number of commands")
plotter.set_ylabel("Latency(ms)")
plotter.plot(packets_array, latency_array25, label="1st round")
plotter.plot(packets_array, latency_array25_2, label="2nd round")
plotter.legend()

pdf.suptitle("Several rounds using 25 nodes")
pdf.savefig("latency_25_nodes.pdf")
pdf.savefig("latency_25_nodes.png")
