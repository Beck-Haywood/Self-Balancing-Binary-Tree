# Followed and studied from youtube tutorial: https://www.youtube.com/watch?v=lxHF-mVdwK8&ab_channel=BrianFaure
class AVLTreeNode:
	def __init__(self, value = None):
	  self.parent = None  # Parent Node
	  self.right = None  # Right Child Pointer
	  self.left = None  # Left Child Pointer
	  self.value = value  # Value of node
	  self.height = 1  # Height for current node(Distance to leaf)
# Time complexity AVL trees are awesome b/c all operations are O(log n)! Average and Worst case.
# Space complexity O(n) for all operations 
class AVLTree:
	def __init__(self):
		self.root = None # Top node in tree, the start

	def __repr__(self):  #---------------------------------------------------This function allows you to see the tree when we print it, 
		if self.root == None: #----------------------------------------------I did not write this function or attempted to understand it.
			return ''
		content = '\n'
		current_nodes = [self.root]
		current_height = self.root.height
		sep = ' '*(2**(current_height-1))
		while True:
			current_height += -1 
			if len(current_nodes) == 0: break
			cur_row=' '
			next_row=''
			next_nodes=[]
			if all(n is None for n in current_nodes):
				break
			for n in current_nodes:
				if n == None:
					cur_row+='   '+sep
					next_row+='   '+sep
					next_nodes.extend([None, None])
					continue
				if n.value != None:       
					buf=' '*int((5-len(str(n.value)))/2)
					cur_row+='%s%s%s'%(buf, str(n.value), buf)+sep
				else:
					cur_row+=' '*5+sep
				if n.left!=None:  
					next_nodes.append(n.left)
					next_row+=' /'+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)
				if n.right!=None: 
					next_nodes.append(n.right)
					next_row+='\ '+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)
			content+=(current_height*'   '+cur_row+'\n'+current_height*'   '+next_row+'\n')
			current_nodes=next_nodes
			sep=' '*int(len(sep)/2) # cut separator size in half
		return content

	def insert(self, value): # Function to remove base cases from insert function
		if self.root == None:
			self.root = AVLTreeNode(value) # Inserts into root b/c tree empty
		else: 
			self._insert(value, self.root) # Call insert because we need to insert it farther down

	def _insert(self, value, current_node):
		if value < current_node.value: # It needs to be inserted left of node
			if current_node.left == None: # CASE: if left child does not exist
				current_node.left = AVLTreeNode(value) # Set node to left
				current_node.left.parent = current_node # Point to parent
				self._inspect_insertion(current_node.left) # Needs to inspect to check if tree needs rebalance
			else:
				self._insert(value, current_node.left) # Recursively call insert and iterate down to left
		elif value > current_node.value: # It needs to be inserted right of node
			if current_node.right == None: # CASE: if right child does not exist
				current_node.right = AVLTreeNode(value) # Set node to right
				current_node.right.parent = current_node # Point to parent
				self._inspect_insertion(current_node.right) # Needs to inspect to check if tree needs rebalance
			else:
				self._insert(value, current_node.right) # Recursively call insert and iterate down to left
		else:
			print("Value already in tree!")

	def print_tree(self):
		if self.root != None:
			self._print_tree(self.root)

	def _print_tree(self, current_node):
		if current_node != None:
			self._print_tree(current_node.left)
			print ('%s, h=%d'%(str(current_node.value), current_node.height)) # Prints height
			self._print_tree(current_node.right)

	def height(self): # Calls height for entire tree
		if self.root != None: # If it is not empty
			return self._height(self.root, 0) # Return the height of the entire tree
		else:
			return 0

	def _height(self, current_node, current_height): # Returns height of current nocd
		if current_node == None: 
			return current_height

		left_height = self._height(current_node.left, current_height + 1) 
		right_height = self._height(current_node.right,  current_height + 1)
		return max(left_height, right_height) # Take greater height b/c height == length to longest leaf

	def find(self, value): # Remove 1 base case from _find function
		if self.root != None:
			return self._find(value, self.root)
		else:
			return None

	def _find(self, value, current_node):
		if value == current_node.value: # Base case: if values are == then return found node
			return current_node
		elif value < current_node.value and current_node.left != None: # Iterate down left recursively call _find
			return self._find(value, current_node.left)
		elif value > current_node.value and current_node.right != None: # Iterate down right recursively call _find
			return self._find(value, current_node.right)

	def delete_value(self, value):
		return self.delete_node(self.find(value)) # Given value use find to delete node

	def delete_node(self, node):
		if node == None or self.find(node.value) == None: # First Base Case if node is not in tree.
			print("Node not found!")
			return None 

		def min_value_node(n): # Helper function to return minimum value of left branch of the tree.
			current = n
			while current.left != None:
				current = current.left
			return current

		def num_children(n): # Helper function to return number of children of a node.
			num_children = 0
			if n.left != None: 
				num_children += 1
			if n.right != None: 
				num_children += 1
			return num_children

		node_parent = node.parent # Define parent, needs to be re pointed b/c node is getting deleted.
		node_children = num_children(node)
		# Case 1 Node has no children
		if node_children == 0:
			if node_parent != None:
				if node_parent.left == node:
					node_parent.left = None # this removes the node by removing pointer
				else:
					node_parent.right = None # this removes the node by removing pointer

			else:
				self.root = None
		# Case 2 Node has 1 child
		if node_children == 1:
			if node.left != None:
				child = node.left
			else:
				child = node.right

			if node_parent != None:
				if node_parent.left == node:
					node_parent.left = child
				else:
					node_parent.right = child
			else:
				self.root = child

			child.parent = node_parent
		# Case 3 Node has 2 children
		if node_children == 2:
			# Defines successor
			successor = min_value_node(node.right)
			node.value = successor.value
			self.delete_node(successor) # Recursively calls it on successor
			return

		if node_parent != None:
			node_parent.height = 1 + max(self.get_height(node_parent.left), self.get_height(node_parent.right))
			# Inspect because tree might need to be rebalanced after a node is deleted.
			self._inspect_deletion(node_parent)

	def search(self, value): # Removes 1 base case from _search
		if self.root != None:
			return self._search(value, self.root) # Call search on root
		else:
			return False # Root doesnt exist then return false

	def _search(self, value, current_node):
		if value == current_node.value: # Base Case: checks if value is = to node value
			return True
		elif value < current_node.value and current_node.left != None: # Iterate down left recursively calling _search
			return self._search(value, current_node.left)
		elif value > current_node.value and current_node.right != None: # Iterate down right recursively calling _search
			return self._search(value, current_node.right)
		return False 


	# Functions specific for AVL -----------------------------------------------------------V
	def _inspect_insertion(self, current_node, path = []):
		if current_node.parent == None: # Base Case if parent doesnt exist exit
			return

		path = [current_node] + path
		# Get heights so you can check if the difference between them is greater than 1 if so then they need rebalancing
		left_height = self.get_height(current_node.parent.left) # Check left height
		right_height = self.get_height(current_node.parent.right) #Check right height

		if abs(left_height - right_height) > 1: # If difference between heights is greater than 1 its not balanced EX:     
	# 	    7      
    #    /    \     
    #   6      8    
    #            \   
    #            9  # Not balanced right is greater than 1 difference in height.
	#             \
	#             10
			path = [current_node.parent] + path # Set path required for rebalancing
			self._rebalance_node(path[0], path[1], path[2]) # Rebalance because its currently unbalanced
			return

		# If it does not need rebalancing set new height and recursively call inspect_insertion
		new_height = 1 + current_node.height 
		if new_height > current_node.parent.height:
			current_node.parent.height = new_height

		self._inspect_insertion(current_node.parent, path)

	def _inspect_deletion(self, current_node):
		if current_node == None:  # Base Case if parent doesnt exist exit
			return

		# Get heights so you can check if the difference between them is greater than 1 if so then they need rebalancing
		left_height = self.get_height(current_node.left) # Check left height
		right_height = self.get_height(current_node.right) # Check right height

		if abs(left_height - right_height) > 1:  # If difference between heights is greater than 1 its not balanced EX:     
	# 	    7      
    #    /    \     
    #   6      8    
    #            \   
    #            9  # Not balanced right is greater than 1 difference in height.
	#             \
	#             10
			# Set y x using taller child
			y = self.taller_child(current_node)
			x = self.taller_child(y) 
			self._rebalance_node(current_node, y, x) # Rebalance

		self._inspect_deletion(current_node.parent) # Recursively call with parent

	def _rebalance_node(self, z, y, x):
		# There are 4 cases when rebalancing an AVL tree 
		# 1. Left Left   case: y is left  child of z and x is left  child of y   ------> Right rotation
		# 2. Left Right  case: y is left  child of z and x is right child of y   ------> Left Right rotation
		# 3. Right Right case: y is right child of z and x is right child of y   ------> Left rotation
		# 4. Right Left  case: y is right child of z and x is left  child of y   ------> Right Left rotation
		if y == z.left and x == y.left: # Case 1
			self._right_rotate(z)
		elif y == z.left and x == y.right: # Case 2
			self._left_rotate(y)
			self._right_rotate(z)
		elif y == z.right and x == y.right: # Case 3
			self._left_rotate(z)
		elif y == z.right and x == y.left: # Case 4
			self._right_rotate(y)
			self._left_rotate(z)
		else: # Error with x y or z
			raise Exception('ERROR: x, y, or z not correctly set when called.')

	def _right_rotate(self, z):
	# 	     7      
    #       / \       # In this example 6 is t3 
    #     6    8      # t3 is the rotation point and its rotated right until its root node
    #    /
	#   5
	#  /
	# 4 # Result:
	# 	     6      
    #       / \      
    #      5   7      
    #    /      \
	#   4        8
		sub_root = z.parent 
		y = z.left
		t3 = y.right
		y.right = z
		z.parent = y
		z.left = t3
		if t3 != None: t3.parent = z
		y.parent = sub_root
		if y.parent == None:
				self.root = y
		else:
			if y.parent.left == z:
				y.parent.left = y
			else:
				y.parent.right = y		
		z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
		y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

	def _left_rotate(self, z):
	# 	    7      
    #    /    \       # In this example 8 is t2 and a left rotation, would swap 8 to be the root and keep 7 and 6 as left children 
    #   6      8    
    #            \   
    #            9  # Not balanced right is greater than 1 difference in height.
	#             \
	#             10
		sub_root = z.parent 
		y = z.right
		t2 = y.left
		y.left = z
		z.parent = y
		z.right = t2
		if t2 != None: t2.parent = z
		y.parent = sub_root
		if y.parent == None: 
			self.root = y
		else:
			if y.parent.left == z:
				y.parent.left = y
			else:
				y.parent.right = y
		z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
		y.height= 1 + max(self.get_height(y.left), self.get_height(y.right))

	def get_height(self, current_node):
		if current_node == None:
			return 0
		return current_node.height # Returns height value of node

	def taller_child(self, current_node):
		left = self.get_height(current_node.left)
		right = self.get_height(current_node.right)

		if left >= right:
			return current_node.left
		else:
			return current_node.right

# Test code
tree = AVLTree()
for i in range(10):
	print("Inserting %d"%i)
	tree.insert(i)
	print(tree)
for i in range(10):
	print("Deleting %d"%i)
	tree.delete_value(i)
	print(tree)