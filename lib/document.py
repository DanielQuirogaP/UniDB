from .encryptor import *
from .hash_lib import find_index, update_index
from .write_data import write_index
from .read_data import get_index

import os
import json


class Document:

    def __init__(self, name, db, collection_index, parent=[]):
        self.parents = parent
        self.name = name
        self.db = db
        self.collection_index = collection_index
        self.doc_index = []

    def get(self):
        try:
            path = "dbs" + os.sep + self.db + os.sep + "docs" + os.sep + self.find_doc_path() + ".uni" #file name
            with open(path, 'r', encoding='cp037') as f:
                dic = decrypt_JSON("".join(f.readlines()))
            print(dic)
        except Exception as e:
            print("\n" + str(e) + "\n")
        pass

    def update(self, dic):
        try:
            path = "dbs"+ os.sep + self.db + os.sep + "docs" + os.sep + self.find_doc_path() + ".uni"
            with open(path, 'r', encoding='cp037') as f:
                actual_dic = decrypt_JSON("".join(f.readlines()))
            new_dic = dict(actual_dic, **dic)
            print(new_dic)
        except Exception as e:
            print("\n" + str(e) + "\n")
        pass

    def put(self, dic):
        try:
            path = "dbs" + os.sep + self.db + os.sep +"docs" + os.sep + self.find_doc_path(True) + ".uni"
            text = encrypt_JSON(dic)
            with open(path, 'w', encoding='cp037') as f:
                f.write(text)

            encrypted_address = ''
            for parent in self.parents:
                encrypted_address += encrypt_name(parent)

            index_path = "dbs" + os.sep + self.db + os.sep + "index" + os.sep + encrypted_address + ".uindx"
            name = encrypt_name(self.name)
            self.doc_index = write_index(name,index_path)

            print('file inserted ;D')
        except Exception as e:
            print("\n" + str(e) + "\n")
        pass

    def delete(self):
        try:
            path = "/dbs/" + self.db + "/docs/" + self.find_doc_path() + ".uni"
            print(path)
        except Exception as e:
            print("\n" + str(e) + "\n")
        pass

    def get_collection_index(self):
        return self.collection_index

    def find_doc_path(self, insert=False):
        path = ""
        doc_index = []
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

                pre_path = "dbs"+ os.sep + self.db + os.sep + "index"
                self.doc_index = get_index(os.path.join(pre_path, path+".uindx"))

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
                raise Exception("\nThe referred document " + self.name + " doesn't exist\n")
        return path
