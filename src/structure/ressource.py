import threading


class Ressource():
    """
    The class Ressource will solve the readers-writers problem
    with a writers-preference
    """
    def __init__(self, ressource):
        """
        The constructor will initialize all the semaphores
        """
        self.ressource = ressource
        self.sem_writer = threading.Semaphore()
        self.sem_reader = threading.Semaphore()
        self.sem_nb_writer = threading.Semaphore()
        self.sem_nb_reader = threading.Semaphore()
        self.nb_writer = 0
        self.nb_reader = 0

    def write(self, fun, *args):
        """
        This function permit to write in the ressource with
        a writer-preference
        """
        self.sem_nb_writer.aquire()
        self.nb_writer += 1
        if self.nb_writer == 1:
            self.sem_reader.acquire()
        self.sem_nb_writer.release()

        self.sem_writer.acquire()
        result = fun(*args)
        self.sem_writer.release()

        self.sem_nb_writer.acquire()
        self.nb_writer -= 1
        if self.nb_writer == 0:
            self.sem_reader.release()
        self.sem_nb_writer.release()
        return result

    def read(self, fun, *args):
        """
        This function read the ressource if there are no writers
        """
        self.sem_reader.acquire()
        self.sem_nb_reader.acquire()

        self.nb_reader += 1
        if self.nb_reader == 1:
            self.sem_writer.acquire()

        self.sem_nb_reader.release()
        self.sem_reader.release()

        result = fun(*args)

        self.sem_nb_reader.acquire()
        self.nb_reader -= 1
        if self.nb_reader == 0:
            self.sem_writer.release()

        self.sem_nb_reader.release()
        return result
