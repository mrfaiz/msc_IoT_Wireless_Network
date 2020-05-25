import re
import numpy as npy
import matplotlib.pyplot as plot


class DataReader:
    def __init__(self, file_name, sample_size, number_of_nodes, central_node):
        self.file_name = file_name
        self.sample_size = sample_size
        self.reliability = npy.empty(self.sample_size)
        self.latency = npy.empty(self.sample_size)
        self.number_of_node = number_of_nodes
        self.tempList = [""]
        self.read_file()
        self.reliability[0] = 100
        self.latency[0] = 0
        self.central_node = central_node

    def read_file(self):
        f = open(self.file_name, "r")
        for x in f:
            temp = x.strip()
            if len(temp) > 5:
                self.tempList.append(temp)

    def calculate_reliability(self):
        temp_reliability_array = []

        for validValue in self.tempList:
            res = re.match(r"(\d+)	ID:(\d+)	(\d+),(\d+)", validValue)
            if res:
                temp_reliability_array.append(validValue)

        for value in temp_reliability_array:
            res = re.match(r"(\d+)	ID:(\d+)	(\d+),(\d+)", value)
            if res:
                self.reliability[int(res.group(3))] = self.reliability[int(res.group(3))] + 1

        # for val in self.reliability:
        #     print(val)
            
        for i in range(1, self.sample_size):
            broad_casted_nodes = self.number_of_node - 1
            self.reliability[i] = round(((broad_casted_nodes - (broad_casted_nodes - self.reliability[i]))/broad_casted_nodes) * 100)

        print("Reliability (for 30 packets) "+str(self.number_of_node)+" nodes")
        for rel in self.reliability:
            print(rel)

        return self.reliability

    def calculate_latency(self):
        # temp_array = []
        key_value = {'packetID_nodeID': 000}
        for validValue in self.tempList:
            res = re.match(r"(\d+)	ID:(\d+)	(\d+),(\d+)", validValue)
            if res:
                temp_key = res.group(3) + "_" + res.group(4)
                key_value[temp_key] = int(res.group(1))
        i = 1
        pc = 0
        total_delay = 0
        packet_counter = 0
        for s in self.tempList:
            if "===================" in s:
                self.latency[i] = round(total_delay/packet_counter)
                i = i + 1
                packet_counter = 0
                total_delay = 0
            res2 = re.match(r"(\d+)	ID:(\d+)	(-?\d+)$", s)
            if res2:
                temp_key = str(i) + "_" + res2.group(2)
                if temp_key in key_value.keys():
                    packet_counter = packet_counter + 1
                    temp_delay = abs(key_value[temp_key] - int(res2.group(1)))
                    total_delay = total_delay + temp_delay
                    key_value[temp_key] = temp_delay
            # if i == 3:
            #     break

        print("Average Latency (for 30 packets) "+str(self.number_of_node)+" nodes")
        for val in self.latency:
            print(val)

        return self.latency



        # tempTimeArray = npy.empty(self.sample_size)
        # start_index = 1
        # for s in range(1,self.sample_size):
        #     temp = 0
        #     for nd in range(1, self.number_of_node):
        #         val = str(s)+","+str(nd)+","
        #         for data in self.tempList:
        #             if val in data:
        #                 temp = temp + 1
        #         # if s+""+nd in self.tempList:
        #         #     temp = temp + 1
        #     print(temp)

    def get_latency_data(self):
        return self.latency

    def get_reliability_data(self):
        for v in range(0, 100):
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

# obj25 = DataReader("data_25_nodes.txt", number_of_packets, 24)
# obj25.populate_data()
# latency_array25 = obj25.get_latency_data()
# # reliability_array25 = obj25.get_reliability_data()

# obj25_2 = DataReader("data_25_nodes_1.txt", number_of_packets, 24)
# obj25_2.populate_data()
# latency_array25_2 = obj25_2.get_latency_data()

# plotter.set_xlabel("Number of commands")
# plotter.set_ylabel("Latency(ms)")
# plotter.plot(packets_array, latency_array25, label="1st round")
# plotter.plot(packets_array, latency_array25_2, label="2nd round")
# plotter.legend()

# pdf.suptitle("Several rounds using 25 nodes")
# pdf.savefig("latency_25_nodes.pdf")
# pdf.savefig("latency_25_nodes.png")

number_of_packets = 31
packets_array = npy.arange(0, number_of_packets, 1)
pdf, plotter = plot.subplots()
for dd in packets_array:
    print(dd)

obj = DataReader("logs_9_nodes.txt", number_of_packets, 9, 25)
rel9 = obj.calculate_reliability()
lat9 = obj.calculate_latency()

obj25 = DataReader("logs_25_nodes.txt", number_of_packets, 25, 25)
rel25 = obj25.calculate_reliability()
lat25 = obj25.calculate_latency()

obj49 = DataReader("logs_49_nodes.txt", number_of_packets, 49, 25)
rel49 = obj49.calculate_reliability()
lat49 = obj49.calculate_latency()


# plotter.set_xlabel("Number of Packets")
# plotter.set_ylabel("Latency(ms)")
# plotter.plot(packets_array, lat9, label='9 nodes')
# plotter.plot(packets_array, lat25, label='25 nodes')
# plotter.plot(packets_array, lat49, label='49 nodes')
# plotter.legend()
# pdf.savefig("latency.pdf")


plotter.set_xlabel("Number of Packets")
plotter.set_ylabel("Average Reliability(%)")
plotter.plot(packets_array, rel9, label='9 nodes')
plotter.plot(packets_array, rel25, label='25 nodes')
plotter.plot(packets_array, rel49, label='49 nodes')
plotter.legend()
pdf.savefig("reliability.pdf")