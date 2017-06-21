from multiprocessing import Process
import tensorflow as tf

class TensorFlowServer:
    def runServer(self, task_index, own_url):
        p = Process(target=self.launchTensorServer)
        p.start()
    
    
    def launchTensorServer(self,task_index=0, own_url="worker1.example.com:2222"):
        cluster = tf.train.ClusterSpec({"local":  {task_index: own_url},})
        server = tf.train.Server(cluster, job_name="local", task_index=task_index)
        print("Starting server #{}".format(0))

        server.start()
        server.join()


if __name__ == '__main__':
    tensor = TensorFlowServer()
    tensor.launchTensorServer(1)