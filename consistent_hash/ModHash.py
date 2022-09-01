#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 rzavalet <rzavalet@noemail.com>
#
# Distributed under terms of the MIT license.

"""
An implementation of a Hash using mod.
Please implement the requiered methods.
"""

from HashScheme import HashScheme
import hashlib

class ModHash(HashScheme):

    def __init__(self):
        """
        You have to decide what members to add to the class
        """
        self.__scheme_name = 'Modular_Hash'
        pass

    def get_name(self):
        return self.__scheme_name

    def dump(self):
        """
        Auxiliary method to print out information about the hash
        """
        pass

    def add_node(self, new_node):
        """
        Creates a new node in the datastore. Once the node is created, a number
        of resources have to be migrated to conform to the hash schema.

        Important: Notice that this method is designed to work with a
        consistent hash. You may need to adjust it to make it work with modular
        hash. Hash_generator has a member "scheme_name" that you can use.
        """
        migracion = 0
        if(self.hash_generator.get_name() == "Consistent_Hash"):
            prev_node = self.hash_generator.hash(new_node)
            print("Previous node {0}".format(prev_node))

            rc = self.hash_generator.add_node(new_node)
            if rc == 0:
                self.nodes[new_node] = Node(new_node)

                """
                If there is a node in the counter clockwise direction, then the
                resources stored in that node need to be rebalanced (removed from a
                node and added to another one).
                """
                if prev_node is not None:
                    resources = self.nodes[prev_node].resources.copy() 

                    for element in resources:
                        target_node = self.hash_generator.hash(element)

                        if target_node is not None and target_node != prev_node:
                            migracion += 1
                            self.nodes[prev_node].resources.remove(element)
                            self.nodes[target_node].resources.append(element)
        
        elif (self.hash_generator.get_name() == "Modular_Hash"):
            not_in_array = True

            for i in self.nodes.values():
                if(i.name == new_node):
                    not_in_array = False
                    break

            if(not_in_array):

                self.hash_generator.add_node(new_node)
                resources = []
                for i in self.nodes.values():
                    resources += i.resources

                nodes_names = []
                migracion = len(resources)
                for i in self.nodes.values():
                    nodes_names.append(i.name)
                nodes_names.append(new_node)
                print(nodes_names)

                self.nodes = {}
                key = 0
                for i in nodes_names:
                    self.nodes[key] = Node(i)
                    key+=1
                print("Keys: {0}".format(self.nodes.keys()))
                for i in resources:
                    self.add_resource(i)
        else: 
            pass
        return migracion

    def remove_node(self, node):
        """
        Possibly just decrement a counter of number of nodes. You may also
        need to update Store to react in certain way depending on the
        scheme_name.
        """
        pass

    def hash(self, value):
        """
        Convert value to a number representation and then obtain mod(number_of_nodes)
        """
        pass
