import hashlib
import bisect

class ConsistentHash:
    def __init__(self, slots=512, virtual_nodes=9):
        self.slots = slots
        self.virtual_nodes = virtual_nodes
        self.hash_ring = []
        self.nodes = {}

    def _hash(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.slots

    def add_server(self, server_id):
        for j in range(self.virtual_nodes):
            vnode = f"{server_id}-{j}"
            h = self._hash(vnode)
            bisect.insort(self.hash_ring, h)
            self.nodes[h] = server_id

    def remove_server(self, server_id):
        to_remove = [h for h in self.nodes if self.nodes[h] == server_id]
        for h in to_remove:
            self.hash_ring.remove(h)
            del self.nodes[h]

    def get_server(self, key):
        if not self.hash_ring:
            return None
        h = self._hash(key)
        index = bisect.bisect_right(self.hash_ring, h) % len(self.hash_ring)
        return self.nodes[self.hash_ring[index]]
