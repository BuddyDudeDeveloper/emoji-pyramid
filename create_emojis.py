import maya.cmds as cmds
from random import uniform, choice;
from math import floor;

"""
Adds an extra string attribute to all shapes in a group. In this case, it is used for paths to textures.

attrname:str - The name of the extra attribute.
paths:list - A collection of paths to each texture.
"""
def add_map(attrname, paths):
	
	# we take care of dealing with the arnold prefix shenanigans
	attrname = 'mtoa_constant_' + attrname
	
	"""
	Selections will be either be a number of shapes or one or more groups that contain shapes.
	"""
	selections = cmds.ls(sl=True)

	# For each member of the group, get their transform node and add them to the shape list.
	for sel in selections:
		shapes = cmds.listRelatives(sel, s=True)
		# sel is a shape, therefore, does not have shape relatives
		if shapes == None:
			transforms = cmds.listRelatives(sel, children=True);
			shapes = []
			for transform in transforms:
				shapes.extend(cmds.listRelatives(transform, s=True));

		# If there are no shapes, inform the user.
		if len(shapes) == 0 or len(shapes[0]) == 0:
			print('Cannot find a shape to add attribute')
			return

		# For each shape, pick a texture map and assign it to the map extra attribute.
		for shape in shapes:
			path = choice(paths);
			if cmds.attributeQuery(attrname, node=shape, exists=True) == False:
				cmds.addAttr(shape, ln=attrname, sn=attrname, nn=attrname, k=True, dt='string')
			cmds.setAttr(shape + '.' + attrname, path, type="string")

# Adds a random texture from the sourceimages directory to each shape in a group.
def add_random_textures():

	# A path to each .tx file in the sourceimages directory is stored in a list.
	texture_path = cmds.workspace(q = True, rootDirectory = True) + "sourceimages/";
	texture_names = cmds.getFileList(folder = texture_path, filespec='*.tx');

	# To make sure the full path to the texture us correct, the path to the workspace is appended to the front.
	length = len(texture_names);
	for i in range(0, length):
		texture_names[i] = texture_path + texture_names[i];

	# The paths are then assigned to each member of the group.
	add_map("map", texture_names);

"""
Creates the pyramid of emojis in the scene.

stack:int - The number of rows, columns and vertical layers in the pyramid.
"""

def create_emojis(stack):	

	# Each circle that will be an emoji is stored in a list so it can be grouped later.
	emojis = [];

	# For each layer, create a grid of emojis.
	for height in range(0, stack):

		# As the pyramid's vertical layer increases, the number of emojis in it decreases.
		length = stack - height;
		grid_range = range(0, length);

		# Since each emoji grid starts at x = 0 and z = 0, a value is needed to move the center of each layer so they line up with the center of the previous grid.
		offset = .5 * height;

		# For each grid and column in the layer, create an emoji.
		for row in grid_range:
			for column in grid_range:
				emojis.extend(cmds.sphere(r = .5));

				# To make the emojis look like they are sitting on top of each other, the height offset is divided by 1.5.
				cmds.move(row + offset, height - offset/1.5, column + offset);
				cmds.rotate(uniform(0, 360), uniform(0, 360), uniform(0, 360));

	# The emojis are then grouped and assigned a random texture.
	cmds.group(emojis, n = "emojis");
	add_random_textures();

	
