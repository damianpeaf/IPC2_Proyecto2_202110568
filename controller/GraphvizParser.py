

import os
from classes.Client import Client
from controller.Simulation import Simulation


class GraphvizParser():

    def __init__(self, simulation: Simulation) -> None:
        self.simulation = simulation
        self.dotStr = ""

    def createPDF(self):

        self.createDotFile()
        os.system(f'cd reports && dot -Tpdf {self.filename}.dot -o {self.filename}.pdf')

        filePath = os.path.join(os.getcwd(), 'reports', self.filename+'.pdf')
        os.startfile(filePath)

    def createDotFile(self):
        self.init()
        self.filename = self.simulation.attentionPoint.name.replace(' ', '_')+"_"+str(self.simulation.reportNumber)
        try:
            file = open('./reports/'+self.filename + ".dot", "x", encoding="utf-8")
            file.write(self.dotStr)
            file.close()
        except:
            try:
                file = open('./reports/'+self.filename + ".dot", "w", encoding="utf-8")
                file.write(self.dotStr)
                file.close()
            except:
                print("Error al crear el archivo dot")

    def getClientsNodes(self) -> str:
        nodes = ""
        i = self.simulation.attentionPoint.clients.size-1
        while i >= 0:
            client = self.simulation.attentionPoint.clients.getItem(i)
            nodes += f'client{i} [label="{client.name}", labelloc=\"b\"]\n'
            i -= 1
        return nodes

    def getClientsRank(self) -> str:
        i = self.simulation.attentionPoint.clients.size-1
        rank = "{rank=same; "
        while i >= 0:
            rank += f'client{i} '
            i -= 1

        rank += "}"
        return rank

    def getClientsEdges(self) -> str:
        edges = ""
        i = self.simulation.attentionPoint.clients.size-1
        while i > 0:
            edges += f'client{i} -> client{i-1}\n'
            i -= 1
        return edges

    def getAttendanceNodes(self) -> str:
        nodes = ""
        for i in range(0, self.simulation.attentionPoint.activeDesktops.size):
            desktop = self.simulation.attentionPoint.activeDesktops.getItem(i)
            client: Client = desktop.attendentClient
            if desktop.attendentClient is not None:
                nodes += f'attendentClient{i} [label="{client.name}"shape=proteinstab,labelloc=\"b\",group=0]\n'
                nodes += f'activeDesktop{i} [label="Escritorio {i+1}\n{desktop.attendant}",shape=box3d, group=1]\n'
                nodes += f'transaction{i} [label="{client.getTransactionsAsStr()}",shape=component,group=2]\n'
                nodes += f'time{i} [label="{client.getTransactionTotalTimeAsStr()}",shape=Mcircle,group=3]\n'
            else:
                nodes += f'attendentClient{i} [label="Escritorio libre", shape=box,labelloc=\"b\",group=0]\n'
                nodes += f'activeDesktop{i} [label="Escritorio {i+1}\n{desktop.attendant}",shape=box3d, group=1]\n'
                nodes += f'transaction{i} [label="-",shape=component,group=2]\n'
                nodes += f'time{i} [label="-",shape=Mcircle,group=3]\n'
        return nodes

    def getAttendanceRank(self) -> str:
        rank = ""
        for i in range(0, self.simulation.attentionPoint.activeDesktops.size):
            rank += "{rank=same; "
            rank += f'attendentClient{i} ->'
            rank += f'activeDesktop{i} ->'
            rank += f'transaction{i} ->'
            rank += f'time{i}'
            rank += "}\n"
        return rank

    def getActiveDesktopEdges(self) -> str:
        edges = ""
        for i in range(0, self.simulation.attentionPoint.activeDesktops.size-1):
            edges += f'activeDesktop{i} -> activeDesktop{i+1}\n'
        return edges

    def getInactiveDesktopNodes(self) -> str:
        nodes = ""
        for i in range(0, self.simulation.attentionPoint.inactiveDesktops.size):
            desktop = self.simulation.attentionPoint.inactiveDesktops.getItem(i)
            nodes += f'inactiveDesktop{i} [label="Escritorio {i+1}\n{desktop.attendant}",shape=box3d, group=0]\n'
        return nodes

    def getInactiveDesktopEdges(self) -> str:
        edges = ""
        for i in range(0, self.simulation.attentionPoint.inactiveDesktops.size-1):
            edges += f'inactiveDesktop{i} -> inactiveDesktop{i+1}\n'
        return edges

    def getInfoNode(self):
        return f'info [label="{self.simulation.getSimulationInfoAsStr()}\", shape=box]'

    def init(self):

        self.dotStr = """
digraph G{

  label=\""""+self.simulation.attentionPoint.name + " - Tiempo trancurrido " + self.simulation.getChronometerAsStr() + """\";

  subgraph cluster_queue {
    node [style=filled,color=black,shape=proteinstab];

    // Clientes nodes
    """+self.getClientsNodes()+"""

    // Clientes rank
    """+self.getClientsRank()+"""

    // Clientes edges
    """+self.getClientsEdges()+"""

    label = "Fila de espera";
  }

  subgraph cluster_active {
    node [style=filled];
    edge [arrowhead=\"none\"];


    // Client, desktops, transactions and time nodes
    """+self.getAttendanceNodes()+"""

    // Client, desktops, transactions and time ranks
    """+self.getAttendanceRank()+"""

    //Desktop edges
    """+self.getActiveDesktopEdges()+"""

    label = "Escritorios activos";
    color=blue
  }

  subgraph cluster_inactive {

    edge [arrowhead="none"];

    // Desktops nodes
    """+self.getInactiveDesktopNodes()+"""

    // Desktops edges
    """+self.getInactiveDesktopEdges()+"""

    label="Escritorios inactivos";
    color=red
  }

    subgraph cluster_information {

    """+self.getInfoNode()+"""
    label="Informacion";
    color=green
  }
}"""
