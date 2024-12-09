class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

# Function to build the Huffman Tree
def build_huffman_tree(char_prob):
    # Create a list of nodes
    nodes = [Node(char, prob) for char, prob in char_prob.items()]
    # Continue until the list contains only one node
    while len(nodes) > 1:
        # Sort the list of nodes by frequency
        nodes = sorted(nodes, key=lambda x: x.freq)
        # Get the two nodes with the smallest frequencies
        left = nodes.pop(0)
        right = nodes.pop(0)
        # Create a new internal node with these two nodes as children
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        # Add the merged node back to the list
        nodes.append(merged)
    # The remaining node is the root of the Huffman Tree
    return nodes[0]

# Function to generate Huffman codes from the Huffman Tree
def generate_codes(node, prefix="", codebook={}):
    if node is not None:
        # If this is a leaf node, it contains a character
        if node.char is not None:
            codebook[node.char] = prefix
        else:
            generate_codes(node.left, prefix + "0", codebook)        # Traverse the left subtree with the prefix '0'
            generate_codes(node.right, prefix + "1", codebook)       # Traverse the right subtree with the prefix '1'
    return codebook

def calculate_avg_bits(huffman_codes, char_prob):       # Function to calculate the average number of bits per codeword
    avg_bits = 0
    for char in huffman_codes:
        prob = char_prob[char]
        code_length = len(huffman_codes[char])
        avg_bits += prob * code_length
    return avg_bits

char_prob = {
    'a': 0.5,
    'b': 0.3,
    'c': 0.1,
    'd': 0.1,
}
huffman_tree = build_huffman_tree(char_prob)
huffman_codes = generate_codes(huffman_tree)
print("Huffman codewords for each character:")
for char, code in huffman_codes.items():
    print(f"{char}: {code}")
avg_bits_per_codeword = calculate_avg_bits(huffman_codes, char_prob)
print(f"Average number of bits per codeword: {avg_bits_per_codeword:.4f}")
print("for a 100 symbol sequence: ")
print("number of bits for encoding using ASCII = " , 100*8)
print("number of bits for encoding using Huffman = " , 100*avg_bits_per_codeword)
print("compression ratio using Huffman = ", (100*avg_bits_per_codeword) / (8 * 100))
