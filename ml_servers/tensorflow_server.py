from multiprocessing import Process
import tensorflow as tf

class TensorFlowServer:
    def runServer(self, counter, clusterMembers=["localhost:2222", "localhost:2223"]):
        p = Process(target=self.launchTensorServer)
        p.start()
        counter.append(p)
    def launchTensorServer(self,task_index=0):
        cluster = tf.train.ClusterSpec({"local": ["45.42.12.32:43210", "54.198.217.133:43210"]})
        server = tf.train.Server(cluster, job_name="local", task_index=task_index)
        print("Starting server #{}".format(0))

        server.start()
        server.join()


if __name__ == '__main__':
    tensor = TensorFlowServer()
    tensor.launchTensorServer(1)