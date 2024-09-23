class Node:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end
        self.link = -1  # Suffix link
        self.next = {}  # Outgoing edges; map from character to node

    def edge_length(self, position):
        """ Calculate the length of the edge leading to this node. """
        return min(self.end if self.end is not None else position + 1, position + 1) - self.start


class SuffixTree:
    """ The suffix tree. """
    def __init__(self, text):
        self.text = text
        self.build_text = ""
        self.root = self.active_node = Node(-1, -1)
        self.position = -1
        self.current_node = 0
        self.need_suffix_link = -1  # Indicates whether a node is waiting for a link
        self.remainder = 0
        self.active_edge = -1
        self.active_length = 0
        self.nodes = [self.root]

    def active_edge_char(self):
        """ Return the character at the active edge. """
        return self.text[self.active_edge]

                
    def find_node_index(self, node):
        """Find the index of the given node in the self.nodes list."""
        for index, current_node in enumerate(self.nodes):
            if current_node == node:
                return index
        return -1  # Vraća -1 ako čvor nije pronađen

    def walk_down(self, next_node):
        """ Walk down the tree following the path of the active edge and length. """
        if self.active_length >= self.nodes[next_node].edge_length(self.position):
            self.active_edge += self.nodes[next_node].edge_length(self.position)
            self.active_length -= self.nodes[next_node].edge_length(self.position)
            self.active_node = self.nodes[next_node]
            return True
        return False

    def new_node(self, start, end):
        """ Create a new node with given start and end indices. """
        node = Node(start, end)
        self.nodes.append(node)
        return len(self.nodes) - 1

    def add_char(self, char):
        """Add a new character to the suffix tree."""
        self.build_text += char
        self.position += 1
        self.remainder += 1
        self.need_suffix_link = -1
        last_created_internal_node = None
        step = 0

        while self.remainder > 0:
            step += 1
            if self.active_length == 0:
                self.active_edge = self.position

            if self.active_edge_char() not in self.active_node.next:
                # Rule 2 (New leaf edge)
                leaf_node = self.new_node(self.position, None)
                self.active_node.next[self.active_edge_char()] = leaf_node

                if last_created_internal_node is not None:
                    print("added link #1")
                    if(self.find_node_index(self.active_node) == -1):
                        raise ValueError("should not be -1")
                    last_created_internal_node.link = self.find_node_index(self.active_node)
                    last_created_internal_node = None

            else:
                next_node = self.active_node.next[self.active_edge_char()]
                if self.walk_down(next_node):
                    continue

                # Rule 3 (Extension of an existing edge)
                if self.text[self.nodes[next_node].start + self.active_length] == char:
                    if last_created_internal_node is not None and self.active_node != self.root:
                        print("adding link #2")
                        if(self.find_node_index(self.active_node) == -1):
                            raise ValueError("should not be -1")
                        last_created_internal_node.link = self.find_node_index(self.active_node)
                    print("rule 3 entered")
                    self.active_length += 1
                    break

                # Rule 2 (New internal node and leaf edge)
                print("rule 2 loweer")
                split_end = self.nodes[next_node].start + self.active_length
                internal_node = self.new_node(self.nodes[next_node].start, split_end)
                leaf_node = self.new_node(self.position, None)
                self.active_node.next[self.active_edge_char()] = internal_node
                self.nodes[internal_node].next[char] = leaf_node
                self.nodes[next_node].start += self.active_length
                self.nodes[internal_node].next[self.text[self.nodes[next_node].start]] = next_node

                if last_created_internal_node is not None:
                    print("adding another link #3")
                    last_created_internal_node.link = internal_node

                last_created_internal_node = self.nodes[internal_node]

            self.remainder -= 1

            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = self.position - self.remainder + 1
            else:
                self.active_node = self.nodes[self.active_node.link] if self.active_node.link != -1 else self.root

    def get_tree_structure_and_links(self, node=None, indent=0, suffix="", link=None, node_number=None):
            """Return the structure and links of the suffix tree as a nested dictionary."""
            if node is None:
                node = self.root

            structure = {'start': node.start, 'end': node.end, 'children': {}}
            if node.start != -1:  # If not the root node
                edge = self.text[node.start:node.end] if node.end is not None else self.text[node.start:]
                link_info = f" (Link: {link})" if link is not None else ""
                node_info = f" (Node: {node_number})" if node_number is not None else ""
                structure['label'] = f"{edge}{node_info}"
                structure['link'] = link
            for char, next_node in node.next.items():
                next_link = self.nodes[next_node].link if self.nodes[next_node].link != -1 else None
                structure['children'][char] = self.get_tree_structure_and_links(self.nodes[next_node], indent + 4, suffix + char, next_link, next_node)
            print(structure)
            return structure
    
    def extract_suffixes(self, node, text, current_suffix, suffixes):
        if not node['children']:  # If there are no children, it's a leaf node
            suffixes.append(current_suffix)
            return

        for char, child in node['children'].items():
            if child['end'] is None:
                suffix_label = text[child['start']:]  # If 'end' is None, use the rest of the text
            else:
                suffix_label = text[child['start']:child['end']]

            new_suffix = current_suffix + suffix_label
            self.extract_suffixes(child, text, new_suffix, suffixes)

    def get_suffixes(self, tree, text):
        suffixes = []
        self.extract_suffixes(tree, text, "", suffixes)
        return suffixes