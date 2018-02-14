import threading

class ressource:

    def __init__(self, ressource, nb_writer=0, nb_reader=0):
        self.ressource = ressource
        self.sem_writer = threading.semaphore()
        self.sem_reader = threading.semaphore()
        self.sem_nb_writer = threading.semaphore()
        self.sem_nb_reader = threading.semaphore()
        self.nb_writer = nb_writer
        self.nb_reader = nb_reader

    def write (self, fun):
        self.sem_nb_writer.aquire()
        self.sem_nb_writer+=1
        if self.sem_nb_writer==1:
            self.sem_reader.acquire()
        self.sem_writer.release()

        self.sem_writer.aqcuire()
        fun(self.ressource)
        self.sem_writer.release()

        self.sem_nb_writer.aqcuire()
        self.sem_nb_writer -= 1
        if self.nb_writer==0:
            self.sem_reader.release()
        self.sem_nb_writer.release()

    def read(self, fun):
        self.sem_reader.acquire()
        self.sem_nb_reader.acquire()

        self.sem_nb_reader += 1
        if self.sem_nb_reader == 1:
            self.sem_writer.acquire()

        self.sem_nb_reader.release()
        self.sem_reader.release()

        fun(self.ressource)

        self.sem_nb_reader.acquire()
        self.nb_reader -= 1
        if self.nb_reader == 0:
            self.sem_writer.release()

        self.sem_nb_reader.release()













