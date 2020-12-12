from .encryptor import *
from .hash_lib import find_index
from .read_data import get_index
from .write_data import write_index

import os
import json


class Collection:
    def __init__(self, name, db, collection_index, parent=[]):
        self.parents = parent
        self.name = name
        self.db = db
        self.collection_index = collection_index
        self.doc_index = []

    def getDocs(self):
        try:
            path = "dbs" + os.sep + self.db + os.sep + "indexes.uindx"
            self.collection_index = get_index(path)
            path = "/dbs/" + self.db + "/index/" + self.find_doc_path() + ".uindx"
            docs = []
            for index in self.doc_index:
                if index != ['']:
                    for file_name in index:
                        name = decrypt_name(file_name)
                        docs.append(name)
            print(docs)
            print("\nOk\n")
        except Exception as e:
            print("\nError: " + str(e) + "\n")

    def put(self, dic):
        try:
            path = "dbs/" + self.db + "/index/" + self.find_doc_path(insert=True) + ".uindx"  # col direction
            print('termino daniel')
            # create new name (beta)
            name = path[:7]
            name = name.replace('/', str(len(name)))
            file_encrypted_name = encrypt_name(name)
            # create file
            encrypt_file = encrypt_JSON(dic)
            with open("dbs" + os.sep + self.db + os.sep + 'docs' + os.sep + file_encrypted_name + '.uni', 'w',
                      encoding='cp037') as f:
                f.write(encrypt_file)

            # update index
            self.doc_index = write_index(file_encrypted_name, path)
            # write index
            print("\nOk\n")
        except Exception as e:
            print("\n" + str(e) + "\n")

    def get_collection_index(self):
        return self.collection_index

    def find_doc_path(self, insert=False):
        if len(self.parents) == 0:
            path = encrypt_name(self.name)
            if not find_index(path, self.collection_index):
                if insert:
                    # Creates the doc_index file of the collection
                    pre_path = "dbs" + os.sep + self.db + os.sep + "index"
                    with open(os.path.join(pre_path, path + ".uindx"), 'w') as f:
                        f.write("")

                    self.collection_index = write_index(path, "dbs" + os.sep + self.db + os.sep + "indexes.uindx")

                else:
                    raise Exception("\nThe collection " + self.name + " doesn't exist\n")
            pre_path = "dbs" + os.sep + self.db + os.sep + "index"
            self.doc_index = get_index(os.path.join(pre_path, path + ".uindx"))
            # pre_path = "dbs" + os.sep + self.db + os.sep + "index"
            # path = os.path.join(pre_path, path + ".uindx")
        else:
            path = ""
            self.doc_index = []
            for i in range(len(self.parents)):
                encrypted = encrypt_name(self.parents[i])
                last_path = path
                path += encrypted

                if i % 2 == 0:  # collection

                    if not find_index(path, self.collection_index):
                        if insert:

                            # Creates the doc_index file of the collection
                            pre_path = "dbs" + os.sep + self.db + os.sep + "index"
                            with open(os.path.join(pre_path, path + ".uindx"), 'w', encoding='cp037') as f:
                                f.write("")

                            if i != 0:
                                pre_path = "dbs" + os.sep + self.db + os.sep + "docs"
                                with open(os.path.join(pre_path, last_path + ".uni"), 'r') as f:
                                    dic = decrypt_JSON("".join(f.readlines()))
                                indexes = dic.get("collections")
                                if indexes is None:
                                    indexes = []
                                indexes.append(path)
                                dic["collections"] = indexes
                                text = encrypt_JSON(dic)
                                with open(os.path.join(pre_path, last_path + ".uni"), 'w', encoding="cp037") as f:
                                    f.write(text)

                            self.collection_index = write_index(path,
                                                                "dbs" + os.sep + self.db + os.sep + "indexes.uindx")

                        else:
                            raise Exception("\nThe collection " + self.parents[i] + " doesn't exist\n")

                    pre_path = "dbs" + os.sep + self.db + os.sep + "index"
                    self.doc_index = get_index(os.path.join(pre_path, path + ".uindx"))

                else:  # document

                    if not find_index(path, self.doc_index):
                        if insert:  # create new document

                            # creates the new JSON document
                            pre_path = "dbs" + os.sep + self.db + os.sep + "docs"
                            text = encrypt_JSON({})
                            with open(os.path.join(pre_path, path + ".uni"), 'w') as f:
                                f.write(text)
                            # Updates the doc_index of the collection
                            pre_path = "dbs" + os.sep + self.db + os.sep + "index" + os.sep + last_path + ".uindx"
                            write_index(path, pre_path)

                        else:
                            raise Exception("\nThe referred document " + self.parents[i] + " doesn't exist\n")
            encrypted = encrypt_name(self.name)
            last_path = path
            path += encrypted
            if not find_index(path, self.collection_index):
                if insert:

                    # Creates the doc_index file of the collection
                    pre_path = "dbs" + os.sep + self.db + os.sep + "index"
                    with open(os.path.join(pre_path, path + ".uindx"), 'w', encoding='cp037') as f:
                        f.write("")
                    pre_path = "dbs" + os.sep + self.db + os.sep + "docs"
                    with open(os.path.join(pre_path, last_path + ".uni"), 'r') as f:
                        dic = decrypt_JSON("".join(f.readlines()))
                    indexes = dic.get("collections")
                    if indexes is None:
                        indexes = []
                    indexes.append(path)
                    dic["collections"] = indexes
                    text = encrypt_JSON(dic)
                    print(text)
                    with open(os.path.join(pre_path, last_path + ".uni"), 'w', encoding="cp037") as f:
                        f.write(text)

                    self.collection_index = write_index(path,
                                                        "dbs" + os.sep + self.db + os.sep + "indexes.uindx")

                else:
                    raise Exception("\nThe collection " + self.name + " doesn't exist\n")

            pre_path = "dbs" + os.sep + self.db + os.sep + "index"
            self.doc_index = get_index(os.path.join(pre_path, path + ".uindx"))
        return path
