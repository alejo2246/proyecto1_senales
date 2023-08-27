import numpy as np
import xml.etree.ElementTree as ET
import graphviz

class Signal:
    def __init__(self, patterns_matrix, frequency_matrix,t,A,name):
        self.patterns_matrix=patterns_matrix
        self.frequency_matrix=frequency_matrix
        self.row_sums = self.compute_row_sums()
        self.group_order = self.compute_group_order()
        self.t=t
        self.A=A
        self.name= name

    def compute_row_sums(self):
        row_sums = {}
        # Sumar las filas repetidas
        for pattern, frequency in zip(self.patterns_matrix, self.frequency_matrix):
            row_sums.setdefault(tuple(pattern), 0)
            row_sums[tuple(pattern)] += frequency
        return row_sums

    def compute_group_order(self):
        group_order = {pattern: i + 1 for i, pattern in enumerate(self.row_sums)}
        return group_order

        
class PatternAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.all_signals=self.load_frequency_matrix()

    def generate_pattern_matrix(self, frequency_matrix):
        pattern_matrix = np.where(frequency_matrix > 0, 1, 0)
        return pattern_matrix
    
    def load_frequency_matrix(self):
        tree = ET.parse(self.filename)
        root = tree.getroot() 
        signals = root.findall("senal")
        patterns_matrix = []
        frequency_matrix = []
        read_signals=[]
        
        for signal in signals:
            t = int(signal.get("t", 0))
            A = int(signal.get("A", 0))
            freq_matrix = np.zeros((t, A), dtype=int)
            
            for dato in signal.findall("dato"):
                time = int(dato.get("t", 0)) - 1
                amplitude = int(dato.get("A", 0)) - 1
                value = int(dato.text)
                freq_matrix[time, amplitude] = value
            name=signal.get('nombre','N/N')
            frequency_matrix = freq_matrix
            patterns_matrix = self.generate_pattern_matrix(frequency_matrix)
            read_signals.append(Signal(patterns_matrix,frequency_matrix,t,A,name))
        return read_signals

    def display_results(self):
        
        for signal in self.all_signals:
            g = graphviz.Digraph(format='png', filename=f'{signal.name}')

            g.edge(str(signal.name), 't=' + str(signal.t))
            g.edge(str(signal.name), 'A=' + str(signal.A))

            # Create a subgraph for each column
            for col_index in range(len(signal.frequency_matrix[0])):
                with g.subgraph() as subg:
                    subg.attr()
                    
                    # Create nodes for each element in the column
                    for row_index, row in enumerate(signal.frequency_matrix):
                        element = row[col_index]
                        subg.node(str(col_index) + '_' + str(row_index), label=str(element))

                # Link the first node in the column to signal.name
                subg.node(str(signal.name))
                first_node = str(col_index) + '_0'
                g.edge(str(signal.name), first_node)

            # Create edges between nodes within each column
            for col_index in range(len(signal.frequency_matrix[0])):
                for row_index in range(1, len(signal.frequency_matrix)):
                    prev_node = str(col_index) + '_' + str(row_index - 1)
                    curr_node = str(col_index) + '_' + str(row_index)
                    g.edge(prev_node, curr_node)

            g.view()
        
            g2 = graphviz.Digraph(format='png', filename=f'{signal.name} reducida')
            g2.edge(str(signal.name) + ' reducida', 'A=' + str(signal.A))
            reduced_matrix = []

            for pattern, group in signal.group_order.items():
                indices = [i + 1 for i, row in enumerate(signal.patterns_matrix) if np.array_equal(row.flatten(), pattern)]
                sum_value = signal.row_sums[pattern]
                row = [f"g={group} (t= {', '.join(map(str, indices))})"] + list(map(str, sum_value))
                reduced_matrix.append(row)
            print(reduced_matrix[0])
            # Create nodes for each element in the matrix
            for col_index in range(len(reduced_matrix[0])):
                with g2.subgraph() as subg2:
                    subg2.attr()
                    
                    # Create nodes for each row in the column
                    for row_index, row in enumerate(reduced_matrix):
                        element = row[col_index]
                        subg2.node(str(row_index) + '_' + str(col_index), label=str(element))
                        
                # Link the first node in the column to signal.name
                subg2.node(str(signal.name) + ' reducida')
                first_node = str(0) + '_' + str(col_index)
                g2.edge(str(signal.name) + ' reducida', first_node)

            # Create edges between nodes within each column
            for col_index in range(len(reduced_matrix[0])):
                for row_index in range(1, len(reduced_matrix)):
                    prev_node = str(row_index - 1) + '_' + str(col_index)
                    curr_node = str(row_index) + '_' + str(col_index)
                    g2.edge(prev_node, curr_node)

            g2.view()

def main():
    filename = "input.xml"
    pattern_analyzer = PatternAnalyzer(filename)
    pattern_analyzer.display_results()

if __name__ == "__main__":
    main()