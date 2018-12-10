from collections import OrderedDict
from PyQt5.QtCore import QObject

##  Abstract base class groups of actors
class Group(QObject):

    ## initialization
    def __init__(self, scene,  **kwargs):
        """Initialize actor."""
        super(Group, self).__init__()

        ## set scene
        self._name = kwargs.get("name", None)
        self._scene = scene
        self._viewport = kwargs.get("viewport", (0.0, 0.0, 1.0, 1.0))

        ## parts list
        self._parts = OrderedDict()
        self._pickable = True
        self._visible = True
        self._selectable = False
        self._selected = False
        self._errorHighlight = False
        self._warningHighlight = False


    @property
    def name(self):
        """Returns the name of this actor"""
        return self._name


    def setName(self, name):
        """Sets this actor's name"""
        self._name = name


    def isPickable(self):
        """Sets whether or not this actor is pickable"""
        return self._pickable
        
        
    def setPickable(self, value):
        """Sets whether this actor is pickable"""
        self._pickable = value
        
        
    def isVisible(self):
        """Sets the visibility of this actor"""
        return self._visible


    def setVisible(self, value):
        """Sets the visibility of this actor"""
        self._visible = value


    def setSelectable(self, value):
        """Sets whther or not this group is selectable"""
        self._selectable = value


    def isSelectable(self):
        """Returns true if group is selectable"""
        return self._selectable


    def isSelected(self):
        """Returns true if it is selected"""
        return self._selected


    def setSelected(self, value):
        """Sets selection to value"""
        self._selected = value


    def setErrorHighlight(self, value):
        """Sets the error highlight"""
        self._errorHighlight = value

            
    def setWarningHighlight(self, value):
        """Sets the warning highlight"""
        self._warningHighlight = value    
        
                
    @property
    def scene(self):
        """Returns the parent scene"""
        return self._scene


    @property
    def parts(self):
        """Returns parts list"""
        return list(self._parts.values())


    def findPartByName(self, name):
        """Returns an actor by name if it exists"""
        if name in self._parts.keys():
            return self._parts[name]
        return None


    def addPart(self, part):
        """Add a part to the group"""
        self._parts[part.name] = part

