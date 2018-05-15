class BiCyle:
    def __init__(self, brand_name, model_name, 
                    wheel, frame, seat, owner, ):
        self.brand_name = brand_name 
        self.model_name = model_name
        self.wheel = wheel
        self.frame = frame
        self.seat = seat
        self.owner = owner
        
    def __str__(self):
        return brand_name + ' ' + model_name + ' owned by ' + owner
        
    def __eq__(self, other):
        return self.model_name == other.model_name
        
    def __add__(self, other):
        return Bicyle(self.brand_name + other.brand_name, 
                      self.model_name + other.model_name, 
                      self.wheel + other.wheel, 
                      self.frame + other.frame, 
                      self.seat + other.seat, 
                      self.owner + other.owner,) 
                      
     