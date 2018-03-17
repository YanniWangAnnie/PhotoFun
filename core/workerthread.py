from threading import Thread

class WorkerTread(Thread):

    def run(self):
        self.status = None
        try:
            Thread.run(self)
        except Exception as ex:
            self.status = ex
        else:
            self.status = 'success'