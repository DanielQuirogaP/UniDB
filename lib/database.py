import os
from .write_data import write_index
from .read_data import get_index
from .encryptor import encrypt_name
from .hash_lib import find_index


class Database:

    def __init__(self, name, database_index):
        self.database_index = database_index
        self.name = name
        self.enc_name = encrypt_name(name)

        if not find_index(self.enc_name, database_index):
            print('entro---------------------------')
            self.database_index = write_index(self.enc_name)
            root = "dbs"
            #new_path = os.path.join(root, self.enc_name)
            new_path = root + os.sep + self.enc_name
            print(new_path)

            os.mkdir(new_path)
            with open(os.path.join(new_path, "indexes.uindx"), 'w') as f:
                f.write("")
            os.mkdir(os.path.join(new_path, "index"))
            # coll_index_path = os.path.join(new_path, "index")
            # with open(os.path.join(coll_index_path, "indexes.uindx"), 'w') as f:
            #     f.write("")
            os.mkdir(os.path.join(new_path, "docs"))
        db = self.enc_name
        self.collection_index = self.load_collections()

    def load_collections(self):
        path = "dbs" + os.sep + self.enc_name
        return get_index(os.path.join(path, "indexes.uindx"))
