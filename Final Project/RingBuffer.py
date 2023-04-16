class RingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.tail = -1
        self.head = 0
        self.size = 0

    '''
    Output useful variables
    '''
    def __str__(self):
        return f'Capacity: {self.capacity}\n Size: {self.size}\n Tail: {self.tail}\n Head: {self.head}'

    '''
    Add items to the ring buffer
    '''
    def enqueue(self, item):
        if self.size != self.capacity:
            self.tail = (self.tail + 1) % self.capacity
            self.queue[self.tail] = item
            self.size = self.size + 1
        else:
            print("Error: Ring Buffer is full!")

    '''
    Delete items from the ring buffer
    '''
    def dequeue(self):
        if self.size != -1:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.capacity
            self.size = self.size - 1
            return temp
        else:
            print("Error: Ring Buffer is empty!")

    '''
    Get the item at the front of the ring buffer
    '''
    def front(self):
        return self.queue[0]

    '''
    Get the item at the end of the ring buffer
    '''
    def end(self):
        return self.queue[self.size-1]

    '''
    Get the current size of the ring buffer
    '''
    def size(self):
        return self.size

    '''
    Get the maximum size of the ring buffer
    '''
    def maxsize(self):
        return self.capacity

    '''
    Check if the ring buffer is full or not
    '''
    def full(self):
        if self.size == self.capacity:
            return True
        else:
            return False

    '''
    Check if the ring buffer is empty or not
    '''
    def empty(self):
        if self.size == 0:
            return True
        else:
            return False

    '''
    Get an item at a specified index
    '''
    def getitem(self, index):
        if index < self.size:
            return self.queue[index]
        else:
            print("Error: Index greater than ring buffer size!")

    '''
    Remove and return an item from the ring buffer
    '''
    def display(self):
        if self.size != 0:
            index = self.head
            for i in range(self.size):
                print(self.queue[index])
                index = (index + 1) % self.capacity
        else:
            print("Ring Buffer is empty!")

