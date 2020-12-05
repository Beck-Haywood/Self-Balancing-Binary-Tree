class Node:
	def __init__(self, value = None):
	  self.parent = None  # Parent Node
	  self.right = None  # Right Child Pointer
	  self.left = None  # Left Child Pointer
	  self.value = value  # Value of node
	  self.height = 1  # Height for current node(Distance to leaf)

class AVLTree:
	def __init__(self):
		self.root = None

	def insert(self, value):
		if self.root == None:
			self.root = Node(value)
		else:
			self._insert(value, self.root)

	def _insert(self, value, current_node):
		if value < current_node.value: #
			if current_node.left == None: # if left child does not exist case
				current_node.left = Node(value)
				current_node.left.parent = current_node # set parent
				self._inspect_insertion(current_node.left)
			else:
				self._insert(value, current_node.left)
		elif value > current_node.value:
			if current_node.right == None: # if right child does not exist case
				current_node.right = Node(value)
				current_node.right.parent=current_node # set parent
				self._inspect_insertion(current_node.right)
			else:
				self._insert(value, current_node.right)
		else:
			print(ValueError("Value already inside tree!"))

	def print_tree(self):
		if self.root != None:
			self._print_tree(self.root)

	def _print_tree(self, current_node):
		if current_node != None:
			self._print_tree(current_node.left)
			print ('%s, h=%d'%(str(current_node.value), current_node.height))
			self._print_tree(current_node.right)

	def height(self):
		if self.root != None:
			return self._height(self.root, 0)
		else:
			return 0

	def _height(self, current_node, current_height):
		if current_node == None: return current_height
		left_height = self._height(current_node.left, current_height + 1)
		right_height = self._height(current_node.right, current_height + 1)
		return max(left_height, right_height)


	def find(self, value):
		if self.root != None:
			return self._find(value, self.root)
		else:
			return None

	def _find(self, value, current_node):
		if value == current_node.value:
			return current_node
		elif value < current_node.value and current_node.left != None:
			return self._find(value, current_node.left)
		elif value > current_node.value and current_node.right != None:
			return self._find(value, current_node.right)

	def delete_value(self, value):
		return self.delete_node(self.find(value))


	def delete_node(self, node):
		if node == None or self.find(node.value) == None:
			print("Node to be deleted not found in the tree!")
			return None 

		# returns the node with min value in tree rooted at input node
		def min_value_node(n):
			current = n
			while current.left != None:
				current = current.left
			return current

		# returns the number of children for the specified node
		def num_children(n):
			num_children = 0
			if n.left != None: num_children += 1
			if n.right != None: num_children += 1
			return num_children

		# get the parent of the node to be deleted
		node_parent = node.parent

		# get the number of children of the node to be deleted
		node_children = num_children(node)

		# break operation into different cases based on the
		# structure of the tree & node to be deleted

		# CASE 1 (node has no children)
		if node_children == 0:

			if node_parent != None:
				# remove reference to the node from the parent
				if node_parent.left == node:
					node_parent.left = None
				else:
					node_parent.right = None
			else:
				self.root = None

		# CASE 2 (node has a single child)
		if node_children == 1:

			# get the single child node
			if node.left != None:
				child = node.left
			else:
				child = node.right

			if node_parent != None:
				# replace the node to be deleted with its child
				if node_parent.left == node:
					node_parent.left = child
				else:
					node_parent.right = child
			else:
				self.root = child

			# correct the parent pointer in node
			child.parent = node_parent

		# CASE 3 (node has two children)
		if node_children == 2:

			# get the inorder successor of the deleted node
			successor = min_value_node(node.right)

			# copy the inorder successor's value to the node formerly
			# holding the value we wished to delete
			node.value = successor.value

			# delete the inorder successor now that it's value was
			# copied into the other node
			self.delete_node(successor)

			# exit function so we don't call the _inspect_deletion twice
			return

		if node_parent != None:
			# fix the height of the parent of current node
			node_parent.height = 1 + max(self.get_height(node_parent.left), self.get_height(node_parent.right))

			# begin to traverse back up the tree checking if there are
			# any sections which now invalidate the AVL balance rules
			self._inspect_deletion(node_parent)

	def search(self, value):
		if self.root != None:
			return self._search(value, self.root)
		else:
			return False

	def _search(self, value, current_node):
		if value == current_node.value:
			return True
		elif value < current_node.value and current_node.left != None:
			return self._search(value, current_node.left)
		elif value > current_node.value and current_node.right != None:
			return self._search(value, current_node.right)
		return False 

	# AVL functions

	def _inspect_insertion(self, current_node, path = []):
		# Base Case
		if current_node.parent == None: return # when hit root node
		path = [current_node] + path # prepend current node to front of list of nodes
		
		left_height = self.get_height(current_node.parent.left)
		right_height = self.get_height(current_node.parent.right)

		if abs(left_height - right_height) > 1: # checks difference between height to check if it is balanced.
			path = [current_node.parent] + path
			self._rebalance_node(path[0], path[1], path[2])
			return

		new_height = 1 + current_node.height

		if new_height > current_node.parent.height:
			current_node.parent.height = new_height
		
		self._inspect_insertion(current_node.parent, path)

	def _inspect_deletion(self, current_node):
		# Base Case
		if current_node == None: return 
		print(current_node.parent)
		left_height = self.get_height(current_node.parent.left)
		right_height = self.get_height(current_node.parent.right)

		if abs(left_height - right_height) > 1: # checks difference between height to check if it is balanced.
			y = self.taller_child(current_node)
			x = self.taller_child(y)
			self._rebalance_node(current_node, y, x)
		if current_node.parent != None:
			self._inspect_deletion(current_node.parent)

	def _rebalance_node(self, z, y, x):
		if y == z.left and x == y.left:
			self._right_rotate(z)
		elif y == z.left and x == y.right:
			self._left_rotate(y)
			self._right_rotate(z)
		elif y == z.right and x == y.right:
			self._left_rotate(z)
		elif y == z.right and x == y.left:
			self._right_rotate(y)
			self._left_rotate(z)
		else:
			raise Exception('_rebalance_node: z,y,x node configuration not recognized!')

	def _right_rotate(self, z):
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
		z.height = 1 + max(self.get_height(z.left),
			self.get_height(z.right))
		y.height = 1 + max(self.get_height(y.left),
			self.get_height(y.right))

	def _left_rotate(self, z):
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
		z.height = 1 + max(self.get_height(z.left),
			self.get_height(z.right))
		y.height = 1 + max(self.get_height(y.left),
			self.get_height(y.right))

	def get_height(self, current_node):
		if current_node==None: return 0
		return current_node.height

	def taller_child(self, current_node):
		left = self.get_height(current_node.left)
		right = self.get_height(current_node.right)
		return current_node.left if left >= right else current_node.right

tree = AVLTree()
for i in range(10):
	print("Inserting %d"%i)
	tree.insert(i)
	print(tree)
for i in range(10):
	print("Deleting %d"%i)
	tree.delete_value(i)
	print(tree)
