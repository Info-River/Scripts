
class emergency_actor:

    def __init__(self,coords,id):
        self.coords=coords
        self.id=id

    def update_coords(self,new_coords):
        self.coords=new_coords

    def get_coords(self):
        return self.coords

    def get_id(self):
        return self.id