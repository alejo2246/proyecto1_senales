import numpy as np
import xml.etree.ElementTree as ET

class PatternAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.patterns_matrix, self.frequency_matrix = self.load_frequency_matrix()
        self.row_sums = self.compute_row_sums()
        self.group_order = self.compute_group_order()
    def generate_pattern_matrix(self, frequency_matrix):
      pattern_matrix = np.where(frequency_matrix > 0, 1, 0)
      return pattern_matrix
    def load_frequency_matrix(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        
        signals = root.findall("senal")
        patterns_matrix = []
        frequency_matrix = []
        
        for signal in signals:
            t = int(signal.get("t", 0))
            A = int(signal.get("A", 0))
            freq_matrix = np.zeros((t, A), dtype=int)
            
            for dato in signal.findall("dato"):
                time = int(dato.get("t", 0)) - 1
                amplitude = int(dato.get("A", 0)) - 1
                value = int(dato.text)
                freq_matrix[time, amplitude] = value
        
            frequency_matrix = freq_matrix
            patterns_matrix = self.generate_pattern_matrix(frequency_matrix)

        return patterns_matrix, frequency_matrix

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

    def display_results(self):
        print("\nValores únicos con grupos:")
        for pattern, group in self.group_order.items():
            indices = [i+1 for i, row in enumerate(self.patterns_matrix) if np.array_equal(row.flatten(), pattern)]
            sum_value = self.row_sums[pattern]
            print(f"g={group} (t= {', '.join(map(str, indices))}) {sum_value}")

def main():
    filename = "input.xml"
    pattern_analyzer = PatternAnalyzer(filename)
    pattern_analyzer.display_results()

if __name__ == "__main__":
    main()