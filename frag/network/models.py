from rdkit import Chem

from frag.utils.network_utils import get_num_ring_atoms, get_type, simplified_graph


class NodeHolder(object):
    """
    A Class to hold a series of nodes
    """
    def __init__(self):
        self.node_list = []
        self.edge_list = []

    def create_or_retrieve_node(self, child_smi):
        new_node = Node(Chem.MolFromSmiles(child_smi))
        new_node_list = [x for x in self.node_list if x == new_node]
        if new_node_list:
            return new_node_list[0], False
        self.node_list.append(new_node)
        return new_node, True

    def create_or_retrieve_edge(self, excluded_smi, child_smi, input_node, new_node):
        """

        :param excluded_smi:
        :param child_smi:
        :param input_node:
        :param new_node:
        :return:
        """
        new_edge = Edge(excluded_smi, child_smi, input_node, new_node)
        new_edge.NODES = []
        self.edge_list.append(new_edge)
        return new_edge

    def get_edges(self):
        """
        :return:
        """
        return set(self.edge_list)

class Node(object):
    """
    A Class to hold a Node on the graph
    """
    def __eq__(self, other):
        return self.SMILES==other.SMILES

    def __init__(self,input_mol=None):
        if not input_mol:
            return
        if type(input_mol) == str:
            input_mol = Chem.MolFromSmiles(input_mol)
        self.SMILES = Chem.MolToSmiles(input_mol, isomericSmiles=True)
        self.HAC = input_mol.GetNumHeavyAtoms()
        self.RAC,split_indices = get_num_ring_atoms(input_mol)
        self.RING_SMILES = simplified_graph(self.SMILES)
        self.RDMol = input_mol
        self.EDGES = []

    def __str__(self):
        return " ".join(["NODE", self.SMILES, str(self.HAC), str(self.RAC), self.RING_SMILES])


class Edge(object):
    """
    A Class to hold an edge
    """

    def __eq__(self, other):
        return str(self) == str(other)

    def __init__(self, excluded_smi, rebuilt_smi, node_one, node_two):
        self.EXCLUDE_SMILES = Chem.MolToSmiles(Chem.MolFromSmiles(excluded_smi),isomericSmiles=False)
        self.EXCLUDE_TYPE = get_type(excluded_smi)
        self.REBUILT_SMILES = Chem.MolToSmiles(Chem.MolFromSmiles(rebuilt_smi),isomericSmiles=False)
        self.REBUILT_RING_SMILES = simplified_graph(rebuilt_smi)
        self.REBUILT_TYPE = get_type(rebuilt_smi)
        self.EXCLUDED_RING_SMILES = simplified_graph(excluded_smi)
        self.NODES = [node_one, node_two]

    def __str__(self):
        return "".join(["EDGE"," ", self.NODES[0].SMILES," ", self.NODES[1].SMILES," ", \
        self.EXCLUDE_TYPE,"|", self.EXCLUDE_SMILES,"|", self.EXCLUDED_RING_SMILES,"|", \
        self.REBUILT_TYPE,"|", self.REBUILT_SMILES,"|", self.REBUILT_RING_SMILES])


class Attr(object):
    """
    A Class of attributes
    """

    def __init__(self, smiles, property_list):
        self.SMILES = smiles
        self.PROP_LIST = property_list

    def __str__(self):
        tot_list=  ["ATTR",self.SMILES]
        tot_list.extend(self.PROP_LIST)
        return " ".join(tot_list)