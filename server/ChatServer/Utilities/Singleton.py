import threading


class Singleton(type):
    _lock = threading.Lock()
    _init_locks = {}
    _instances = {}

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            lock = cls._init_locks.get(cls.__name__)
            if lock is None:
                lock = threading.Lock()
                cls._init_locks[cls.__name__] = lock
            with lock:
                if not cls._instances.get(cls.__name__):
                    cls._instances[cls.__name__] = super(Singleton, cls).__call__(*args, **kwargs)
                return cls._instances[cls.__name__]

    @classmethod
    def clear_instance_references(cls):
        with cls._lock:
            cls._init_locks = {}
            cls._instances = {}
